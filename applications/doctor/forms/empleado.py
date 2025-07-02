# applications/doctor/forms/empleado.py

from django import forms
from applications.core.models import Empleado, Cargo
from django.utils import timezone
from datetime import date

class EmpleadoForm(forms.ModelForm):
    # Campo para el campo 'cargo' con un QuerySet limitado
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.filter(activo=True).order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-select block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
        label="Cargo del Empleado"
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

    fecha_ingreso = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'
            },
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
        label='Fecha de Ingreso'
    )

    class Meta:
        model = Empleado
        fields = [
            'nombres',
            'apellidos',
            'cedula_ecuatoriana',
            'dni',
            'fecha_nacimiento',
            'cargo',
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
            'sueldo': forms.NumberInput(attrs={'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'step': '0.01', 'placeholder': 'Ej: 1200.50'}),
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
            'sueldo': 'Sueldo',
            'direccion': 'Dirección',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'foto': 'Foto del Empleado',
            'activo': 'Activo',
        }
        help_texts = {
            'cedula_ecuatoriana': 'Ingrese el número de cédula sin espacios ni guiones.',
            'dni': 'Pasaporte, DNI, CURP u otro documento válido internacionalmente.',
            'fecha_nacimiento': 'Seleccione la fecha de nacimiento del empleado.',
            'fecha_ingreso': 'Seleccione la fecha de ingreso del empleado a la empresa.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Asegurar que las fechas se muestren correctamente en edición
        if self.instance and self.instance.pk:
            if self.instance.fecha_nacimiento:
                self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
            if self.instance.fecha_ingreso:
                self.fields['fecha_ingreso'].initial = self.instance.fecha_ingreso.strftime('%Y-%m-%d')
        
        # Hacer que algunos campos sean requeridos
        self.fields['nombres'].required = True
        self.fields['apellidos'].required = True
        self.fields['cedula_ecuatoriana'].required = True
        self.fields['fecha_nacimiento'].required = True
        self.fields['fecha_ingreso'].required = True
        self.fields['cargo'].required = True

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        
        if fecha_nacimiento:
            # Validar que la fecha no sea futura
            if fecha_nacimiento > date.today():
                raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
            
            # Validar que la persona tenga al menos 18 años
            edad = (date.today() - fecha_nacimiento).days // 365
            if edad < 18:
                raise forms.ValidationError('El empleado debe ser mayor de 18 años.')
            
            # Validar que la persona no tenga más de 100 años
            if edad > 100:
                raise forms.ValidationError('La fecha de nacimiento no puede ser tan antigua.')
        
        return fecha_nacimiento

    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data.get('fecha_ingreso')
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        
        if fecha_ingreso:
            # Validar que la fecha no sea futura
            if fecha_ingreso > date.today():
                raise forms.ValidationError('La fecha de ingreso no puede ser futura.')
            
            # Validar que la fecha de ingreso sea posterior a la fecha de nacimiento
            if fecha_nacimiento and fecha_ingreso <= fecha_nacimiento:
                raise forms.ValidationError('La fecha de ingreso debe ser posterior a la fecha de nacimiento.')
            
            # Validar que la persona tenga al menos 18 años en la fecha de ingreso
            if fecha_nacimiento:
                edad_ingreso = (fecha_ingreso - fecha_nacimiento).days // 365
                if edad_ingreso < 18:
                    raise forms.ValidationError('El empleado debe tener al menos 18 años en la fecha de ingreso.')
        
        return fecha_ingreso

    def clean_cedula_ecuatoriana(self):
        cedula = self.cleaned_data.get('cedula_ecuatoriana')
        
        if cedula:
            # Verificar que solo contenga números
            if not cedula.isdigit():
                raise forms.ValidationError('La cédula debe contener solo números.')
            
            # Verificar que tenga exactamente 10 dígitos
            if len(cedula) != 10:
                raise forms.ValidationError('La cédula debe tener exactamente 10 dígitos.')
            
            # Verificar que no exista otro empleado con la misma cédula (excepto el actual en edición)
            existing_empleado = Empleado.objects.filter(cedula_ecuatoriana=cedula).exclude(pk=self.instance.pk if self.instance else None)
            if existing_empleado.exists():
                raise forms.ValidationError('Ya existe un empleado con esta cédula.')
        
        return cedula

    def clean_sueldo(self):
        sueldo = self.cleaned_data.get('sueldo')
        
        if sueldo is not None:
            # Validar que el sueldo sea positivo
            if sueldo <= 0:
                raise forms.ValidationError('El sueldo debe ser mayor a 0.')
            
            # Validar que el sueldo no sea excesivamente alto (opcional)
            if sueldo > 100000:
                raise forms.ValidationError('El sueldo parece excesivamente alto. Verifique el monto.')
        
        return sueldo