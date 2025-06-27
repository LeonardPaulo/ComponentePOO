from django import forms
from django.forms import ModelForm
from applications.core.models import Paciente


class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
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
        }
