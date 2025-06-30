from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from applications.doctor.models import DetallePago
from applications.doctor.forms.detalle_pago import DetallePagoForm
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class DetallePagoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/detalle_pago/list.html'
    model = DetallePago
    context_object_name = 'detalles'
    permission_required = 'view_detallepago'

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(descripcion_seguro__icontains=q)
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:detalle_pago_create')
        return context

class DetallePagoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = DetallePago
    template_name = 'doctor/detalle_pago/form.html'
    form_class = DetallePagoForm
    success_url = reverse_lazy('doctor:detalle_pago_list')
    permission_required = 'add_detallepago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Detalle de Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Detalle de pago registrado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar el detalle de pago.")
        return super().form_invalid(form)

class DetallePagoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = DetallePago
    template_name = 'doctor/detalle_pago/form.html'
    form_class = DetallePagoForm
    success_url = reverse_lazy('doctor:detalle_pago_list')
    permission_required = 'change_detallepago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Detalle de Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Detalle de pago actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el detalle de pago.")
        return super().form_invalid(form)

class DetallePagoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = DetallePago
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:detalle_pago_list')
    permission_required = 'delete_detallepago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Detalle de Pago'
        context['description'] = f"¿Desea eliminar el detalle de pago #{self.object.id}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Detalle de pago eliminado exitosamente.")
        return response