from django import forms
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