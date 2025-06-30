from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from applications.doctor.models import CitaMedica
from applications.doctor.forms.cita_medica import CitaMedicaForm  # Debes tener este formulario
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class CitaMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/cita_medica/list.html'
    model = CitaMedica
    context_object_name = 'citas'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(paciente__nombres__icontains=q)
        return queryset.order_by('-fecha', '-hora_cita')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_create')
        return context


class CitaMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:cita_list')
    permission_required = 'add_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Cita Médica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Cita médica registrada exitosamente para {self.object.paciente}")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar la cita médica.")
        return super().form_invalid(form)


class CitaMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:cita_list')
    permission_required = 'change_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Cita Médica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Cita médica actualizada exitosamente para {self.object.paciente}")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la cita médica.")
        return super().form_invalid(form)


class CitaMedicaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:cita_list')
    permission_required = 'delete_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Cita Médica'
        context['description'] = f"¿Desea eliminar la cita de: {self.object.paciente}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        paciente_nombre = self.object.paciente
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar la cita de {paciente_nombre}.")
        return response