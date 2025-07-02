from django import forms
from applications.core.models import GastoMensual

class GastoMensualForm(forms.ModelForm):
    class Meta:
        model = GastoMensual
        fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5'}),
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5'
                },
                format='%Y-%m-%d'
            ),
            'valor': forms.NumberInput(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5', 'step': '0.01'}),
            'observacion': forms.Textarea(attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg block w-full p-2.5', 'rows': 2, 'placeholder': 'Observaciones (opcional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar el formato de entrada de fecha
        self.fields['fecha'].input_formats = ['%Y-%m-%d']
        
        # Si es una instancia existente, asegurar que la fecha se formatee correctamente
        if self.instance and self.instance.pk and hasattr(self.instance, 'fecha'):
            if self.instance.fecha:
                # Asegurar que el campo de fecha tenga el valor correcto
                self.fields['fecha'].widget.attrs['value'] = self.instance.fecha.strftime('%Y-%m-%d')