from django import forms
from applications.core.models import FotoPaciente

class FotoPacienteForm(forms.ModelForm):
    class Meta:
        model = FotoPaciente
        fields = ['paciente', 'imagen', 'descripcion']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descripción (opcional)'}),
        }