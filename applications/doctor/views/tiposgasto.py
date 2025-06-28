from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator

from applications.core.models import TipoGasto
from applications.doctor.forms.tipogasto import TipoGastoForm

# Vistas para TipoGasto (CRUD)
@login_required
@permission_required('core.view_tipogasto', raise_exception=True)
def tipogasto_list(request):
    tipos_gasto = TipoGasto.objects.all()
    query = request.GET.get('q')
    if query:
        tipos_gasto = tipos_gasto.filter(nombre__icontains=query)

    paginator = Paginator(tipos_gasto, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Listado de Tipos de Gasto',
        'title1': 'Tipos de Gasto',
        'page_obj': page_obj,
        'permissions': {
            'add_tipogasto': request.user.has_perm('core.add_tipogasto'),
            'change_tipogasto': request.user.has_perm('core.change_tipogasto'),
            'delete_tipogasto': request.user.has_perm('core.delete_tipogasto'),
            'view_tipogasto': request.user.has_perm('core.view_tipogasto'),
        }
    }
    return render(request, 'doctor/tipos_gasto/list.html', context)

@login_required
@permission_required('core.add_tipogasto', raise_exception=True)
def tipogasto_create(request):
    if request.method == 'POST':
        form = TipoGastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de gasto agregado exitosamente.')
            return redirect('doctor:tipogasto_list')
        else:
            messages.error(request, 'Error al agregar el tipo de gasto. Por favor, revisa los datos.')
    else:
        form = TipoGastoForm()

    context = {
        'title': 'Agregar Tipo de Gasto',
        'form': form,
        'action_url': 'doctor:tipogasto_create',
        'btn_text': 'Guardar Tipo de Gasto',
        'is_update': False,
    }
    return render(request, 'doctor/tipos_gasto/form.html', context)

@login_required
@permission_required('core.change_tipogasto', raise_exception=True)
def tipogasto_update(request, pk):
    tipo_gasto = get_object_or_404(TipoGasto, pk=pk)
    if request.method == 'POST':
        form = TipoGastoForm(request.POST, instance=tipo_gasto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de gasto actualizado exitosamente.')
            return redirect('doctor:tipogasto_list')
        else:
            messages.error(request, 'Error al actualizar el tipo de gasto. Por favor, revisa los datos.')
    else:
        form = TipoGastoForm(instance=tipo_gasto)

    context = {
        'title': 'Editar Tipo de Gasto',
        'form': form,
        'action_url': 'doctor:tipogasto_update',
        'btn_text': 'Actualizar Tipo de Gasto',
        'is_update': True,
        'tipo_gasto': tipo_gasto,
    }
    return render(request, 'doctor/tipos_gasto/form.html', context)

@login_required
@permission_required('core.delete_tipogasto', raise_exception=True)
def tipogasto_delete(request, pk):
    tipo_gasto = get_object_or_404(TipoGasto, pk=pk)
    if request.method == 'POST':
        tipo_gasto.delete()
        messages.success(request, 'Tipo de gasto eliminado exitosamente.')
        return redirect('doctor:tipogasto_list')
    messages.error(request, 'Método no permitido para eliminar el tipo de gasto.')
    return redirect('doctor:tipogasto_list')