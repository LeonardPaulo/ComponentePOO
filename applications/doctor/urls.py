# applications/doctor/urls.py

from django.urls import path

# Importaciones para AtencionMedica (Class-Based Views) - Mantener estas líneas
from applications.doctor.views.atencion_medica import (
    AtencionListView, AtencionCreateView, AtencionUpdateView, AtencionDeleteView
)

# Importaciones para Pacientes (Class-Based Views) - Mantener estas líneas
from applications.doctor.views.pacientes import (
    PacienteListView,
    PacienteCreateView,
    PacienteUpdateView,
    PacienteDeleteView,
)

# Importación para Tipos de Sangre (Function-Based Views) - Esto es lo clave para TipoSangre
# ¡CAMBIO AQUÍ! Importa el módulo de vistas de tipos de sangre desde la subcarpeta 'views'
from applications.doctor.views import tiposangre as tiposangre_views 

# Definición del espacio de nombres de la aplicación
app_name = 'doctor'

urlpatterns = [
    # Rutas para vistas relacionadas con AtencionMedica (Class-Based Views)
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),

    # Rutas para vistas relacionadas con Pacientes (Class-Based Views)
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/crear/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # Rutas para Tipos de Sangre (Function-Based Views) - Usando tiposangre_views
    path('tipos_sangre/', tiposangre_views.tiposangre_list, name='tiposangre_list'),
    path('tipos_sangre/crear/', tiposangre_views.tiposangre_create, name='tiposangre_create'),
    path('tipos_sangre/editar/<int:pk>/', tiposangre_views.tiposangre_update, name='tiposangre_update'),
    path('tipos_sangre/eliminar/<int:pk>/', tiposangre_views.tiposangre_delete, name='tiposangre_delete'),
]