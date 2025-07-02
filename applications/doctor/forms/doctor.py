# applications/doctor/forms/doctor.py

from django import forms
from applications.core.models import Doctor, Especialidad

class DoctorForm(forms.ModelForm):
    especialidad = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.filter(activo=True).order_by('nombre'),
        widget=forms.SelectMultiple(attrs={'class': 'form-multiselect block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white h-32'}),
        label="Especialidad(es)"
    )

    class Meta:
        model = Doctor
        fields = [
            'nombres',
            'apellidos',
            'ruc',
            'especialidad',
            'fecha_nacimiento',
            'direccion',
            'latitud',
            'longitud',
            'foto',
            'activo',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Nombres del doctor'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Apellidos del doctor'}),
            'ruc': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ej: 1234567890001', 'pattern': '[0-9]{13}', 'title': 'Ingrese 13 dígitos numéricos para el RUC'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'direccion': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Dirección de trabajo'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': 'any', 'placeholder': 'Ej: -2.12345'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': 'any', 'placeholder': 'Ej: -79.98765'}),
            'foto': forms.FileInput(attrs={'class': 'form-input-file block w-full text-gray-700 dark:text-gray-300 border border-gray-300 rounded-md cursor-pointer bg-gray-50 dark:bg-gray-700 dark:border-gray-600 focus:outline-none'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:checked:bg-emerald-500 dark:checked:border-emerald-500'}),
        }
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'ruc': 'RUC',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Dirección de Trabajo',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'foto': 'Foto del Doctor',
            'activo': 'Activo',
        }
        help_texts = {
            'ruc': 'Ingrese el número de RUC de 13 dígitos.',
        }