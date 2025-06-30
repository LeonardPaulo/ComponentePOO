from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from applications.doctor.models import HorarioAtencion
from applications.doctor.forms.horario_atencion import HorarioAtencionForm
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class HorarioAtencionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/horario_atencion/list.html'
    model = HorarioAtencion
    context_object_name = 'horarios'
    permission_required = 'view_horarioatencion'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(dia_semana__icontains=q)
        return queryset.order_by('dia_semana', 'hora_inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:horario_atencion_create')
        return context

class HorarioAtencionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'add_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Horario de Atención'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Horario de atención registrado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar el horario de atención.")
        return super().form_invalid(form)

class HorarioAtencionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'change_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Horario de Atención'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Horario de atención actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el horario de atención.")
        return super().form_invalid(form)

class HorarioAtencionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = HorarioAtencion
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'delete_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Horario de Atención'
        context['description'] = f"¿Desea eliminar el horario de atención para {self.object.dia_semana}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Horario de atención eliminado exitosamente.")
        return response