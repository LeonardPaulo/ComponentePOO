# applications/doctor/views/marcamedicamento.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import MarcaMedicamento
from applications.doctor.forms.marcamedicamento import MarcaMedicamentoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para Marca de Medicamento
class MarcaMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = MarcaMedicamento
    template_name = 'doctor/marcamedicamento/list.html'
    context_object_name = 'marcas'
    paginate_by = 2
    permission_required = 'view_marcamedicamento'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombre__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Marcas de Medicamentos'
        context['title1'] = 'Marcas de Medicamentos'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class MarcaMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'doctor/marcamedicamento/form.html'
    success_url = reverse_lazy('doctor:marcasmedicamento_list')
    permission_required = 'add_marcamedicamento'

    def form_valid(self, form):
        messages.success(self.request, 'Marca de Medicamento creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear la Marca de Medicamento. Por favor, revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Marca de Medicamento'
        context['title1'] = 'Crear Nueva Marca de Medicamento'
        context['action_url'] = 'doctor:marcamedicamento_create'
        context['btn_text'] = 'Guardar Marca'
        context['is_update'] = False
        return context

class MarcaMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = MarcaMedicamento
    form_class = MarcaMedicamentoForm
    template_name = 'doctor/marcamedicamento/form.html'
    success_url = reverse_lazy('doctor:marcasmedicamento_list')
    permission_required = 'change_marcamedicamento'

    def form_valid(self, form):
        messages.success(self.request, 'Marca de Medicamento actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar la Marca de Medicamento. Por favor, revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Marca de Medicamento'
        context['title1'] = f'Editar Marca de Medicamento: {self.object.nombre}'
        context['action_url'] = 'doctor:marcamedicamento_update'
        context['btn_text'] = 'Actualizar Marca'
        context['is_update'] = True
        context['marca'] = self.object
        return context

class MarcaMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = MarcaMedicamento
    success_url = reverse_lazy('doctor:marcasmedicamento_list')
    permission_required = 'delete_marcamedicamento'

    def post(self, request, *args, **kwargs):
        try:
            marca_nombre = self.get_object().nombre
            self.get_object().delete()
            messages.success(self.request, f'Marca "{marca_nombre}" eliminada exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar la marca: {e}')
        return redirect(self.success_url)

# Funciones wrapper para mantener compatibilidad con URLs existentes
def marcasmedicamento_list(request):
    return MarcaMedicamentoListView.as_view()(request)

def marcamedicamento_create(request):
    return MarcaMedicamentoCreateView.as_view()(request)

def marcamedicamento_update(request, pk):
    return MarcaMedicamentoUpdateView.as_view()(request, pk=pk)

def marcamedicamento_delete(request, pk):
    return MarcaMedicamentoDeleteView.as_view()(request, pk=pk)