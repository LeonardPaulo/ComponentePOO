from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import FotoPaciente
from applications.doctor.forms.fotopaciente import FotoPacienteForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

class FotoPacienteListView(PermissionMixin, ListViewMixin, ListView):
    model = FotoPaciente
    template_name = 'doctor/fotos_paciente/list.html'
    context_object_name = 'fotos'
    paginate_by = 2
    permission_required = 'view_fotopaciente'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(paciente__apellidos__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).select_related('paciente').order_by('-fecha_subida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fotos de Paciente'
        context['title1'] = 'Fotos de Pacientes'
        context['search_query'] = self.request.GET.get('q', '')
        context['permissions'] = {
            'add_fotopaciente': self.request.user.has_perm('core.add_fotopaciente'),
            'change_fotopaciente': self.request.user.has_perm('core.change_fotopaciente'),
            'delete_fotopaciente': self.request.user.has_perm('core.delete_fotopaciente'),
            'view_fotopaciente': self.request.user.has_perm('core.view_fotopaciente'),
        }
        return context

class FotoPacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = FotoPaciente
    form_class = FotoPacienteForm
    template_name = 'doctor/fotos_paciente/form.html'
    success_url = reverse_lazy('doctor:fotopaciente_list')
    permission_required = 'add_fotopaciente'

    def form_valid(self, form):
        messages.success(self.request, 'Foto agregada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al agregar la foto. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Foto de Paciente'
        context['btn_text'] = 'Guardar Foto'
        context['is_update'] = False
        context['action_url'] = 'doctor:fotopaciente_create'  # Agregamos el action_url
        return context

class FotoPacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = FotoPaciente
    form_class = FotoPacienteForm
    template_name = 'doctor/fotos_paciente/form.html'
    success_url = reverse_lazy('doctor:fotopaciente_list')
    permission_required = 'change_fotopaciente'

    def form_valid(self, form):
        messages.success(self.request, 'Foto actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar la foto. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Foto de Paciente'
        context['btn_text'] = 'Actualizar Foto'
        context['is_update'] = True
        context['foto'] = self.object
        context['action_url'] = 'doctor:fotopaciente_update'  # Agregamos el action_url
        return context

class FotoPacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = FotoPaciente
    success_url = reverse_lazy('doctor:fotopaciente_list')
    permission_required = 'delete_fotopaciente'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Foto eliminada exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar la foto: {e}')
        return redirect(self.success_url)

# Funciones wrapper para compatibilidad con URLs existentes
def fotopaciente_list(request):
    return FotoPacienteListView.as_view()(request)

def fotopaciente_create(request):
    return FotoPacienteCreateView.as_view()(request)

def fotopaciente_update(request, pk):
    return FotoPacienteUpdateView.as_view()(request, pk=pk)

def fotopaciente_delete(request, pk):
    return FotoPacienteDeleteView.as_view()(request, pk=pk)