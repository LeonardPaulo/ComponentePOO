import paypalrestsdk
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from applications.doctor.models import Pago

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def crear_pago_paypal(request, pago_id):
    pago = Pago.objects.get(pk=pago_id)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('doctor:paypal_success', args=[pago.id])),
            "cancel_url": request.build_absolute_uri(reverse('doctor:paypal_cancel', args=[pago.id])),
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"Pago #{pago.id}",
                    "sku": f"pago-{pago.id}",
                    "price": str(pago.monto_total),
                    "currency": "USD",
                    "quantity": 1,
                }]
            },
            "amount": {
                "total": str(pago.monto_total),
                "currency": "USD"
            },
            "description": f"Pago de servicios médicos #{pago.id}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
        return render(request, "error.html", {"mensaje": "No se encontró el enlace de aprobación de PayPal."})
    else:
        return render(request, "error.html", {"mensaje": "Error al crear el pago en PayPal."})

def paypal_success(request, pago_id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        pago = Pago.objects.get(pk=pago_id)
        pago.estado = 'pagado'
        pago.save()
        return render(request, "doctor/pago/paypal_success.html", {"pago": pago})
    else:
        return render(request, "error.html", {"mensaje": "No se pudo completar el pago."})

def paypal_cancel(request, pago_id):
    return render(request, "doctor/pago/paypal_cancel.html", {"pago_id": pago_id})