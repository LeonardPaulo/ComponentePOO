from django import forms
from applications.doctor.models import CitaMedica

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
        labels = {
            'paciente': 'Paciente',
            'fecha': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }