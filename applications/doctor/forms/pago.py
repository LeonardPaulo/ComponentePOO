from django import forms
from django.utils import timezone
from applications.doctor.models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'atencion', 'metodo_pago', 'monto_total', 'estado', 'fecha_pago',
            'nombre_pagador', 'referencia_externa', 'evidencia_pago', 'observaciones', 'activo'
        ]
        widgets = {
            'fecha_pago': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando un objeto existente y tiene fecha_pago, formatearla correctamente
        if self.instance and self.instance.pk and self.instance.fecha_pago:
            # Convertir a zona horaria local usando Django
            local_time = timezone.localtime(self.instance.fecha_pago)
            # Formatear la fecha para que sea compatible con datetime-local
            self.initial['fecha_pago'] = local_time.strftime('%Y-%m-%dT%H:%M')

    def clean_fecha_pago(self):
        fecha_pago = self.cleaned_data.get('fecha_pago')
        estado = self.cleaned_data.get('estado')
        
        # Si el estado es 'pagado' y no hay fecha, asignar la fecha actual
        if estado == 'pagado' and not fecha_pago:
            # Solo si es un nuevo registro (no estamos editando)
            if not self.instance.pk:
                return timezone.now()
        
        # Si tenemos una fecha, asegurar que esté en la zona horaria correcta
        if fecha_pago and timezone.is_naive(fecha_pago):
            # Convertir la fecha naive a aware usando la zona horaria actual
            fecha_pago = timezone.make_aware(fecha_pago)
        
        return fecha_pago