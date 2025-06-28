from django import forms
from applications.core.models import TipoGasto

class TipoGastoForm(forms.ModelForm):
    class Meta:
        model = TipoGasto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-emerald-500 dark:focus:border-emerald-500 dark:shadow-sm-light',
                'placeholder': 'Ej: Servicios básicos'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-emerald-500 dark:focus:border-emerald-500 dark:shadow-sm-light',
                'placeholder': 'Ej: Agua, luz, teléfono (opcional)'
            }),
        }