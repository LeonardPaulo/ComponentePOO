# applications/doctor/forms/tiposangre.py

from django import forms
# CORREGIDO: 'aplicaciones' cambiado a 'applications'
from applications.core.models import TipoSangre 

class TipoSangreForm(forms.ModelForm):
    class Meta:
        model = TipoSangre
        fields = ['tipo', 'descripcion']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-emerald-500 dark:focus:border-emerald-500 dark:shadow-sm-light', 'placeholder': 'Ej: A+'}),
            'descripcion': forms.TextInput(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-emerald-500 focus:border-emerald-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-emerald-500 dark:focus:border-emerald-500 dark:shadow-sm-light', 'placeholder': 'Ej: Sangre tipo A positivo (opcional)'}),
        }