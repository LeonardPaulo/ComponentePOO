# applications/doctor/views/tiposangre.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator

# CORREGIDO: 'aplicaciones' cambiado a 'applications'
from applications.core.models import TipoSangre

# CORREGIDO: La ruta del formulario debe ser absoluta desde la raíz del proyecto
from applications.doctor.forms.tiposangre import TipoSangreForm 


# Vistas para TipoSangre (CRUD)
@login_required
@permission_required('core.view_tiposangre', raise_exception=True)
def tiposangre_list(request):
    tipos_sangre = TipoSangre.objects.all()
    query = request.GET.get('q')
    if query:
        tipos_sangre = tipos_sangre.filter(tipo__icontains=query)

    paginator = Paginator(tipos_sangre, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Listado de Tipos de Sangre',
        'title1': 'Tipos de Sangre',
        'page_obj': page_obj,
        'permissions': {
            'add_tiposangre': request.user.has_perm('core.add_tiposangre'),
            'change_tiposangre': request.user.has_perm('core.change_tiposangre'),
            'delete_tiposangre': request.user.has_perm('core.delete_tiposangre'),
            'view_tiposangre': request.user.has_perm('core.view_tiposangre'),
        }
    }
    return render(request, 'doctor/tipos_sangre/list.html', context)

@login_required
@permission_required('core.add_tiposangre', raise_exception=True)
def tiposangre_create(request):
    if request.method == 'POST':
        form = TipoSangreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de sangre agregado exitosamente.')
            return redirect('doctor:tiposangre_list')
        else:
            messages.error(request, 'Error al agregar el tipo de sangre. Por favor, revisa los datos.')
    else:
        form = TipoSangreForm()

    context = {
        'title': 'Agregar Tipo de Sangre',
        'form': form,
        'action_url': 'doctor:tiposangre_create',
        'btn_text': 'Guardar Tipo de Sangre',
        'is_update': False,
    }
    return render(request, 'doctor/tipos_sangre/form.html', context)

@login_required
@permission_required('core.change_tiposangre', raise_exception=True)
def tiposangre_update(request, pk):
    tipo_sangre = get_object_or_404(TipoSangre, pk=pk)
    if request.method == 'POST':
        form = TipoSangreForm(request.POST, instance=tipo_sangre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de sangre actualizado exitosamente.')
            return redirect('doctor:tiposangre_list')
        else:
            messages.error(request, 'Error al actualizar el tipo de sangre. Por favor, revisa los datos.')
    else:
        form = TipoSangreForm(instance=tipo_sangre)

    context = {
        'title': 'Editar Tipo de Sangre',
        'form': form,
        'action_url': 'doctor:tiposangre_update',
        'btn_text': 'Actualizar Tipo de Sangre',
        'is_update': True,
        'tipo_sangre': tipo_sangre, # <--- ¡ESTA ES LA LÍNEA CRÍTICA AÑADIDA!
    }
    return render(request, 'doctor/tipos_sangre/form.html', context)

@login_required
@permission_required('core.delete_tiposangre', raise_exception=True)
def tiposangre_delete(request, pk):
    tipo_sangre = get_object_or_404(TipoSangre, pk=pk)
    if request.method == 'POST':
        tipo_sangre.delete()
        messages.success(request, 'Tipo de sangre eliminado exitosamente.')
        return redirect('doctor:tiposangre_list')
    messages.error(request, 'Método no permitido para eliminar el tipo de sangre.')
    return redirect('doctor:tiposangre_list')