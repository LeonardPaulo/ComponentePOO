# applications/doctor/views/marcamedicamento.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
# Eliminamos la importación de reverse_lazy ya que no usaremos Generic Views para Delete

from applications.core.models import MarcaMedicamento
from ..forms.marcamedicamento import MarcaMedicamentoForm

class MarcaMedicamentoListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'core.view_marcamedicamento'
    template_name = 'doctor/marcamedicamento/list.html'

    def get(self, request):
        search_query = request.GET.get('q', '')
        marcas_medicamento = MarcaMedicamento.objects.all()

        if search_query:
            marcas_medicamento = marcas_medicamento.filter(
                Q(nombre__icontains=search_query) |
                Q(descripcion__icontains=search_query)
            )

        paginator = Paginator(marcas_medicamento, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'title': 'Lista de Marcas de Medicamentos',
            'title1': 'Marcas de Medicamentos',
            'page_obj': page_obj,
            'search_query': search_query,
            'permissions': self.get_permissions_context(request),
        }
        return render(request, self.template_name, context)
    
    def get_permissions_context(self, request):
        return {
            'add_marcamedicamento': request.user.has_perm('core.add_marcamedicamento'),
            'change_marcamedicamento': request.user.has_perm('core.change_marcamedicamento'),
            'delete_marcamedicamento': request.user.has_perm('core.delete_marcamedicamento'),
        }

class MarcaMedicamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'core.add_marcamedicamento'
    template_name = 'doctor/marcamedicamento/form.html'

    def get(self, request):
        form = MarcaMedicamentoForm()
        context = {
            'title': 'Crear Marca de Medicamento',
            'title1': 'Crear Nueva Marca de Medicamento',
            'form': form,
            'permissions': self.get_permissions_context(request),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MarcaMedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca de Medicamento creada exitosamente.')
            return redirect('doctor:marcasmedicamento_list')
        else:
            messages.error(request, 'Hubo un error al crear la Marca de Medicamento. Por favor, revisa los datos.')
            context = {
                'title': 'Crear Marca de Medicamento',
                'title1': 'Crear Nueva Marca de Medicamento',
                'form': form,
                'permissions': self.get_permissions_context(request),
            }
            return render(request, self.template_name, context)

    def get_permissions_context(self, request):
        return {
            'add_marcamedicamento': request.user.has_perm('core.add_marcamedicamento'),
            'change_marcamedicamento': request.user.has_perm('core.change_marcamedicamento'),
            'delete_marcamedicamento': request.user.has_perm('core.delete_marcamedicamento'),
        }

class MarcaMedicamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'core.change_marcamedicamento'
    template_name = 'doctor/marcamedicamento/form.html'

    def get(self, request, pk):
        marca_medicamento = get_object_or_404(MarcaMedicamento, pk=pk)
        form = MarcaMedicamentoForm(instance=marca_medicamento)
        context = {
            'title': 'Editar Marca de Medicamento',
            'title1': f'Editar Marca de Medicamento: {marca_medicamento.nombre}',
            'form': form,
            'permissions': self.get_permissions_context(request),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        marca_medicamento = get_object_or_404(MarcaMedicamento, pk=pk)
        form = MarcaMedicamentoForm(request.POST, instance=marca_medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca de Medicamento actualizada exitosamente.')
            return redirect('doctor:marcasmedicamento_list')
        else:
            messages.error(request, 'Hubo un error al actualizar la Marca de Medicamento. Por favor, revisa los datos.')
            context = {
                'title': 'Editar Marca de Medicamento',
                'title1': f'Editar Marca de Medicamento: {marca_medicamento.nombre}',
                'form': form,
                'permissions': self.get_permissions_context(request),
            }
            return render(request, self.template_name, context)

    def get_permissions_context(self, request):
        return {
            'add_marcamedicamento': request.user.has_perm('core.add_marcamedicamento'),
            'change_marcamedicamento': request.user.has_perm('core.change_marcamedicamento'),
            'delete_marcamedicamento': request.user.has_perm('core.delete_marcamedicamento'),
        }

# Vista de Eliminación directa (sin plantilla de confirmación dedicada)
class MarcaMedicamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'core.delete_marcamedicamento'

    def post(self, request, pk): # Cambiamos a POST para una eliminación segura
        marca_medicamento = get_object_or_404(MarcaMedicamento, pk=pk)
        try:
            marca_medicamento.delete()
            messages.success(request, f'Marca "{marca_medicamento.nombre}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la marca "{marca_medicamento.nombre}": {e}')
        
        return redirect('doctor:marcasmedicamento_list')

    # No necesitamos un método get aquí porque no hay una página de confirmación.
    # La eliminación se activará vía POST desde el list.html.