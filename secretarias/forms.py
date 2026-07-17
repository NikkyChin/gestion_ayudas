from django import forms
from django.core.exceptions import ValidationError
from .models import Ayuda

from .models import ConfiguracionCorreo


class ConfiguracionCorreoAdminForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            render_value=True
        )
    )

    class Meta:
        model = ConfiguracionCorreo
        fields = "__all__"
        
class AyudaForm(forms.ModelForm):

    class Meta:
        model = Ayuda
        fields = ["nombre", "descripcion", "activa"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese nombre de la ayuda",
                "minlength": "3",
                "maxlength": "100",
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "maxlength": "500",
                "placeholder": "Ingrese descripción",
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 3:
            raise ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        return nombre.capitalize()

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()

        if len(descripcion) < 5:
            raise ValidationError(
                "La descripción es demasiado corta."
            )

        return descripcion