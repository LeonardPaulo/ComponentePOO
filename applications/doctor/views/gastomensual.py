# applications/doctor/views/gastomensual.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import GastoMensual
from applications.doctor.forms.gastomensual import GastoMensualForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para Gasto Mensual
class GastoMensualListView(PermissionMixin, ListViewMixin, ListView):
    model = GastoMensual
    template_name = 'doctor/gastos_mensuales/list.html'
    context_object_name = 'gastos'
    paginate_by = 2
    permission_required = 'view_gastomensual'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(tipo_gasto__nombre__icontains=search_query), Q.OR)
            self.query.add(Q(observacion__icontains=search_query), Q.OR)
        return self.model.objects.select_related('tipo_gasto').filter(self.query).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Gastos Mensuales'
        context['title1'] = 'Gastos Mensuales'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class GastoMensualCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'doctor/gastos_mensuales/form.html'
    success_url = reverse_lazy('doctor:gastomensual_list')
    permission_required = 'add_gastomensual'

    def form_valid(self, form):
        messages.success(self.request, 'Gasto mensual agregado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al agregar el gasto mensual. Por favor, revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Gasto Mensual'
        context['title1'] = 'Gastos Mensuales'
        context['action_url'] = 'doctor:gastomensual_create'
        context['btn_text'] = 'Guardar Gasto Mensual'
        context['is_update'] = False
        return context

class GastoMensualUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GastoMensual
    form_class = GastoMensualForm
    template_name = 'doctor/gastos_mensuales/form.html'
    success_url = reverse_lazy('doctor:gastomensual_list')
    permission_required = 'change_gastomensual'

    def form_valid(self, form):
        messages.success(self.request, 'Gasto mensual actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el gasto mensual. Por favor, revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Gasto Mensual'
        context['title1'] = 'Gastos Mensuales'
        context['action_url'] = 'doctor:gastomensual_update'
        context['btn_text'] = 'Actualizar Gasto Mensual'
        context['is_update'] = True
        context['gasto'] = self.object
        return context

class GastoMensualDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GastoMensual
    success_url = reverse_lazy('doctor:gastomensual_list')
    permission_required = 'delete_gastomensual'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Gasto mensual eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el gasto mensual: {e}')
        return redirect(self.success_url)

# Funciones wrapper para mantener compatibilidad con URLs existentes
def gastomensual_list(request):
    return GastoMensualListView.as_view()(request)

def gastomensual_create(request):
    return GastoMensualCreateView.as_view()(request)

def gastomensual_update(request, pk):
    return GastoMensualUpdateView.as_view()(request, pk=pk)

def gastomensual_delete(request, pk):
    return GastoMensualDeleteView.as_view()(request, pk=pk)