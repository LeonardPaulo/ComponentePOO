# applications/doctor/views/cargo.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Cargo
from applications.doctor.forms.cargo import CargoForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para Cargo
class CargoListView(PermissionMixin, ListViewMixin, ListView):
    model = Cargo
    template_name = 'doctor/cargo/list.html'
    context_object_name = 'cargos'
    paginate_by = 2
    permission_required = 'view_cargo'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombre__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Cargos'
        context['title1'] = 'Cargos'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class CargoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'doctor/cargo/form.html'
    success_url = reverse_lazy('doctor:cargo_list')
    permission_required = 'add_cargo'

    def form_valid(self, form):
        messages.success(self.request, 'Cargo creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el cargo. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Cargo'
        context['title1'] = 'Cargos'
        return context

class CargoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'doctor/cargo/form.html'
    success_url = reverse_lazy('doctor:cargo_list')
    permission_required = 'change_cargo'

    def form_valid(self, form):
        messages.success(self.request, 'Cargo actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el cargo. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cargo'
        context['title1'] = 'Cargos'
        return context

class CargoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Cargo
    success_url = reverse_lazy('doctor:cargo_list')
    permission_required = 'delete_cargo'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Cargo eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el cargo: {e}')