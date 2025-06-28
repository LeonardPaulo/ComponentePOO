# applications/doctor/views/tipomedicamento.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import TipoMedicamento
from applications.doctor.forms.tipomedicamento import TipoMedicamentoForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

# Vistas para TipoMedicamento
class TipoMedicamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TipoMedicamento
    template_name = 'doctor/tipomedicamento/list.html'
    context_object_name = 'tipos_medicamento' # Cambiado para ser más descriptivo
    paginate_by = 10
    permission_required = ('core.view_tipomedicamento',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Medicamentos'
        context['title1'] = 'Tipos de Medicamentos'
        # Añadir permisos al contexto
        user_permissions = self.request.user.get_all_permissions()
        context['permissions'] = {
            'add_tipomedicamento': 'core.add_tipomedicamento' in user_permissions,
            'change_tipomedicamento': 'core.change_tipomedicamento' in user_permissions,
            'delete_tipomedicamento': 'core.delete_tipomedicamento' in user_permissions,
            'view_tipomedicamento': 'core.view_tipomedicamento' in user_permissions,
        }
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(nombre__icontains=query) | \
                       queryset.filter(descripcion__icontains=query)
        return queryset

class TipoMedicamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'doctor/tipomedicamento/form.html'
    success_url = reverse_lazy('doctor:tiposmedicamento_list') # Asegúrate que esta URL sea correcta
    permission_required = ('core.add_tipomedicamento',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Tipo de Medicamento'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Medicamento creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el Tipo de Medicamento. Por favor, revisa los campos.')
        return super().form_invalid(form)

class TipoMedicamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TipoMedicamento
    form_class = TipoMedicamentoForm
    template_name = 'doctor/tipomedicamento/form.html'
    success_url = reverse_lazy('doctor:tiposmedicamento_list')
    permission_required = ('core.change_tipomedicamento',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Medicamento'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de Medicamento actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el Tipo de Medicamento. Por favor, revisa los campos.')
        return super().form_invalid(form)

class TipoMedicamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = TipoMedicamento
    template_name = 'doctor/tipomedicamento/delete.html' # Puedes usar un template específico o el modal genérico
    success_url = reverse_lazy('doctor:tiposmedicamento_list')
    permission_required = ('core.delete_tipomedicamento',)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Tipo de Medicamento eliminado exitosamente.')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Redirige para evitar que se acceda directamente a la vista de eliminación por GET
        messages.warning(self.request, 'Acceso no permitido directamente a la eliminación.')
        return redirect('doctor:tiposmedicamento_list')