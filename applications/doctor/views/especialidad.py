# applications/doctor/views/especialidad.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Especialidad
from applications.doctor.forms.especialidad import EspecialidadForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# --- Vistas para el modelo Especialidad ---

class EspecialidadListView(PermissionMixin, ListViewMixin, ListView):
    model = Especialidad
    template_name = "doctor/especialidad/list.html"
    context_object_name = "especialidades"
    paginate_by = 2
    permission_required = 'view_especialidad'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombre__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Especialidades'
        context['title1'] = 'Especialidades'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class EspecialidadCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "doctor/especialidad/form.html"
    success_url = reverse_lazy('doctor:especialidad_list')
    permission_required = 'add_especialidad'

    def form_valid(self, form):
        messages.success(self.request, 'Especialidad creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear la especialidad. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nueva Especialidad'
        context['title1'] = 'Especialidades'
        return context

class EspecialidadUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "doctor/especialidad/form.html"
    success_url = reverse_lazy('doctor:especialidad_list')
    permission_required = 'change_especialidad'

    def form_valid(self, form):
        messages.success(self.request, 'Especialidad actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar la especialidad. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Especialidad'
        context['title1'] = 'Especialidades'
        return context

class EspecialidadDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Especialidad
    template_name = "doctor/especialidad/form.html"
    success_url = reverse_lazy('doctor:especialidad_list')
    permission_required = 'delete_especialidad'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Especialidad eliminada exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar la especialidad: {e}')
        return redirect(self.success_url)