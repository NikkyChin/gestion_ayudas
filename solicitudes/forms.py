from django import forms
from .models import EntregaAyuda


class EntregaAyudaForm(forms.ModelForm):
    class Meta:
        model = EntregaAyuda
        fields = ["ayuda", "descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }