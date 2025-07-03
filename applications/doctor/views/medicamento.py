# applications/doctor/views/medicamento.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Medicamento, TipoMedicamento, MarcaMedicamento
from applications.doctor.forms.medicamento import MedicamentoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para Medicamento
class MedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = Medicamento
    template_name = 'doctor/medicamento/list.html'
    context_object_name = 'medicamentos'
    paginate_by = 2
    permission_required = 'view_medicamento'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombre__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
            self.query.add(Q(concentracion__icontains=search_query), Q.OR)
            self.query.add(Q(tipo__nombre__icontains=search_query), Q.OR)
            self.query.add(Q(marca_medicamento__nombre__icontains=search_query), Q.OR)
        return self.model.objects.select_related('tipo', 'marca_medicamento').filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Medicamentos'
        context['title1'] = 'Medicamentos'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class MedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'doctor/medicamento/form.html'
    success_url = reverse_lazy('doctor:medicamento_list')
    permission_required = 'add_medicamento'

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el medicamento. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Medicamento'
        context['title1'] = 'Medicamentos'
        context['action_url'] = 'doctor:medicamento_create'
        context['btn_text'] = 'Guardar Medicamento'
        context['is_update'] = False
        return context

class MedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'doctor/medicamento/form.html'
    success_url = reverse_lazy('doctor:medicamento_list')
    permission_required = 'change_medicamento'

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el medicamento. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Medicamento'
        context['title1'] = f'Editar Medicamento: {self.object.nombre}'
        context['action_url'] = 'doctor:medicamento_update'
        context['btn_text'] = 'Actualizar Medicamento'
        context['is_update'] = True
        context['medicamento'] = self.object
        return context

class MedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    success_url = reverse_lazy('doctor:medicamento_list')
    permission_required = 'delete_medicamento'

    def post(self, request, *args, **kwargs):
        try:
            medicamento_nombre = self.get_object().nombre
            self.get_object().delete()
            messages.success(self.request, f'Medicamento "{medicamento_nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el medicamento: {e}')
        return redirect(self.success_url)

# Funciones wrapper para mantener compatibilidad con URLs existentes
def medicamento_list(request):
    return MedicamentoListView.as_view()(request)

def medicamento_create(request):
    return MedicamentoCreateView.as_view()(request)

def medicamento_update(request, pk):
    return MedicamentoUpdateView.as_view()(request, pk=pk)

def medicamento_delete(request, pk):
    return MedicamentoDeleteView.as_view()(request, pk=pk)