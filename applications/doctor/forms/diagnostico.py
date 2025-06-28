# applications/doctor/forms/diagnostico.py

from django import forms
from applications.core.models import Diagnostico # Importa tu modelo Diagnostico

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = [
            'codigo',
            'descripcion',
            'datos_adicionales',
            'activo',
        ]
        widgets = {
            'codigo': forms.TextInput(
                attrs={
                    'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                    'placeholder': 'Código del Diagnóstico (Ej: A09)'
                }
            ),
            'descripcion': forms.Textarea( # Cambiado a Textarea para consistencia y posibilidad de múltiples líneas
                attrs={
                    'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                    'placeholder': 'Descripción breve del diagnóstico',
                    'rows': 3 # Puedes ajustar el número de filas si lo deseas
                }
            ),
            'datos_adicionales': forms.Textarea(
                attrs={
                    # ¡Estas son las clases que Flowbite/Tailwind esperan para un textarea!
                    'class': 'block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring',
                    'placeholder': 'Observaciones clínicas, notas o contexto específico',
                    'rows': 3 # Puedes ajustar el número de filas si lo deseas
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={
                    # ¡Estas son las clases para un checkbox!
                    'class': 'form-checkbox h-5 w-5 text-blue-600 dark:bg-gray-700 dark:border-gray-600 rounded focus:ring-blue-500'
                }
            ),
        }
        labels = {
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'datos_adicionales': 'Datos Adicionales',
            'activo': 'Activo',
        }
        # Puedes añadir help_texts aquí si quieres que aparezcan debajo de los campos
        help_texts = {
            'codigo': 'Código estándar del diagnóstico (Ej: A00, I00, K35.2)',
            'descripcion': 'Nombre del diagnóstico según el código (Ej: Faringitis aguda)',
            'datos_adicionales': 'Observaciones clínicas u otra información útil.',
            'activo': 'Desactive este diagnóstico si ya no está en uso.',
        }