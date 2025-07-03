from django import forms
from applications.core.models import FotoPaciente


class FotoPacienteForm(forms.ModelForm):
    class Meta:
        model = FotoPaciente
        fields = ["paciente", "imagen", "descripcion"]
        widgets = {
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Descripción (opcional)",
                }
            ),
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get("imagen")
        if imagen:
            # Validar que el archivo sea una imagen
            if not imagen.content_type.startswith("image/"):
                raise forms.ValidationError("El archivo debe ser una imagen válida.")

            # Validar tamaño máximo (5MB)
            if imagen.size > 5 * 1024 * 1024:
                raise forms.ValidationError("La imagen no puede ser mayor a 5MB.")

            # Validar extensiones permitidas
            allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
            import os

            ext = os.path.splitext(imagen.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    "Solo se permiten archivos de imagen (JPG, PNG, GIF, BMP)."
                )

        return imagen
