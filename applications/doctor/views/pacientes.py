import json
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from applications.core.models import Paciente, FotoPaciente
from applications.doctor.forms.paciente import PacienteForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
import shutil
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os

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
        # Agregar datos de fotos para JavaScript
        context['fotos_data'] = self._get_fotos_json()
        return context

    def _get_fotos_json(self):
        """Genera JSON con datos de fotos para JavaScript"""
        fotos = FotoPaciente.objects.filter(imagen__isnull=False).select_related('paciente')
        fotos_data = {}
        for foto in fotos:
            fotos_data[str(foto.pk)] = {
                'url': foto.imagen.url,
                'paciente': str(foto.paciente),
                'descripcion': foto.descripcion or '',
                'fecha': foto.fecha_subida.strftime('%d/%m/%Y')
            }
        return json.dumps(fotos_data)

    def form_valid(self, form):
        # IMPORTANTE: Asegurar que el paciente se cree como activo
        form.instance.activo = True
    
        # Manejar selección de foto existente
        foto_existente_id = form.cleaned_data.get('foto_existente')
        foto_nueva = form.cleaned_data.get('foto')
    
        # Si se seleccionó una foto existente
        if foto_existente_id:
            # Asignar la referencia a la foto existente
            form.instance.foto_referencia = foto_existente_id
            # Limpiar el campo foto directa para evitar conflictos
            form.instance.foto = None
        elif foto_nueva:
            # Si se sube una foto nueva, limpiar la referencia
            form.instance.foto_referencia = None
            # La foto nueva se maneja automáticamente por Django
    
        response = super().form_valid(form)
        messages.success(self.request, f'Paciente {self.object.nombres} {self.object.apellidos} creado exitosamente.')
        return response


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
        # Agregar datos de fotos para JavaScript
        context['fotos_data'] = self._get_fotos_json()
        return context

    def _get_fotos_json(self):
        """Genera JSON con datos de fotos para JavaScript"""
        fotos = FotoPaciente.objects.filter(imagen__isnull=False).select_related('paciente')
        fotos_data = {}
        for foto in fotos:
            fotos_data[str(foto.pk)] = {
                'url': foto.imagen.url,
                'paciente': str(foto.paciente),
                'descripcion': foto.descripcion or '',
                'fecha': foto.fecha_subida.strftime('%d/%m/%Y')
            }
        return json.dumps(fotos_data)

    def form_valid(self, form):
        # Manejar selección de foto existente
        foto_existente_id = form.cleaned_data.get('foto_existente')
        foto_nueva = form.cleaned_data.get('foto')
    
        # Si se seleccionó una foto existente
        if foto_existente_id:
            # Asignar la referencia a la foto existente
            form.instance.foto_referencia = foto_existente_id
            # Limpiar el campo foto directa para evitar conflictos
            form.instance.foto = None
        elif foto_nueva:
            # Si se sube una foto nueva, limpiar la referencia
            form.instance.foto_referencia = None
            # La foto nueva se maneja automáticamente por Django
    
        response = super().form_valid(form)
        messages.success(self.request, f'Paciente {self.object.nombres} {self.object.apellidos} actualizado exitosamente.')
        return response


class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'doctor/pacientes/delete.html'
    success_url = reverse_lazy('doctor:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Paciente'
        context['back_url'] = self.success_url
        return context