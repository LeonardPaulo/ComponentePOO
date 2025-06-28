from django import forms
from applications.core.models import GastoMensual

class GastoMensualForm(forms.ModelForm):
    class Meta:
        model = GastoMensual
        fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5'}),
            'valor': forms.NumberInput(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5', 'step': '0.01'}),
            'observacion': forms.Textarea(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5', 'rows': 2, 'placeholder': 'Observaciones (opcional)'}),
        }