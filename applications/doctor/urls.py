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
from applications.doctor.views import tiposgasto as tipogasto_views
from applications.doctor.views import gastomensual as gastomensual_views
from applications.doctor.views import fotopaciente as fotopaciente_views
from applications.doctor.views import serviciosadicionales

from .views.cita_medica import (
    CitaMedicaListView,
    CitaMedicaCreateView,
    CitaMedicaUpdateView,
    CitaMedicaDeleteView,
)

from applications.doctor.views.pago import (
    PagoListView, PagoCreateView, PagoUpdateView, PagoDeleteView
)

from applications.doctor.views.detalle_pago import (
    DetallePagoListView, DetallePagoCreateView, DetallePagoUpdateView, DetallePagoDeleteView
)

from applications.doctor.views.horario_atencion import (
    HorarioAtencionListView, HorarioAtencionCreateView, HorarioAtencionUpdateView, HorarioAtencionDeleteView
)

from applications.doctor.views.paypal import crear_pago_paypal, paypal_success, paypal_cancel

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

    # Tipos de Gastos
    path('tipos_gasto/', tipogasto_views.tipogasto_list, name='tipogasto_list'),
    path('tipos_gasto/crear/', tipogasto_views.tipogasto_create, name='tipogasto_create'),
    path('tipos_gasto/editar/<int:pk>/', tipogasto_views.tipogasto_update, name='tipogasto_update'),
    path('tipos_gasto/eliminar/<int:pk>/', tipogasto_views.tipogasto_delete, name='tipogasto_delete'),

    # Gastos Mensuales
    path('gastos_mensuales/', gastomensual_views.gastomensual_list, name='gastomensual_list'),
    path('gastos_mensuales/crear/', gastomensual_views.gastomensual_create, name='gastomensual_create'),
    path('gastos_mensuales/editar/<int:pk>/', gastomensual_views.gastomensual_update, name='gastomensual_update'),
    path('gastos_mensuales/eliminar/<int:pk>/', gastomensual_views.gastomensual_delete, name='gastomensual_delete'),

    path('fotos_paciente/', fotopaciente_views.fotopaciente_list, name='fotopaciente_list'),
    path('fotos_paciente/crear/', fotopaciente_views.fotopaciente_create, name='fotopaciente_create'),
    path('fotos_paciente/editar/<int:pk>/', fotopaciente_views.fotopaciente_update, name='fotopaciente_update'),
    path('fotos_paciente/eliminar/<int:pk>/', fotopaciente_views.fotopaciente_delete, name='fotopaciente_delete'),

    path('serviciosadicionales/', serviciosadicionales.serviciosadicionales_list, name='serviciosadicionales_list'),
    path('serviciosadicionales/create/', serviciosadicionales.serviciosadicionales_create, name='serviciosadicionales_create'),
    path('serviciosadicionales/<int:pk>/update/', serviciosadicionales.serviciosadicionales_update, name='serviciosadicionales_update'),
    path('serviciosadicionales/<int:pk>/delete/', serviciosadicionales.serviciosadicionales_delete, name='serviciosadicionales_delete'),

    # Citas Médicas
    path('citas/', CitaMedicaListView.as_view(), name='cita_list'),
    path('citas/crear/', CitaMedicaCreateView.as_view(), name='cita_create'),
    path('citas/editar/<int:pk>/', CitaMedicaUpdateView.as_view(), name='cita_update'),
    path('citas/eliminar/<int:pk>/', CitaMedicaDeleteView.as_view(), name='cita_delete'),

    # Pagos
    path('pagos/', PagoListView.as_view(), name='pago_list'),
    path('pagos/crear/', PagoCreateView.as_view(), name='pago_create'),
    path('pagos/editar/<int:pk>/', PagoUpdateView.as_view(), name='pago_update'),
    path('pagos/eliminar/<int:pk>/', PagoDeleteView.as_view(), name='pago_delete'),

    # Detalles de Pago
    path('detalle_pago/', DetallePagoListView.as_view(), name='detalle_pago_list'),
    path('detalle_pago/crear/', DetallePagoCreateView.as_view(), name='detalle_pago_create'),
    path('detalle_pago/editar/<int:pk>/', DetallePagoUpdateView.as_view(), name='detalle_pago_update'),
    path('detalle_pago/eliminar/<int:pk>/', DetallePagoDeleteView.as_view(), name='detalle_pago_delete'),

    #Horario de atención
    path('horario_atencion/', HorarioAtencionListView.as_view(), name='horario_atencion_list'),
    path('horario_atencion/crear/', HorarioAtencionCreateView.as_view(), name='horario_atencion_create'),
    path('horario_atencion/editar/<int:pk>/', HorarioAtencionUpdateView.as_view(), name='horario_atencion_update'),
    path('horario_atencion/eliminar/<int:pk>/', HorarioAtencionDeleteView.as_view(), name='horario_atencion_delete'),

    path('pagos/paypal/<int:pago_id>/', crear_pago_paypal, name='paypal_pago'),
    path('pagos/paypal/success/<int:pago_id>/', paypal_success, name='paypal_success'),
    path('pagos/paypal/cancel/<int:pago_id>/', paypal_cancel, name='paypal_cancel'),
]