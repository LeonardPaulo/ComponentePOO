from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator

from applications.core.models import GastoMensual
from applications.doctor.forms.gastomensual import GastoMensualForm

@login_required
@permission_required('core.view_gastomensual', raise_exception=True)
def gastomensual_list(request):
    gastos = GastoMensual.objects.select_related('tipo_gasto').all()
    query = request.GET.get('q')
    if query:
        gastos = gastos.filter(tipo_gasto__nombre__icontains=query)
    paginator = Paginator(gastos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Listado de Gastos Mensuales',
        'title1': 'Gastos Mensuales',
        'page_obj': page_obj,
        'permissions': {
            'add_gastomensual': request.user.has_perm('core.add_gastomensual'),
            'change_gastomensual': request.user.has_perm('core.change_gastomensual'),
            'delete_gastomensual': request.user.has_perm('core.delete_gastomensual'),
            'view_gastomensual': request.user.has_perm('core.view_gastomensual'),
        }
    }
    return render(request, 'doctor/gastos_mensuales/list.html', context)

@login_required
@permission_required('core.add_gastomensual', raise_exception=True)
def gastomensual_create(request):
    if request.method == 'POST':
        form = GastoMensualForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto mensual agregado exitosamente.')
            return redirect('doctor:gastomensual_list')
        else:
            messages.error(request, 'Error al agregar el gasto mensual. Por favor, revisa los datos.')
    else:
        form = GastoMensualForm()
    context = {
        'title': 'Agregar Gasto Mensual',
        'form': form,
        'action_url': 'doctor:gastomensual_create',
        'btn_text': 'Guardar Gasto Mensual',
        'is_update': False,
    }
    return render(request, 'doctor/gastos_mensuales/form.html', context)

@login_required
@permission_required('core.change_gastomensual', raise_exception=True)
def gastomensual_update(request, pk):
    gasto = get_object_or_404(GastoMensual, pk=pk)
    if request.method == 'POST':
        form = GastoMensualForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gasto mensual actualizado exitosamente.')
            return redirect('doctor:gastomensual_list')
        else:
            messages.error(request, 'Error al actualizar el gasto mensual. Por favor, revisa los datos.')
    else:
        form = GastoMensualForm(instance=gasto)
    context = {
        'title': 'Editar Gasto Mensual',
        'form': form,
        'action_url': 'doctor:gastomensual_update',
        'btn_text': 'Actualizar Gasto Mensual',
        'is_update': True,
        'gasto': gasto,
    }
    return render(request, 'doctor/gastos_mensuales/form.html', context)

@login_required
@permission_required('core.delete_gastomensual', raise_exception=True)
def gastomensual_delete(request, pk):
    gasto = get_object_or_404(GastoMensual, pk=pk)
    if request.method == 'POST':
        gasto.delete()
        messages.success(request, 'Gasto mensual eliminado exitosamente.')
        return redirect('doctor:gastomensual_list')
    messages.error(request, 'Método no permitido para eliminar el gasto mensual.')
    return redirect('doctor:gastomensual_list')