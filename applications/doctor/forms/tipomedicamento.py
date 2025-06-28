# applications/doctor/forms/tipomedicamento.py

from django import forms
from applications.core.models import TipoMedicamento

class TipoMedicamentoForm(forms.ModelForm):
    class Meta:
        model = TipoMedicamento
        fields = ['nombre', 'descripcion', 'activo']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                'placeholder': 'Ej: Analgésico, Antibiótico, Antiinflamatorio'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                'placeholder': 'Información adicional sobre este tipo de medicamento.',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-blue-600 dark:bg-gray-700 dark:border-gray-600 rounded focus:ring-blue-500'
            }),
        }
        
        labels = {
            'nombre': 'Tipo de Medicamento',
            'descripcion': 'Descripción',
            'activo': 'Activo',
        }
        
        help_texts = {
            'nombre': 'Nombre del tipo de medicamento (Ej: Analgésico, Antibiótico)',
            'descripcion': 'Información adicional sobre este tipo de medicamento.',
            'activo': 'Indica si este tipo de medicamento está activo o inactivo.',
        }