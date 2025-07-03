from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.doctor.models import ServiciosAdicionales
from applications.doctor.forms.serviciosadicionales import ServiciosAdicionalesForm
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class ServiciosAdicionalesListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/serviciosadicionales/list.html'
    model = ServiciosAdicionales
    context_object_name = 'servicios'
    permission_required = 'view_serviciosadicionales'
    paginate_by = 2

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(
                Q(nombre_servicio__icontains=q) |
                Q(descripcion__icontains=q)
            )
        return queryset.order_by('nombre_servicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:serviciosadicionales_create')
        return context

class ServiciosAdicionalesCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ServiciosAdicionales
    template_name = 'doctor/serviciosadicionales/form.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('doctor:serviciosadicionales_list')
    permission_required = 'add_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Servicio Adicional'
        context['back_url'] = self.success_url
        context['action'] = 'Crear'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Servicio "{self.object.nombre_servicio}" registrado exitosamente.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar el servicio adicional.")
        return super().form_invalid(form)

class ServiciosAdicionalesUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ServiciosAdicionales
    template_name = 'doctor/serviciosadicionales/form.html'
    form_class = ServiciosAdicionalesForm
    success_url = reverse_lazy('doctor:serviciosadicionales_list')
    permission_required = 'change_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Servicio Adicional'
        context['back_url'] = self.success_url
        context['action'] = 'Actualizar'
        context['servicio'] = self.object
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Servicio "{self.object.nombre_servicio}" actualizado exitosamente.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el servicio adicional.")
        return super().form_invalid(form)

class ServiciosAdicionalesDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:serviciosadicionales_list')
    permission_required = 'delete_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Servicio Adicional'
        context['description'] = f"¿Desea eliminar el servicio adicional '{self.object.nombre_servicio}'?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        nombre_servicio = self.object.nombre_servicio
        response = super().form_valid(form)
        messages.success(self.request, f'Servicio "{nombre_servicio}" eliminado exitosamente.')
        return response

# Funciones wrapper para mantener compatibilidad con URLs existentes
def serviciosadicionales_list(request):
    return ServiciosAdicionalesListView.as_view()(request)

def serviciosadicionales_create(request):
    return ServiciosAdicionalesCreateView.as_view()(request)

def serviciosadicionales_update(request, pk):
    return ServiciosAdicionalesUpdateView.as_view()(request, pk=pk)

def serviciosadicionales_delete(request, pk):
    return ServiciosAdicionalesDeleteView.as_view()(request, pk=pk)