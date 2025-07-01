# applications/doctor/views/cargo.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Cargo # Asegúrate de importar el modelo Cargo
from applications.doctor.forms.cargo import CargoForm # Asegúrate de importar el formulario

# Vistas para Cargo
class CargoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cargo
    template_name = 'doctor/cargo/list.html'
    context_object_name = 'cargos' # Nombre de la variable en el template
    paginate_by = 10 
    permission_required = 'core.view_cargo' # Permiso requerido para ver la lista

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')

        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(descripcion__icontains=search_query)
            ).distinct()
        
        queryset = queryset.order_by('nombre')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Cargos'
        context['title1'] = 'Cargos'
        context['search_query'] = self.request.GET.get('q', '')
        context['permissions'] = self.get_permissions_context(self.request)
        return context

    def get_permissions_context(self, request):
        return {
            'add_cargo': request.user.has_perm('core.add_cargo'),
            'change_cargo': request.user.has_perm('core.change_cargo'),
            'delete_cargo': request.user.has_perm('core.delete_cargo'),
        }

class CargoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'doctor/cargo/form.html'
    success_url = reverse_lazy('doctor:cargo_list')
    permission_required = 'core.add_cargo'

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

class CargoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'doctor/cargo/form.html'
    success_url = reverse_lazy('doctor:cargo_list')
    permission_required = 'core.change_cargo'

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

class CargoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cargo
    success_url = reverse_lazy('doctor:cargo_list')
    permission_required = 'core.delete_cargo'

    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Cargo eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el cargo: {e}')
        return redirect(self.success_url)