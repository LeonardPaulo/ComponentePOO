# applications/doctor/forms/especialidad.py
from django import forms
from applications.core.models import Especialidad

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'activo'] # Asegúrate de que 'activo' esté aquí si lo tienes en el modelo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la especialidad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la especialidad'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }