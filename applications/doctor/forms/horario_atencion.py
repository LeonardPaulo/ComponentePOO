from django import forms
from applications.doctor.models import HorarioAtencion

class HorarioAtencionForm(forms.ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = [
            'dia_semana',
            'hora_inicio',
            'hora_fin',
            'intervalo_desde',
            'intervalo_hasta',
            'activo',
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
            'intervalo_desde': forms.TimeInput(attrs={'type': 'time'}),
            'intervalo_hasta': forms.TimeInput(attrs={'type': 'time'}),
        }