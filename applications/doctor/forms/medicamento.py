# applications/doctor/forms/medicamento.py

from django import forms
# Asegúrate de que Medicamento, TipoMedicamento y MarcaMedicamento estén en applications.core.models
from applications.core.models import Medicamento, TipoMedicamento, MarcaMedicamento 

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'tipo',
            'marca_medicamento',
            'nombre',
            'descripcion',
            'concentracion',
            'via_administracion',
            'cantidad',
            'precio',
            'comercial',
            'foto', # Incluye el campo foto
            'activo'
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'marca_medicamento': forms.Select(attrs={'class': 'form-select block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Nombre comercial o genérico'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'rows': 3, 'placeholder': 'Uso, indicaciones o precauciones relevantes.'}),
            'concentracion': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ejemplo: 500mg, 1g, 5%'}),
            'via_administracion': forms.Select(attrs={'class': 'form-select block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Cantidad en stock'}),
            'precio': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': '0.01', 'placeholder': 'Precio unitario'}),
            'comercial': forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:checked:bg-emerald-500 dark:checked:border-emerald-500'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:checked:bg-emerald-500 dark:checked:border-emerald-500'}),
        }
        labels = {
            'tipo': 'Tipo de Medicamento',
            'marca_medicamento': 'Marca del Medicamento',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'concentracion': 'Concentración',
            'via_administracion': 'Vía de Administración',
            'cantidad': 'Stock',
            'precio': 'Precio Unitario',
            'comercial': 'Es Comercial',
            'foto': 'Foto del Medicamento',
            'activo': 'Activo',
        }
        help_texts = {
            'nombre': 'Nombre comercial o genérico del medicamento.',
            'descripcion': 'Uso, indicaciones o precauciones relevantes.',
            'concentracion': 'Ejemplo: 500mg, 1g, 5%',
            'cantidad': 'Cantidad actual disponible en inventario.',
            'precio': 'Precio unitario del medicamento.',
            'comercial': 'Marcar como "No" si es un medicamento genérico.',
            'via_administracion': 'Forma en que se administra el medicamento (oral, intravenosa, etc.)',
            'foto': 'Sube una imagen del medicamento.',
        }