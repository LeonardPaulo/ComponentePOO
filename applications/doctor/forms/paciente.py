# applications/doctor/forms/pacientes.py

from django import forms
from django.forms import ModelForm
from applications.core.models import Paciente, FotoPaciente

class PacienteForm(ModelForm):
    # Campo adicional para seleccionar foto existente
    foto_existente = forms.ModelChoiceField(
        queryset=FotoPaciente.objects.all(),
        required=False,
        empty_label="-- Seleccionar foto existente --",
        widget=forms.Select(attrs={
            'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
            'onchange': 'mostrarFotoSeleccionada(this.value)'
        }),
        help_text="Selecciona una foto existente de la galería de pacientes"
    )
    
    class Meta:
        model = Paciente
        fields = [
            'nombres', 'apellidos', 'cedula_ecuatoriana', 'dni',
            'fecha_nacimiento', 'telefono', 'email', 'sexo',
            'estado_civil', 'direccion', 'latitud', 'longitud',
            'tipo_sangre', 'foto', 'foto_referencia',  # ← Agregar foto_referencia
            'antecedentes_personales', 'antecedentes_quirurgicos',
            'antecedentes_familiares', 'alergias', 'medicamentos_actuales',
            'habitos_toxicos', 'vacunas', 'antecedentes_gineco_obstetricos',
            'activo',
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
            'foto': forms.FileInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'accept': 'image/*',
                'onchange': 'mostrarVistaPrevia(this)'
            }),
            'foto_referencia': forms.HiddenInput(),  # Campo oculto
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # Filtrar solo fotos que tienen imagen válida
        self.fields['foto_existente'].queryset = FotoPaciente.objects.filter(
            imagen__isnull=False
        ).select_related('paciente').order_by('-fecha_subida')
    
    # Personalizar el label de cada opción para mostrar paciente y fecha
        choices = [('', '-- Seleccionar foto existente --')]
        for foto in self.fields['foto_existente'].queryset:
            label = f"{foto.paciente} - {foto.fecha_subida.strftime('%d/%m/%Y')}"
            if foto.descripcion:
                label += f" ({foto.descripcion[:30]}...)" if len(foto.descripcion) > 30 else f" ({foto.descripcion})"
            choices.append((foto.pk, label))
    
        self.fields['foto_existente'].choices = choices
    
    # IMPORTANTE: Configurar campo activo como oculto y por defecto True
        self.fields['activo'].widget = forms.HiddenInput()
        self.fields['activo'].initial = True