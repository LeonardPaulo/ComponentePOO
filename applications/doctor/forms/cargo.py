# applications/doctor/forms/cargo.py

from django import forms
from applications.core.models import Cargo # Asegúrate de importar el modelo Cargo

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = [
            'nombre',
            'descripcion',
            'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ej.: Médico, Enfermero, Administrador'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'rows': 3, 'placeholder': 'Descripción breve del rol.'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:checked:bg-emerald-500 dark:checked:border-emerald-500'}),
        }
        labels = {
            'nombre': 'Nombre del Cargo',
            'descripcion': 'Descripción del Cargo',
            'activo': 'Activo',
        }
        help_texts = {
            'nombre': 'Ej.: Médico, Enfermero, Administrador',
            'descripcion': 'Descripción breve del rol que cumple este cargo (opcional).',
            'activo': 'Desactiva este cargo si ya no se usa en el sistema.',
        }