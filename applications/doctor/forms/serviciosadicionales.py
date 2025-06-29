from django import forms
from applications.doctor.models import ServiciosAdicionales

class ServiciosAdicionalesForm(forms.ModelForm):
    class Meta:
        model = ServiciosAdicionales
        fields = ['nombre_servicio', 'costo_servicio', 'descripcion', 'activo']
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5',
                'placeholder': 'Ej: Radiografía, Laboratorio clínico'
            }),
            'costo_servicio': forms.NumberInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5',
                'rows': 3,
                'placeholder': 'Descripción opcional del servicio'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2'
            }),
        }