from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from applications.doctor.models import Pago
from applications.doctor.forms.pago import PagoForm
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class PagoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/pago/list.html'
    model = Pago
    context_object_name = 'pagos'
    permission_required = 'view_pago'
    paginate_by = 2

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(
                Q(nombre_pagador__icontains=q) |
                Q(metodo_pago__icontains=q)
            )
        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:pago_create')
        return context

class PagoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Pago
    template_name = 'doctor/pago/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'add_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.metodo_pago == 'paypal' and form.instance.estado == 'pagado':
            return redirect(reverse('doctor:paypal_pago', args=[form.instance.id]))
        messages.success(self.request, f"Pago registrado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar el pago.")
        return super().form_invalid(form)

class PagoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Pago
    template_name = 'doctor/pago/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'change_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance.metodo_pago == 'paypal' and form.instance.estado == 'pagado':
            return redirect(reverse('doctor:paypal_pago', args=[form.instance.id]))
        messages.success(self.request, f"Pago actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el pago.")
        return super().form_invalid(form)

class PagoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Pago
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'delete_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Pago'
        context['description'] = f"¿Desea eliminar el pago #{self.object.id}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Pago eliminado exitosamente.")
        return response