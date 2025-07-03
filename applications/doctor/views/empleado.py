# applications/doctor/views/empleado.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Empleado
from applications.doctor.forms.empleado import EmpleadoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para Empleado
class EmpleadoListView(PermissionMixin, ListViewMixin, ListView):
    model = Empleado
    template_name = 'doctor/empleado/list.html'
    context_object_name = 'empleados'
    paginate_by = 10
    permission_required = 'view_empleado'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombres__icontains=search_query), Q.OR)
            self.query.add(Q(apellidos__icontains=search_query), Q.OR)
            self.query.add(Q(cedula_ecuatoriana__icontains=search_query), Q.OR)
            self.query.add(Q(cargo__nombre__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Empleados'
        context['title1'] = 'Empleados'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class EmpleadoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'doctor/empleado/form.html'
    success_url = reverse_lazy('doctor:empleado_list')
    permission_required = 'add_empleado'

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

class EmpleadoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'doctor/empleado/form.html'
    success_url = reverse_lazy('doctor:empleado_list')
    permission_required = 'change_empleado'

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

class EmpleadoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    success_url = reverse_lazy('doctor:empleado_list')
    permission_required = 'delete_empleado'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Empleado eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el empleado: {e}')
        return redirect(self.success_url)