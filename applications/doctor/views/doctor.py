# applications/doctor/views/doctor.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import Doctor, Especialidad
from applications.doctor.forms.doctor import DoctorForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

class DoctorListView(PermissionMixin, ListViewMixin, ListView):
    model = Doctor
    template_name = 'doctor/doctor/list.html' 
    context_object_name = 'doctores'
    paginate_by = 10
    permission_required = 'view_doctor'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(nombres__icontains=search_query), Q.OR)
            self.query.add(Q(apellidos__icontains=search_query), Q.OR)
            self.query.add(Q(ruc__icontains=search_query), Q.OR)
            self.query.add(Q(especialidad__nombre__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Doctores'
        context['title1'] = 'Doctores'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class DoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/doctor/form.html'
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'add_doctor'

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

class DoctorUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/doctor/form.html'
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'change_doctor'

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

class DoctorDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctor:doctor_list')
    permission_required = 'delete_doctor'

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(self.request, 'Doctor eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el doctor: {e}')
            print(f"Error al eliminar doctor: {e}")
        return