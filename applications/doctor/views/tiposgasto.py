# applications/doctor/views/tiposgasto.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import TipoGasto
from applications.doctor.forms.tipogasto import TipoGastoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para TipoGasto
class TipoGastoListView(PermissionMixin, ListViewMixin, ListView):
    model = TipoGasto
    template_name = 'doctor/tipos_gasto/list.html'
    context_object_name = 'tipos_gasto'
    paginate_by = 2
    permission_required = 'view_tipogasto'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombre__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Tipos de Gasto'
        context['title1'] = 'Tipos de Gasto'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class TipoGastoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = 'doctor/tipos_gasto/form.html'
    success_url = reverse_lazy('doctor:tipogasto_list')
    permission_required = 'add_tipogasto'

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de gasto creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el tipo de gasto. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Tipo de Gasto'
        context['title1'] = 'Tipos de Gasto'
        context['action_url'] = 'doctor:tipogasto_create'
        context['btn_text'] = 'Guardar Tipo de Gasto'
        context['is_update'] = False
        return context

class TipoGastoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoGasto
    form_class = TipoGastoForm
    template_name = 'doctor/tipos_gasto/form.html'
    success_url = reverse_lazy('doctor:tipogasto_list')
    permission_required = 'change_tipogasto'

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de gasto actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el tipo de gasto. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Gasto'
        context['title1'] = f'Editar Tipo de Gasto: {self.object.nombre}'
        context['action_url'] = 'doctor:tipogasto_update'
        context['btn_text'] = 'Actualizar Tipo de Gasto'
        context['is_update'] = True
        context['tipogasto'] = self.object
        return context

class TipoGastoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoGasto
    success_url = reverse_lazy('doctor:tipogasto_list')
    permission_required = 'delete_tipogasto'

    def post(self, request, *args, **kwargs):
        try:
            tipogasto_nombre = self.get_object().nombre
            self.get_object().delete()
            messages.success(self.request, f'Tipo de gasto "{tipogasto_nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el tipo de gasto: {e}')
        return redirect(self.success_url)

# Funciones wrapper para mantener compatibilidad con URLs existentes
def tipogasto_list(request):
    return TipoGastoListView.as_view()(request)

def tipogasto_create(request):
    return TipoGastoCreateView.as_view()(request)

def tipogasto_update(request, pk):
    return TipoGastoUpdateView.as_view()(request, pk=pk)

def tipogasto_delete(request, pk):
    return TipoGastoDeleteView.as_view()(request, pk=pk)