# applications/doctor/views/especialidad.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # Para seguridad
from applications.core.models import Especialidad
from applications.doctor.forms.especialidad import EspecialidadForm

# --- Vistas para el modelo Especialidad ---

class EspecialidadListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Especialidad
    template_name = "doctor/especialidad/list.html"
    context_object_name = "especialidades"
    paginate_by = 2 # Opcional: para paginación
    permission_required = 'core.view_especialidad' # Permiso necesario para ver

class EspecialidadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "doctor/especialidad/form.html"
    success_url = reverse_lazy('doctor:especialidad_list')
    permission_required = 'core.add_especialidad' # Permiso necesario para crear

class EspecialidadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "doctor/especialidad/form.html"
    success_url = reverse_lazy('doctor:especialidad_list')
    permission_required = 'core.change_especialidad' # Permiso necesario para editar

class EspecialidadDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Especialidad
    template_name = "doctor/especialidad/form.html"
    success_url = reverse_lazy('doctor:especialidad_list')
    permission_required = 'core.delete_especialidad' # Permiso necesario para eliminar