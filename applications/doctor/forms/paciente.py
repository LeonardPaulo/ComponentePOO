# applications/doctor/forms/pacientes.py

from django import forms
from django.forms import ModelForm
from applications.core.models import Paciente 

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        # EXCLUYE 'ocupacion' al listar explícitamente los campos
        fields = [
            'nombres', 'apellidos', 'cedula_ecuatoriana', 'dni',
            'fecha_nacimiento', 'telefono', 'email', 'sexo',
            'estado_civil', 'direccion', 'latitud', 'longitud',
            'tipo_sangre', 'foto',
            'antecedentes_personales', 'antecedentes_quirurgicos',
            'antecedentes_familiares', 'alergias', 'medicamentos_actuales',
            'habitos_toxicos', 'vacunas', 'antecedentes_gineco_obstetricos',
            'activo', # Si quieres que el campo 'activo' sea editable
        ]

        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Nombres del paciente'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Apellidos del paciente'
            }),
            'cedula_ecuatoriana': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Cédula ecuatoriana'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Número de teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Correo electrónico'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Dirección del paciente'
            }),
            'tipo_sangre': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'antecedentes_personales': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'antecedentes_quirurgicos': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'antecedentes_familiares': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'alergias': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'habitos_toxicos': forms.TextInput(attrs={'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'placeholder': 'Ej: tabaco, alcohol, sedentarismo'}),
            'vacunas': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'antecedentes_gineco_obstetricos': forms.Textarea(attrs={'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200', 'rows': 3}),
            'dni': forms.TextInput(attrs={ 
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'DNI internacional (opcional)'
            }),
        }
