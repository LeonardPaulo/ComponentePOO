# applications/doctor/views/empleado.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Empleado # Asegúrate de importar el modelo Empleado
from applications.doctor.forms.empleado import EmpleadoForm # Asegúrate de importar el formulario

# Vistas para Empleado
class EmpleadoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Empleado
    template_name = 'doctor/empleado/list.html'
    context_object_name = 'empleados' # Nombre de la variable en el template
    paginate_by = 10 
    permission_required = 'core.view_empleado' # Permiso requerido para ver la lista

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')

        if search_query:
            queryset = queryset.filter(
                Q(nombres__icontains=search_query) |
                Q(apellidos__icontains=search_query) |
                Q(cedula_ecuatoriana__icontains=search_query) |
                Q(cargo__nombre__icontains=search_query) # Búsqueda por nombre de cargo relacionado
            ).distinct()
        
        queryset = queryset.order_by('apellidos', 'nombres')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Empleados'
        context['title1'] = 'Empleados'
        context['search_query'] = self.request.GET.get('q', '')
        context['permissions'] = self.get_permissions_context(self.request)
        return context

    def get_permissions_context(self, request):
        return {
            'add_empleado': request.user.has_perm('core.add_empleado'),
            'change_empleado': request.user.has_perm('core.change_empleado'),
            'delete_empleado': request.user.has_perm('core.delete_empleado'),
        }

class EmpleadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'doctor/empleado/form.html'
    success_url = reverse_lazy('doctor:empleado_list')
    permission_required = 'core.add_empleado'

    def form_valid(self, form):
        messages.success(self.request, 'Empleado creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el empleado. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Empleado'
        context['title1'] = 'Empleados'
        return context

class EmpleadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'doctor/empleado/form.html'
    success_url = reverse_lazy('doctor:empleado_list')
    permission_required = 'core.change_empleado'

    def form_valid(self, form):
        messages.success(self.request, 'Empleado actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el empleado. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Empleado'
        context['title1'] = 'Empleados'
        return context

class EmpleadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Empleado
    success_url = reverse_lazy('doctor:empleado_list')
    permission_required = 'core.delete_empleado'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Empleado eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el empleado: {e}')
        return redirect(self.success_url)