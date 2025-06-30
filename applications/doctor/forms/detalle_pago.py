from django import forms
from applications.doctor.models import DetallePago

class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'pago',
            'servicio_adicional',
            'cantidad',
            'precio_unitario',
            'descuento_porcentaje',
            'aplica_seguro',
            'valor_seguro',
            'descripcion_seguro',
        ]
        widgets = {
            'descripcion_seguro': forms.TextInput(attrs={'placeholder': 'Nombre del seguro, si aplica'}),
        }