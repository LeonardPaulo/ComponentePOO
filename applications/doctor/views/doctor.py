# applications/doctor/views/doctor.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Doctor, Especialidad
from applications.doctor.forms.doctor import DoctorForm

class DoctorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctor/doctor/list.html' 
    context_object_name = 'doctores'
    paginate_by = 10
    permission_required = 'core.view_doctor'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(nombres__icontains=search_query) |
                Q(apellidos__icontains=search_query) |
                Q(ruc__icontains=search_query) |
                Q(especialidad__nombre__icontains=search_query)
            ).distinct()
        queryset = queryset.order_by('apellidos', 'nombres')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Doctores'
        context['title1'] = 'Doctores'
        context['search_query'] = self.request.GET.get('q', '')
        context['permissions'] = self.get_permissions_context(self.request)
        return context

    def get_permissions_context(self, request):
        return {
            'add_doctor': request.user.has_perm('core.add_doctor'),
            'change_doctor': request.user.has_perm('core.change_doctor'),
            'delete_doctor': request.user.has_perm('core.delete_doctor'),
        }

class DoctorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/doctor/form.html'
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'core.add_doctor'

    def form_valid(self, form):
        messages.success(self.request, 'Doctor creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el doctor. Revisa los datos.')
        print("Errores del formulario (DoctorCreateView):", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Doctor'
        context['title1'] = 'Doctores'
        return context

class DoctorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/doctor/form.html'
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'core.change_doctor'

    def form_valid(self, form):
        messages.success(self.request, 'Doctor actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el doctor. Revisa los datos.')
        print("Errores del formulario (DoctorUpdateView):", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Doctor'
        context['title1'] = 'Doctores'
        return context

class DoctorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'core.delete_doctor'
    # ¡¡IMPORTANTE: NO DEBE HABER template_name AQUÍ!!
    # Si DeleteView recibe un GET y no tiene template_name, intentará buscar uno por defecto,
    # lo cual causaba el TemplateDoesNotExist.
    # Al sobrescribir `post` y no tener `template_name`, el GET seguirá buscando una plantilla,
    # pero el POST se manejará correctamente. La clave es que el botón de eliminar envíe POST.

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(self.request, 'Doctor eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el doctor: {e}')
            print(f"Error al eliminar doctor: {e}")
        return redirect(self.success_url)