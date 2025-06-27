import json
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from applications.core.models import Paciente
from applications.doctor.forms.paciente import PacienteForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

class PacienteListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/pacientes/list.html'
    model = Paciente
    context_object_name = 'pacientes'
    permission_required = 'view_paciente'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(Q(nombres__icontains=q), Q.OR)
            self.query.add(Q(apellidos__icontains=q), Q.OR)
            self.query.add(Q(cedula_ecuatoriana__icontains=q), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:paciente_create')
        return context


class PacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    template_name = 'doctor/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('doctor:paciente_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Paciente'
        context['back_url'] = self.success_url
        return context


class PacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    template_name = 'doctor/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('doctor:paciente_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        return context


class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar al paciente: {self.object}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        paciente_nombre = self.object
        response = super().form_valid(form)
        messages.success(self.request, f"Paciente {paciente_nombre} eliminado correctamente.")
        return response
