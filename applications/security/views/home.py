from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from applications.security.components.menu_module import MenuModule
from applications.security.components.mixin_crud import PermissionMixin
from applications.security.models import User
from applications.doctor.models import Atencion, CitaMedica, HorarioAtencion
from applications.core.models import Paciente

class ModuloTemplateView(PermissionMixin, TemplateView):
    template_name = 'home.html'
   
    def get_context_data(self, **kwargs):
        context = {}
        context["title"] = "SaludTotal - Dashboard"
        context["title1"] = "Módulos Disponibles"
        
        # Agregar estadísticas reales
        context.update(self.get_dashboard_stats())
        
        # Llenar el contexto con menús y permisos
        MenuModule(self.request).fill(context)
        
        return context
    
    def get_dashboard_stats(self):
        """
        Obtiene las estadísticas reales del sistema
        """
        try:
            # Fecha actual
            hoy = timezone.now().date()
            
            # 1. Total de usuarios activos
            total_usuarios = User.objects.filter(is_active=True).count()
            
            # 2. Atenciones del día actual
            atenciones_hoy = Atencion.objects.filter(
                fecha_atencion__date=hoy
            ).count()
            
            # 3. Consultas pendientes (citas médicas programadas que no están atendidas)
            consultas_pendientes = CitaMedica.objects.filter(
                Q(fecha__gte=hoy) & 
                ~Q(estado='atendido')
            ).count()
            
            # 4. Mantenimientos/Horarios inactivos
            mantenimientos = HorarioAtencion.objects.filter(activo=False).count()
            
            return {
                'stats': {
                    'total_usuarios': total_usuarios,
                    'atenciones_hoy': atenciones_hoy,
                    'consultas_pendientes': consultas_pendientes,
                    'mantenimientos': mantenimientos,
                }
            }
            
        except Exception as e:
            # En caso de error, devolver valores por defecto
            return {
                'stats': {
                    'total_usuarios': 0,
                    'atenciones_hoy': 0,
                    'consultas_pendientes': 0,
                    'mantenimientos': 0,
                }
            }