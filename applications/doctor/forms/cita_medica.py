from django import forms
from applications.doctor.models import CitaMedica

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = [
            'nombre_paciente',
            'apellido_paciente',
            'cedula_paciente',
            'direccion_paciente',
            'fecha',
            'hora_cita',
            'estado',
            'observaciones'
        ]
        widgets = {
            'nombre_paciente': forms.TextInput(attrs={'class': 'form-input'}),
            'apellido_paciente': forms.TextInput(attrs={'class': 'form-input'}),
            'cedula_paciente': forms.TextInput(attrs={'class': 'form-input'}),
            'direccion_paciente': forms.TextInput(attrs={'class': 'form-input'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
        labels = {
            'nombre_paciente': 'Nombre',
            'apellido_paciente': 'Apellido',
            'cedula_paciente': 'Cédula',
            'direccion_paciente': 'Dirección',
            'fecha': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }