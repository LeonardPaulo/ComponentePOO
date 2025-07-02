# applications/doctor/forms/doctor.py

from django import forms
from applications.core.models import Doctor, Especialidad
from django.utils import timezone
from datetime import date

class DoctorForm(forms.ModelForm):
    especialidad = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.filter(activo=True).order_by('nombre'),
        widget=forms.SelectMultiple(attrs={'class': 'form-multiselect block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white h-32'}),
        label="Especialidad(es)"
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'
            },
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
        label='Fecha de Nacimiento'
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
            'direccion': 'Dirección de Trabajo',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'foto': 'Foto del Doctor',
            'activo': 'Activo',
        }
        help_texts = {
            'ruc': 'Ingrese el número de RUC de 13 dígitos.',
            'fecha_nacimiento': 'Seleccione la fecha de nacimiento del doctor.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Asegurar que la fecha de nacimiento se muestre correctamente en edición
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
        
        # Hacer que algunos campos sean requeridos
        self.fields['nombres'].required = True
        self.fields['apellidos'].required = True
        self.fields['ruc'].required = True
        self.fields['fecha_nacimiento'].required = True
        self.fields['especialidad'].required = True

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        
        if fecha_nacimiento:
            # Validar que la fecha no sea futura
            if fecha_nacimiento > date.today():
                raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
            
            # Validar que la persona tenga al menos 18 años
            edad = (date.today() - fecha_nacimiento).days // 365
            if edad < 18:
                raise forms.ValidationError('El doctor debe ser mayor de 18 años.')
            
            # Validar que la persona no tenga más de 100 años
            if edad > 100:
                raise forms.ValidationError('La fecha de nacimiento no puede ser tan antigua.')
        
        return fecha_nacimiento

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        
        if ruc:
            # Verificar que solo contenga números
            if not ruc.isdigit():
                raise forms.ValidationError('El RUC debe contener solo números.')
            
            # Verificar que tenga exactamente 13 dígitos
            if len(ruc) != 13:
                raise forms.ValidationError('El RUC debe tener exactamente 13 dígitos.')
            
            # Verificar que no exista otro doctor con el mismo RUC (excepto el actual en edición)
            existing_doctor = Doctor.objects.filter(ruc=ruc).exclude(pk=self.instance.pk if self.instance else None)
            if existing_doctor.exists():
                raise forms.ValidationError('Ya existe un doctor con este RUC.')
        
        return ruc