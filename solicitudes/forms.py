from django import forms
from django.core.exceptions import ValidationError

from .models import EntregaAyuda


class EntregaAyudaForm(forms.ModelForm):

    class Meta:
        model = EntregaAyuda

        fields = [
            "numero_recibo",
            "ayuda",
            "descripcion",
        ]

        widgets = {
            "numero_recibo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: 12345",
                    "maxlength": "30",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": "500",
                    "placeholder": "Ingrese descripción de la entrega",
                }
            ),
        }

    def clean_numero_recibo(self):
        numero = self.cleaned_data["numero_recibo"].strip()

        # Si el campo es opcional
        if not numero:
            return numero

        if len(numero) > 30:
            raise ValidationError(
                "El número de recibo es demasiado largo."
            )

        return numero

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()

        if len(descripcion) < 5:
            raise ValidationError(
                "La descripción es demasiado corta."
            )

        return descripcion