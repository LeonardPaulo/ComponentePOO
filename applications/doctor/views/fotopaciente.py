from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from applications.core.models import FotoPaciente
from applications.doctor.forms.fotopaciente import FotoPacienteForm

@login_required
@permission_required('core.view_fotopaciente', raise_exception=True)
def fotopaciente_list(request):
    fotos = FotoPaciente.objects.select_related('paciente').all()
    query = request.GET.get('q')
    if query:
        fotos = fotos.filter(paciente__apellidos__icontains=query)
    paginator = Paginator(fotos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Listado de Fotos de Paciente',
        'title1': 'Fotos de Pacientes',
        'page_obj': page_obj,
        'permissions': {
            'add_fotopaciente': request.user.has_perm('core.add_fotopaciente'),
            'change_fotopaciente': request.user.has_perm('core.change_fotopaciente'),
            'delete_fotopaciente': request.user.has_perm('core.delete_fotopaciente'),
            'view_fotopaciente': request.user.has_perm('core.view_fotopaciente'),
        }
    }
    return render(request, 'doctor/fotos_paciente/list.html', context)

@login_required
@permission_required('core.add_fotopaciente', raise_exception=True)
def fotopaciente_create(request):
    if request.method == 'POST':
        form = FotoPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto agregada exitosamente.')
            return redirect('doctor:fotopaciente_list')
        else:
            messages.error(request, 'Error al agregar la foto. Revisa los datos.')
    else:
        form = FotoPacienteForm()
    context = {
        'title': 'Agregar Foto de Paciente',
        'form': form,
        'action_url': 'doctor:fotopaciente_create',
        'btn_text': 'Guardar Foto',
        'is_update': False,
    }
    return render(request, 'doctor/fotos_paciente/form.html', context)

@login_required
@permission_required('core.change_fotopaciente', raise_exception=True)
def fotopaciente_update(request, pk):
    foto = get_object_or_404(FotoPaciente, pk=pk)
    if request.method == 'POST':
        form = FotoPacienteForm(request.POST, request.FILES, instance=foto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto actualizada exitosamente.')
            return redirect('doctor:fotopaciente_list')
        else:
            messages.error(request, 'Error al actualizar la foto. Revisa los datos.')
    else:
        form = FotoPacienteForm(instance=foto)
    context = {
        'title': 'Editar Foto de Paciente',
        'form': form,
        'action_url': 'doctor:fotopaciente_update',
        'btn_text': 'Actualizar Foto',
        'is_update': True,
        'foto': foto,
    }
    return render(request, 'doctor/fotos_paciente/form.html', context)

@login_required
@permission_required('core.delete_fotopaciente', raise_exception=True)
def fotopaciente_delete(request, pk):
    foto = get_object_or_404(FotoPaciente, pk=pk)
    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Foto eliminada exitosamente.')
        return redirect('doctor:fotopaciente_list')
    messages.error(request, 'Método no permitido para eliminar la foto.')
    return redirect('doctor:fotopaciente_list')