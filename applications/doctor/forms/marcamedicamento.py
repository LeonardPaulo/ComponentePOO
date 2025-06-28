# applications/doctor/forms/marcamedicamento.py

from django import forms
from applications.core.models import MarcaMedicamento # Asegúrate de importar el modelo correcto

class MarcaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = MarcaMedicamento
        fields = ['nombre', 'descripcion', 'activo'] # ¡Incluimos 'activo' aquí!
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                'placeholder': 'Ej: Pfizer, Bayer, Genfar'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                'placeholder': 'Información adicional sobre esta marca de medicamento.',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-blue-600 dark:bg-gray-700 dark:border-gray-600 rounded focus:ring-blue-500'
            }),
        }
        
        labels = {
            'nombre': 'Marca de Medicamento',
            'descripcion': 'Descripción',
            'activo': 'Activo',
        }
        
        help_texts = {
            'nombre': 'Nombre de la marca comercial.',
            'descripcion': 'Descripción general u observaciones sobre esta marca.',
            'activo': 'Indica si esta marca de medicamento está activa o inactiva.',
        }