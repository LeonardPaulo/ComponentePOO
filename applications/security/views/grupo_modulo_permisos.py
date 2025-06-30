# Vistas para el manejo de grupos, módulos y permisos de seguridad

from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.group_module_permisos import GroupModulePermissionForm
from applications.security.models import GroupModulePermission
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q, Count
from django.contrib.auth.models import Group, Permission
from applications.security.models import Module
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/grupos_modulos_permisos/list.html'
    model = GroupModulePermission
    context_object_name = 'GroupModulePermissions'
    permission_required = 'view_groupmodulepermission'
    paginate_by = 50

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(group__name__icontains=q1), Q.OR)
            self.query.add(Q(module__name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('group', 'module').prefetch_related('permissions').order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        
        # Calcular estadísticas
        queryset = self.get_queryset()
        
        # Contar grupos únicos
        unique_groups = Group.objects.count()
        
        # Contar módulos únicos
        unique_modules = Module.objects.count()
        
        # Total de asignaciones
        total_assignments = queryset.count()
        
        # Total de permisos asignados
        total_permissions = 0
        for assignment in queryset:
            total_permissions += assignment.permissions.count()
        
        context['stats'] = {
            'unique_groups': unique_groups,
            'unique_modules': unique_modules,
            'total_assignments': total_assignments,
            'total_permissions': total_permissions
        }
        
        return context


class GroupModulePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GroupModulePermission
    template_name = 'security/grupos_modulos_permisos/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'add_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Asignar Permisos por Grupo'
        context['back_url'] = self.success_url
        
        # Solo necesitamos los grupos para el combo
        context['groups'] = Group.objects.all()
        
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo_modulo_permiso = self.object
        messages.success(self.request, f"Éxito al crear el grupo módulo permiso {grupo_modulo_permiso.id}.")
        return response


# Vista para obtener módulos con conteo de permisos asignados
class GetModulesWithPermissionsView(PermissionMixin, View):
    permission_required = 'view_groupmodulepermission'
    
    def get(self, request, *args, **kwargs):
        group_id = request.GET.get('group_id')
        if not group_id:
            return JsonResponse({'error': 'No se proporcionó group_id'}, status=400)
        
        try:
            # Obtener todos los módulos
            modules = Module.objects.all()
            modules_data = []
            
            for module in modules:
                # Contar permisos asignados para este grupo-módulo
                try:
                    gmp = GroupModulePermission.objects.get(group_id=group_id, module=module)
                    assigned_permissions = gmp.permissions.count()
                except GroupModulePermission.DoesNotExist:
                    assigned_permissions = 0
                
                # Total de permisos disponibles en el módulo
                total_permissions = module.permissions.count()
                
                modules_data.append({
                    'id': module.id,
                    'name': module.name,
                    'icon': module.icon or 'fas fa-cube',
                    'assigned_permissions': assigned_permissions,
                    'total_permissions': total_permissions,
                    'has_assignment': assigned_permissions > 0
                })
            
            return JsonResponse({
                'modules': modules_data
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# Vista para obtener permisos de un módulo específico
class GetModulePermissionsView(PermissionMixin, View):
    permission_required = 'view_groupmodulepermission'
    
    def get(self, request, *args, **kwargs):
        module_id = request.GET.get('module_id')
        group_id = request.GET.get('group_id')
        
        if not module_id or not group_id:
            return JsonResponse({'error': 'Faltan parámetros requeridos'}, status=400)
        
        try:
            module = Module.objects.get(pk=module_id)
            
            # Siempre mostrar SOLO los permisos específicos del módulo seleccionado
            # Sin importar si es superusuario o no
            module_permissions = list(module.permissions.values('id', 'name', 'codename'))
            
            # Agregar información adicional a cada permiso
            for perm in module_permissions:
                perm['is_module_specific'] = True
                perm['is_header'] = False
            
            # Obtener permisos ya asignados al grupo para este módulo
            assigned_permission_ids = []
            try:
                gmp = GroupModulePermission.objects.get(group_id=group_id, module_id=module_id)
                assigned_permission_ids = list(gmp.permissions.values_list('id', flat=True))
            except GroupModulePermission.DoesNotExist:
                pass
            
            # Marcar cuáles están asignados
            for permission in module_permissions:
                permission['is_assigned'] = permission['id'] in assigned_permission_ids
            
            return JsonResponse({
                'module_name': module.name,
                'module_icon': module.icon or 'fas fa-cube',
                'permissions': module_permissions,
                'has_existing_assignment': len(assigned_permission_ids) > 0,
                'is_superuser': request.user.is_superuser,
                'total_permissions': len(module_permissions)
            })
            
        except Module.DoesNotExist:
            return JsonResponse({'error': 'Módulo no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Vista para guardar permisos de un módulo específico
@method_decorator(csrf_exempt, name='dispatch')
class SaveModulePermissionsView(PermissionMixin, View):
    permission_required = 'add_groupmodulepermission'
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')
            module_id = data.get('module_id')
            permission_ids = data.get('permission_ids', [])
            
            if not group_id or not module_id:
                return JsonResponse({'success': False, 'message': 'Faltan datos requeridos'})
            
            # Verificar que existan
            group = Group.objects.get(id=group_id)
            module = Module.objects.get(id=module_id)
            
            # Crear o obtener la asignación
            gmp, created = GroupModulePermission.objects.get_or_create(
                group=group, 
                module=module
            )
            
            # Si no hay permisos seleccionados, eliminar la asignación
            if not permission_ids:
                if not created:  # Solo eliminar si ya existía
                    gmp.delete()
                    return JsonResponse({
                        'success': True, 
                        'message': f'Permisos removidos para {group.name} - {module.name}',
                        'assigned_count': 0
                    })
                else:
                    return JsonResponse({
                        'success': True, 
                        'message': f'No se asignaron permisos para {group.name} - {module.name}',
                        'assigned_count': 0
                    })
            else:
                # Asignar permisos seleccionados
                permissions = Permission.objects.filter(id__in=permission_ids)
                gmp.permissions.set(permissions)
                
                action = "creados" if created else "actualizados"
                return JsonResponse({
                    'success': True, 
                    'message': f'Permisos {action} para {group.name} - {module.name}',
                    'assigned_count': len(permission_ids)
                })
            
        except (Group.DoesNotExist, Module.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Grupo o módulo no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'})


class GroupModulePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GroupModulePermission
    template_name = 'security/grupos_modulos_permisos/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'change_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar grupo módulo permiso'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo_modulo_permiso = self.object
        messages.success(self.request, f"Éxito al actualizar el grupo módulo permiso {grupo_modulo_permiso.id}.")
        return response


class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'security/grupos_modulos_permisos/confirm_delete.html'
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'delete_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar grupo módulo permiso'
        context['description'] = f"¿Desea eliminar el grupo módulo permiso: {self.object.group.name} - {self.object.module.name}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f"Éxito al eliminar el grupo módulo permiso.")
        return response


# Vista adicional para asignaciones múltiples desde el formulario principal
@method_decorator(csrf_exempt, name='dispatch')
class BulkAssignPermissionsView(PermissionMixin, View):
    permission_required = 'add_groupmodulepermission'
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            assignments = data.get('assignments', [])
            if not assignments:
                return JsonResponse({'success': False, 'message': 'No se recibieron asignaciones.'})

            messages = []
            for item in assignments:
                group_id = item.get('group_id')
                module_id = item.get('module_id')
                permission_ids = item.get('permission_ids', [])

                if not group_id or not module_id or not permission_ids:
                    continue

                try:
                    group = Group.objects.get(id=group_id)
                    module = Module.objects.get(id=module_id)
                    permissions = Permission.objects.filter(id__in=permission_ids)
                except:
                    continue

                existing = GroupModulePermission.objects.filter(group=group, module=module).first()
                if existing:
                    messages.append(f"Ya existe: {group.name} - {module.name}")
                    continue

                assignment = GroupModulePermission.objects.create(group=group, module=module)
                assignment.permissions.set(permissions)
                messages.append(f"Creado: {group.name} - {module.name}")

            return JsonResponse({'success': True, 'message': " | ".join(messages)})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'})