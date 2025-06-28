from django.urls import path

from applications.doctor.views.atencion_medica import (
    AtencionListView, AtencionCreateView, AtencionUpdateView, AtencionDeleteView
)
from applications.doctor.views.pacientes import (
    PacienteListView,
    PacienteCreateView,
    PacienteUpdateView,
    PacienteDeleteView,
)
from applications.doctor.views import tiposangre as tiposangre_views
from applications.doctor.views.diagnostico import (
    DiagnosticoListView,
    DiagnosticoCreateView,
    DiagnosticoUpdateView,
    DiagnosticoDeleteView,
)
from applications.doctor.views.tipomedicamento import (
    TipoMedicamentoListView,
    TipoMedicamentoCreateView,
    TipoMedicamentoUpdateView,
    TipoMedicamentoDeleteView,
)
from applications.doctor.views.marcamedicamento import (
    MarcaMedicamentoListView,
    MarcaMedicamentoCreateView,
    MarcaMedicamentoUpdateView,
    MarcaMedicamentoDeleteView
)

app_name = 'doctor'

urlpatterns = [
    # Atenciones médicas
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),

    # Pacientes
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/crear/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),

    # Tipos de Sangre
    path('tipos_sangre/', tiposangre_views.tiposangre_list, name='tiposangre_list'),
    path('tipos_sangre/crear/', tiposangre_views.tiposangre_create, name='tiposangre_create'),
    path('tipos_sangre/editar/<int:pk>/', tiposangre_views.tiposangre_update, name='tiposangre_update'),
    path('tipos_sangre/eliminar/<int:pk>/', tiposangre_views.tiposangre_delete, name='tiposangre_delete'),

    # Diagnósticos
    path('diagnosticos/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnosticos/crear/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnosticos/editar/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnosticos/eliminar/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),

    # Tipos de Medicamento
    path('tiposmedicamento/', TipoMedicamentoListView.as_view(), name='tiposmedicamento_list'),
    path('tiposmedicamento/crear/', TipoMedicamentoCreateView.as_view(), name='tiposmedicamento_create'),
    path('tiposmedicamento/editar/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name='tiposmedicamento_update'),
    path('tiposmedicamento/eliminar/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name='tiposmedicamento_delete'),

    # Marcas de Medicamento
    path('marcasmedicamento/', MarcaMedicamentoListView.as_view(), name='marcasmedicamento_list'),
    path('marcasmedicamento/nuevo/', MarcaMedicamentoCreateView.as_view(), name='marcamedicamento_create'),
    path('marcasmedicamento/editar/<int:pk>/', MarcaMedicamentoUpdateView.as_view(), name='marcamedicamento_update'),
    path('marcasmedicamento/eliminar/<int:pk>/', MarcaMedicamentoDeleteView.as_view(), name='marcamedicamento_delete'),
]