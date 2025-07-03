# applications/doctor/views/diagnostico.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Diagnostico
from applications.doctor.forms.diagnostico import DiagnosticoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vista para listar todos los diagnósticos
class DiagnosticoListView(PermissionMixin, ListViewMixin, ListView):
    model = Diagnostico
    template_name = 'doctor/diagnostico/list.html'
    context_object_name = 'diagnosticos'
    paginate_by = 2
    permission_required = 'view_diagnostico'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(codigo__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('codigo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Diagnósticos'
        context['title1'] = 'Diagnósticos'
        context['search_query'] = self.request.GET.get('q', '')
        return context

# Vista para crear un nuevo diagnóstico
class DiagnosticoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'doctor/diagnostico/form.html'
    success_url = reverse_lazy('doctor:diagnostico_list')
    permission_required = 'add_diagnostico'

    def form_valid(self, form):
        messages.success(self.request, 'Diagnóstico creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el diagnóstico. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Diagnóstico'
        context['title1'] = 'Diagnósticos'
        return context

# Vista para actualizar un diagnóstico existente
class DiagnosticoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'doctor/diagnostico/form.html'
    success_url = reverse_lazy('doctor:diagnostico_list')
    permission_required = 'change_diagnostico'

    def form_valid(self, form):
        messages.success(self.request, 'Diagnóstico actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el diagnóstico. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Diagnóstico'
        context['title1'] = 'Diagnósticos'
        return context

# Vista para eliminar un diagnóstico
class DiagnosticoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    success_url = reverse_lazy('doctor:diagnostico_list')
    permission_required = 'delete_diagnostico'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Diagnóstico eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el diagnóstico: {e}')
        return redirect(self.success_url)