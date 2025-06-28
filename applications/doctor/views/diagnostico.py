# applications/doctor/views/diagnostico.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q # ¡Importa Q para las búsquedas OR!
from applications.core.models import Diagnostico
from applications.doctor.forms.diagnostico import DiagnosticoForm

# Vista para listar todos los diagnósticos
class DiagnosticoListView(ListView):
    model = Diagnostico
    template_name = 'doctor/diagnostico/list.html'
    context_object_name = 'diagnosticos'
    paginate_by = 10

    # Sobreescribe el método get_queryset para añadir la lógica de búsqueda
    def get_queryset(self):
        queryset = super().get_queryset() # Obtiene el queryset base (todos los Diagnosticos)
        search_query = self.request.GET.get('q', '') # Obtiene el parámetro 'q' de la URL

        if search_query:
            # Aplica el filtro al queryset si hay un término de búsqueda
            queryset = queryset.filter(
                Q(codigo__icontains=search_query) | # Busca en el campo 'codigo' (insensible a mayúsculas/minúsculas)
                Q(descripcion__icontains=search_query) # Busca en el campo 'descripcion'
            ).distinct() # Usa distinct() para evitar duplicados si un mismo objeto coincide con múltiples Qs

        # Opcional: Puedes añadir un ordenamiento por defecto
        queryset = queryset.order_by('codigo') # Ordena por el campo 'codigo'

        return queryset

    # Opcional: Para pasar el search_query de vuelta a la plantilla y mantenerlo en el campo de búsqueda
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        # Agrega cualquier otro contexto que necesites, como 'title', 'title1', 'permissions'
        context['title'] = 'Lista de Diagnósticos'
        context['title1'] = 'Diagnósticos'
        # Si tienes un método get_permissions_context en este mismo archivo, puedes llamarlo:
        # context['permissions'] = self.get_permissions_context(self.request)
        return context

# Vista para crear un nuevo diagnóstico
class DiagnosticoCreateView(CreateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'doctor/diagnostico/form.html'
    success_url = reverse_lazy('doctor:diagnostico_list')

# Vista para actualizar un diagnóstico existente
class DiagnosticoUpdateView(UpdateView):
    model = Diagnostico
    form_class = DiagnosticoForm
    template_name = 'doctor/diagnostico/form.html'
    success_url = reverse_lazy('doctor:diagnostico_list')

# Vista para eliminar un diagnóstico
class DiagnosticoDeleteView(DeleteView):
    model = Diagnostico
    # NO necesitas template_name si la eliminación se hace vía POST directamente sin confirmación HTML.
    # Si Django te da un error de TemplateDoesNotExist, significa que espera una plantilla por defecto
    # para GET (confirmación) o POST (si no está bien configurado el botón).
    # La mejor práctica para DeleteView es tener un template_name con un formulario POST para confirmar.
    # Si quieres una eliminación directa por POST desde el listado, asegúrate que tu botón de eliminar
    # en el template sea un <form action="{% url 'doctor:diagnostico_delete' diagnostico.pk %}" method="post">
    # y que incluya {% csrf_token %}.
    success_url = reverse_lazy('doctor:diagnostico_list')