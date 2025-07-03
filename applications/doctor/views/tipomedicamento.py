# applications/doctor/views/tipomedicamento.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import TipoMedicamento
from applications.doctor.forms.tipomedicamento import TipoMedicamentoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para TipoMedicamento
class TipoMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = TipoMedicamento
    template_name = 'doctor/tipomedicamento/list.html'
    context_object_name = 'tipos_medicamento'
    paginate_by = 2
    permission_required = 'view_tipomedicamento'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombre__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Tipos de Medicamentos'
        context['title1'] = 'Tipos de Medicamentos'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class TipoMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'doctor/tipomedicamento/form.html'
    success_url = reverse_lazy('doctor:tiposmedicamento_list')
    permission_required = 'add_tipomedicamento'

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de medicamento creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el tipo de medicamento. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Tipo de Medicamento'
        context['title1'] = 'Tipos de Medicamentos'
        context['action_url'] = 'doctor:tiposmedicamento_create'
        context['btn_text'] = 'Guardar Tipo de Medicamento'
        context['is_update'] = False
        return context

class TipoMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'doctor/tipomedicamento/form.html'
    success_url = reverse_lazy('doctor:tiposmedicamento_list')
    permission_required = 'change_tipomedicamento'

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de medicamento actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el tipo de medicamento. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Medicamento'
        context['title1'] = f'Editar Tipo de Medicamento: {self.object.nombre}'
        context['action_url'] = 'doctor:tiposmedicamento_update'
        context['btn_text'] = 'Actualizar Tipo de Medicamento'
        context['is_update'] = True
        context['tipomedicamento'] = self.object
        return context

class TipoMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoMedicamento
    success_url = reverse_lazy('doctor:tiposmedicamento_list')
    permission_required = 'delete_tipomedicamento'

    def post(self, request, *args, **kwargs):
        try:
            tipomedicamento_nombre = self.get_object().nombre
            self.get_object().delete()
            messages.success(self.request, f'Tipo de medicamento "{tipomedicamento_nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el tipo de medicamento: {e}')
        return redirect(self.success_url)

# Funciones wrapper para mantener compatibilidad con URLs existentes
def tiposmedicamento_list(request):
    return TipoMedicamentoListView.as_view()(request)

def tiposmedicamento_create(request):
    return TipoMedicamentoCreateView.as_view()(request)

def tiposmedicamento_update(request, pk):
    return TipoMedicamentoUpdateView.as_view()(request, pk=pk)

def tiposmedicamento_delete(request, pk):
    return TipoMedicamentoDeleteView.as_view()(request, pk=pk)