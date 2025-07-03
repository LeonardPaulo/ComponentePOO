# applications/doctor/views/tiposangre.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect

from applications.core.models import TipoSangre
from applications.doctor.forms.tiposangre import TipoSangreForm
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)

# Vistas para TipoSangre
class TipoSangreListView(PermissionMixin, ListViewMixin, ListView):
    model = TipoSangre
    template_name = 'doctor/tipos_sangre/list.html'
    context_object_name = 'tipos_sangre'
    paginate_by = 2
    permission_required = 'view_tiposangre'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            self.query.add(Q(tipo__icontains=search_query), Q.OR)
            self.query.add(Q(descripcion__icontains=search_query), Q.OR)
        return self.model.objects.filter(self.query).order_by('tipo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Tipos de Sangre'
        context['title1'] = 'Tipos de Sangre'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class TipoSangreCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    form_class = TipoSangreForm
    template_name = 'doctor/tipos_sangre/form.html'
    success_url = reverse_lazy('doctor:tiposangre_list')
    permission_required = 'add_tiposangre'

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de sangre creado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el tipo de sangre. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Nuevo Tipo de Sangre'
        context['title1'] = 'Tipos de Sangre'
        context['action_url'] = 'doctor:tiposangre_create'
        context['btn_text'] = 'Guardar Tipo de Sangre'
        context['is_update'] = False
        return context

class TipoSangreUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    form_class = TipoSangreForm
    template_name = 'doctor/tipos_sangre/form.html'
    success_url = reverse_lazy('doctor:tiposangre_list')
    permission_required = 'change_tiposangre'

    def form_valid(self, form):
        messages.success(self.request, 'Tipo de sangre actualizado exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el tipo de sangre. Revisa los datos.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Sangre'
        context['title1'] = f'Editar Tipo de Sangre: {self.object.tipo}'
        context['action_url'] = 'doctor:tiposangre_update'
        context['btn_text'] = 'Actualizar Tipo de Sangre'
        context['is_update'] = True
        context['tiposangre'] = self.object
        return context

class TipoSangreDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    success_url = reverse_lazy('doctor:tiposangre_list')
    permission_required = 'delete_tiposangre'

    def post(self, request, *args, **kwargs):
        try:
            tiposangre_tipo = self.get_object().tipo
            self.get_object().delete()
            messages.success(self.request, f'Tipo de sangre "{tiposangre_tipo}" eliminado exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al eliminar el tipo de sangre: {e}')
        return redirect(self.success_url)

# Funciones wrapper para mantener compatibilidad con URLs existentes
def tiposangre_list(request):
    return TipoSangreListView.as_view()(request)

def tiposangre_create(request):
    return TipoSangreCreateView.as_view()(request)

def tiposangre_update(request, pk):
    return TipoSangreUpdateView.as_view()(request, pk=pk)

def tiposangre_delete(request, pk):
    return TipoSangreDeleteView.as_view()(request, pk=pk)