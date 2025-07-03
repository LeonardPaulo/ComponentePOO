from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.views import View
from datetime import datetime, timedelta, time
from applications.doctor.models import HorarioAtencion, CitaMedica
from applications.doctor.utils.intervalos import generar_intervalos
from applications.security.components.mixin_crud import PermissionMixin
from applications.security.components.menu_module import MenuModule

class AgendaCalendarioView(PermissionMixin, View):
    permission_required = 'view_horarioatencion'
    
    def get(self, request):
        fecha_str = request.GET.get('fecha')
        if fecha_str:
            try:
                hoy = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                hoy = datetime.today().date()
        else:
            hoy = datetime.today().date()

        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        agenda = []

        for i, dia_nombre in enumerate(dias_semana):
            fecha = hoy + timedelta(days=(i - hoy.weekday()))
            horarios = HorarioAtencion.objects.filter(dia_semana=dia_nombre, activo=True)
            intervalos_dia = []
            for horario in horarios:
                if horario.intervalo_desde and horario.intervalo_hasta:
                    # Intervalos antes del descanso
                    intervalos_antes = generar_intervalos(
                        horario.hora_inicio.strftime('%H:%M'),
                        horario.intervalo_desde.strftime('%H:%M')
                    )
                    # Intervalos de descanso (siempre ocupados)
                    intervalos_descanso = generar_intervalos(
                        horario.intervalo_desde.strftime('%H:%M'),
                        horario.intervalo_hasta.strftime('%H:%M')
                    )
                    # Intervalos después del descanso
                    intervalos_despues = generar_intervalos(
                        horario.intervalo_hasta.strftime('%H:%M'),
                        horario.hora_fin.strftime('%H:%M')
                    )
                    # Antes del descanso
                    for inicio, fin in intervalos_antes:
                        hora = time.fromisoformat(inicio)
                        cita = CitaMedica.objects.filter(
                            fecha=fecha,
                            hora_cita=hora
                        ).first()
                        if cita:
                            if cita.estado == 'atendido':
                                estado = 'atendido'
                            else:
                                estado = 'ocupado'
                        else:
                            estado = 'disponible'
                        intervalos_dia.append({
                            'inicio': inicio,
                            'fin': fin,
                            'estado': estado
                        })
                    # Intervalos de descanso (ocupados)
                    for inicio, fin in intervalos_descanso:
                        intervalos_dia.append({
                            'inicio': inicio,
                            'fin': fin,
                            'estado': 'descanso'
                        })
                    # Después del descanso
                    for inicio, fin in intervalos_despues:
                        hora = time.fromisoformat(inicio)
                        cita = CitaMedica.objects.filter(
                            fecha=fecha,
                            hora_cita=hora
                        ).first()
                        if cita:
                            if cita.estado == 'atendido':
                                estado = 'atendido'
                            else:
                                estado = 'ocupado'
                        else:
                            estado = 'disponible'
                        intervalos_dia.append({
                            'inicio': inicio,
                            'fin': fin,
                            'estado': estado
                        })
                else:
                    intervalos = generar_intervalos(
                        horario.hora_inicio.strftime('%H:%M'),
                        horario.hora_fin.strftime('%H:%M')
                    )
                    for inicio, fin in intervalos:
                        hora = time.fromisoformat(inicio)
                        cita = CitaMedica.objects.filter(
                            fecha=fecha,
                            hora_cita=hora
                        ).first()
                        if cita:
                            if cita.estado == 'atendido':
                                estado = 'atendido'
                            else:
                                estado = 'ocupado'
                        else:
                            estado = 'disponible'
                        intervalos_dia.append({
                            'inicio': inicio,
                            'fin': fin,
                            'estado': estado
                        })
            agenda.append({
                'dia': dia_nombre.capitalize(),
                'fecha': fecha,
                'intervalos': intervalos_dia
            })

        semana_anterior = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        semana_siguiente = (hoy + timedelta(days=7)).strftime('%Y-%m-%d')

        # Crear el contexto e incluir el MenuModule
        context = {
            'agenda': agenda,
            'semana_anterior': semana_anterior,
            'semana_siguiente': semana_siguiente,
            'hoy': hoy,
        }
        
        # Agregar el contexto del MenuModule (incluyendo group_list)
        MenuModule(request).fill(context)

        return render(request, 'doctor/agenda/calendario.html', context)

# Función wrapper para mantener compatibilidad con URLs existentes
def agenda_calendario(request):
    return AgendaCalendarioView.as_view()(request)