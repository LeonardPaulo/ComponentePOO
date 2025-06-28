from django.urls import path

from applications.doctor.views.atencion_medica import (
    AtencionListView, AtencionCreateView, AtencionUpdateView, AtencionDeleteView
)
# applications/doctor/urls.py

from django.urls import path

# Importaciones para AtencionMedica (Class-Based Views)
from applications.doctor.views.atencion_medica import (
    AtencionListView, AtencionCreateView, AtencionUpdateView, AtencionDeleteView
)

# Importaciones para Pacientes (Class-Based Views)
from applications.doctor.views.pacientes import (
    PacienteListView,
    PacienteCreateView,
    PacienteUpdateView,
    PacienteDeleteView,
)

# Importación para Tipos de Sangre (Function-Based Views)
from applications.doctor.views import tiposangre as tiposangre_views

# Importa las vistas de Diagnostico
from applications.doctor.views.diagnostico import (
    DiagnosticoListView,
    DiagnosticoCreateView,
    DiagnosticoUpdateView,
    DiagnosticoDeleteView,
)

# Importaciones para Tipo Medicamento
from applications.doctor.views.tipomedicamento import (
    TipoMedicamentoListView,
    TipoMedicamentoCreateView,
    TipoMedicamentoUpdateView,
    TipoMedicamentoDeleteView,
)

# Importaciones para Marca Medicamento
from applications.doctor.views.marcamedicamento import (
    MarcaMedicamentoListView,
    MarcaMedicamentoCreateView,
    MarcaMedicamentoUpdateView,
    MarcaMedicamentoDeleteView
)


# Definición del espacio de nombres de la aplicación

app_name = 'doctor'

urlpatterns = [
    # Rutas para vistas relacionadas con AtencionMedica (Class-Based Views)
    # Rutas para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),

    # Pacientes

    # Rutas para vistas relacionadas con Pacientes (Class-Based Views)
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/crear/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),

    # Rutas para Tipos de Sangre (Function-Based Views)
    path('tipos_sangre/', tiposangre_views.tiposangre_list, name='tiposangre_list'),
    path('tipos_sangre/crear/', tiposangre_views.tiposangre_create, name='tiposangre_create'),
    path('tipos_sangre/editar/<int:pk>/', tiposangre_views.tiposangre_update, name='tiposangre_update'),
    path('tipos_sangre/eliminar/<int:pk>/', tiposangre_views.tiposangre_delete, name='tiposangre_delete'),

    # Rutas para Diagnóstico (Class-Based Views)
    path('diagnosticos/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnosticos/crear/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnosticos/editar/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnosticos/eliminar/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),

    # Rutas para Tipo de Medicamento
    path('tiposmedicamento/', TipoMedicamentoListView.as_view(), name='tiposmedicamento_list'),
    path('tiposmedicamento/crear/', TipoMedicamentoCreateView.as_view(), name='tiposmedicamento_create'),
    path('tiposmedicamento/editar/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name='tiposmedicamento_update'),
    path('tiposmedicamento/eliminar/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name='tiposmedicamento_delete'),
    
    # Rutas para Marca Medicamento
    path('marcasmedicamento/', MarcaMedicamentoListView.as_view(), name='marcasmedicamento_list'), # <-- ¡CORREGIDO AQUÍ!
    path('marcasmedicamento/nuevo/', MarcaMedicamentoCreateView.as_view(), name='marcamedicamento_create'),
    path('marcasmedicamento/editar/<int:pk>/', MarcaMedicamentoUpdateView.as_view(), name='marcamedicamento_update'),
    path('marcasmedicamento/eliminar/<int:pk>/', MarcaMedicamentoDeleteView.as_view(), name='marcamedicamento_delete'),
]