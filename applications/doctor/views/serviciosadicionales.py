from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from applications.doctor.models import ServiciosAdicionales
from applications.doctor.forms.serviciosadicionales import ServiciosAdicionalesForm

def serviciosadicionales_list(request):
    """Lista de servicios adicionales con búsqueda y paginación"""
    search = request.GET.get('search', '')
    servicios = ServiciosAdicionales.objects.all()
    
    if search:
        servicios = servicios.filter(
            Q(nombre_servicio__icontains=search) |
            Q(descripcion__icontains=search)
        )
    
    # Paginación
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'title': 'Servicios Adicionales',
    }
    return render(request, 'doctor/serviciosadicionales/list.html', context)

def serviciosadicionales_create(request):
    """Crear nuevo servicio adicional"""
    if request.method == 'POST':
        form = ServiciosAdicionalesForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            messages.success(request, f'Servicio "{servicio.nombre_servicio}" creado exitosamente.')
            return redirect('doctor:serviciosadicionales_list')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ServiciosAdicionalesForm()
    
    context = {
        'form': form,
        'title': 'Crear Servicio Adicional',
        'action': 'Crear'
    }
    return render(request, 'doctor/serviciosadicionales/form.html', context)

def serviciosadicionales_update(request, pk):
    """Actualizar servicio adicional existente"""
    servicio = get_object_or_404(ServiciosAdicionales, pk=pk)
    
    if request.method == 'POST':
        form = ServiciosAdicionalesForm(request.POST, instance=servicio)
        if form.is_valid():
            servicio = form.save()
            messages.success(request, f'Servicio "{servicio.nombre_servicio}" actualizado exitosamente.')
            return redirect('doctor:serviciosadicionales_list')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ServiciosAdicionalesForm(instance=servicio)
    
    context = {
        'form': form,
        'servicio': servicio,
        'title': 'Editar Servicio Adicional',
        'action': 'Actualizar'
    }
    return render(request, 'doctor/serviciosadicionales/form.html', context)

def serviciosadicionales_delete(request, pk):
    """Eliminar servicio adicional"""
    servicio = get_object_or_404(ServiciosAdicionales, pk=pk)
    
    if request.method == 'POST':
        nombre_servicio = servicio.nombre_servicio
        servicio.delete()
        messages.success(request, f'Servicio "{nombre_servicio}" eliminado exitosamente.')
        return redirect('doctor:serviciosadicionales_list')
    
    context = {
        'servicio': servicio,
        'title': 'Eliminar Servicio Adicional'
    }
    return render(request, 'doctor/serviciosadicionales/delete.html', context)