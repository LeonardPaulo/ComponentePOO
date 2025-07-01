# applications/doctor/views/medicamento.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q # Importa Q para la búsqueda avanzada
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages # Para mensajes flash
from django.shortcuts import redirect # Necesario para la redirección en DeleteView

# Asegúrate de importar los modelos y el formulario correctamente
from applications.core.models import Medicamento, TipoMedicamento, MarcaMedicamento 
from applications.doctor.forms.medicamento import MedicamentoForm

# Vistas para Medicamento
class MedicamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Medicamento
    template_name = 'doctor/medicamento/list.html'
    context_object_name = 'medicamentos' # Nombre de la variable en el template
    paginate_by = 10 # Paginación, muestra 10 elementos por página
    permission_required = 'core.view_medicamento' # Permiso requerido para ver la lista

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')

        if search_query:
            # Búsqueda insensible a mayúsculas/minúsculas en varios campos, incluyendo FKs
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(descripcion__icontains=search_query) |
                Q(concentracion__icontains=search_query) |
                Q(tipo__nombre__icontains=search_query) | # Búsqueda por nombre del Tipo de Medicamento
                Q(marca_medicamento__nombre__icontains=search_query) # Búsqueda por nombre de la Marca de Medicamento
            ).distinct() # Usa distinct() para evitar duplicados si un elemento coincide con múltiples Q
        
        queryset = queryset.order_by('nombre') # Ordena por nombre por defecto
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Medicamentos'
        context['title1'] = 'Medicamentos' # Título secundario/breadcrumbs
        context['search_query'] = self.request.GET.get('q', '') # Pasa la query de búsqueda al template
        context['permissions'] = self.get_permissions_context(self.request) # Pasa permisos al template
        return context

    def get_permissions_context(self, request):
        # Ayuda para pasar los permisos al contexto del template para control de botones
        return {
            'add_medicamento': request.user.has_perm('core.add_medicamento'),
            'change_medicamento': request.user.has_perm('core.change_medicamento'),
            'delete_medicamento': request.user.has_perm('core.delete_medicamento'),
        }

class MedicamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'doctor/medicamento/form.html' # Template para el formulario de creación
    success_url = reverse_lazy('doctor:medicamento_list') # Redirección tras éxito
    permission_required = 'core.add_medicamento' # Permiso requerido para crear

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el medicamento. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Medicamento'
        context['title1'] = 'Medicamentos'
        return context

class MedicamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'doctor/medicamento/form.html' # Template para el formulario de edición
    success_url = reverse_lazy('doctor:medicamento_list') # Redirección tras éxito
    permission_required = 'core.change_medicamento' # Permiso requerido para editar

    def form_valid(self, form):
        messages.success(self.request, 'Medicamento actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el medicamento. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Medicamento'
        context['title1'] = 'Medicamentos'
        return context

class MedicamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Medicamento
    success_url = reverse_lazy('doctor:medicamento_list') # Redirección tras éxito
    permission_required = 'core.delete_medicamento' # Permiso requerido para eliminar

    # Sobreescribimos el método post para manejar la eliminación y los mensajes flash
    def post(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            messages.success(self.request, 'Medicamento eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el medicamento: {e}')
        return redirect(self.success_url)

    # Si quisieras un template de confirmación separado, lo descomentarías y ajustarías:
    # template_name = 'doctor/medicamento/confirm_delete.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Confirmar Eliminación'
    #     context['title1'] = 'Medicamentos'
    #     return context