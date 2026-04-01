from django import forms
from .models import Ayuda


class AyudaForm(forms.ModelForm):
    class Meta:
        model = Ayuda
        fields = ["nombre", "descripcion", "activa"]