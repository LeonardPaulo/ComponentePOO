# applications/doctor/forms/empleado.py

from django import forms
from applications.core.models import Empleado, Cargo # Importa Empleado y Cargo

class EmpleadoForm(forms.ModelForm):
    # Campo para el campo 'cargo' con un QuerySet limitado
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.filter(activo=True).order_by('nombre'), # Solo cargos activos, ordenados por nombre
        widget=forms.Select(attrs={'class': 'form-select block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
        label="Cargo del Empleado"
    )

    class Meta:
        model = Empleado
        fields = [
            'nombres',
            'apellidos',
            'cedula_ecuatoriana',
            'dni',
            'fecha_nacimiento',
            'cargo', # Usamos el campo definido arriba
            'sueldo',
            'fecha_ingreso',
            'direccion',
            'latitud',
            'longitud',
            'foto',
            'activo',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Nombres del empleado'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Apellidos del empleado'}),
            'cedula_ecuatoriana': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ej: 1234567890', 'pattern': '[0-9]{10}', 'title': 'Ingrese 10 dígitos numéricos'}),
            'dni': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Documento internacional (opcional)'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            # 'cargo': Ya está definido arriba con su widget
            'sueldo': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': '0.01', 'placeholder': 'Ej: 1200.50'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'direccion': forms.TextInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Dirección completa'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': 'any', 'placeholder': 'Ej: -2.12345'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': 'any', 'placeholder': 'Ej: -79.98765'}),
            'foto': forms.FileInput(attrs={'class': 'form-input-file block w-full text-gray-700 dark:text-gray-300 border border-gray-300 rounded-md cursor-pointer bg-gray-50 dark:bg-gray-700 dark:border-gray-600 focus:outline-none'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:checked:bg-emerald-500 dark:checked:border-emerald-500'}),
        }
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'cedula_ecuatoriana': 'Cédula Ecuatoriana',
            'dni': 'DNI Internacional',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            # 'cargo': El label ya está definido en ModelChoiceField
            'sueldo': 'Sueldo',
            'fecha_ingreso': 'Fecha de Ingreso',
            'direccion': 'Dirección',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'foto': 'Foto del Empleado',
            'activo': 'Activo',
        }
        help_texts = {
            'cedula_ecuatoriana': 'Ingrese el número de cédula sin espacios ni guiones.',
            'dni': 'Pasaporte, DNI, CURP u otro documento válido internacionalmente.',
        }