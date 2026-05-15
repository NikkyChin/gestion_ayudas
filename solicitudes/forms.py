from django import forms
from django.core.exceptions import ValidationError
from .models import EntregaAyuda


class EntregaAyudaForm(forms.ModelForm):

    class Meta:
        model = EntregaAyuda
        fields = ["ayuda", "descripcion"]

        widgets = {
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "maxlength": "500",
                "placeholder": "Ingrese descripción de la entrega",
            }),
        }


    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()

        if len(descripcion) < 5:
            raise ValidationError(
                "La descripción es demasiado corta."
            )

        return descripcion