from django import forms
from django.core.exceptions import ValidationError
from .models import Persona
from .constants import BARRIOS_CHOICES
import re


class PersonaForm(forms.ModelForm):

    barrio = forms.ChoiceField(
        choices=[("", "---------")] + BARRIOS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )
    class Meta:
        model = Persona
        fields = [
            "dni",
            "nombre",
            "apellido",
            "direccion",
            "barrio",
            "telefono",
            "observaciones",
            "email",
            "encuesta_social_pendiente",
            "activa",
        ]

        widgets = {
            "dni": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese DNI",
                "min": "1000000",
                "max": "99999999",
            }),

            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese nombre",
                "minlength": "2",
                "maxlength": "50",
            }),

            "apellido": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese apellido",
                "minlength": "2",
                "maxlength": "50",
            }),

            "direccion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese dirección",
                "maxlength": "100",
            }),

            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese teléfono",
                "pattern": "[0-9]+",
                "maxlength": "15",
            }),

            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "maxlength": "500",
                "placeholder": "Observaciones adicionales",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Ingrese correo electrónico",
            }),
        }

    def clean_dni(self):
        dni = str(self.cleaned_data["dni"]).strip()

        if not dni.isdigit():
            raise ValidationError(
                "El DNI solo debe contener números."
            )

        if len(dni) < 7 or len(dni) > 8:
            raise ValidationError(
                "El DNI debe tener entre 7 y 8 dígitos."
            )

        return dni

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if len(nombre) < 2:
            raise ValidationError(
                "El nombre es demasiado corto."
            )

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
            raise ValidationError(
                "El nombre solo puede contener letras."
            )

        return nombre.title()

    def clean_apellido(self):
        apellido = self.cleaned_data["apellido"].strip()

        if len(apellido) < 2:
            raise ValidationError(
                "El apellido es demasiado corto."
            )

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", apellido):
            raise ValidationError(
                "El apellido solo puede contener letras."
            )

        return apellido.title()

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"].strip()

        telefono_limpio = (
            telefono.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if not telefono_limpio.isdigit():
            raise ValidationError(
                "El teléfono solo debe contener números."
            )

        if len(telefono_limpio) < 8:
            raise ValidationError(
                "El teléfono ingresado no es válido."
            )

        return telefono

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            email = email.strip()

            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                raise ValidationError(
                    "El correo electrónico ingresado no es válido."
                )

        return email
    
    def clean(self):
        cleaned_data = super().clean()

        direccion = cleaned_data.get("direccion")
        barrio = cleaned_data.get("barrio")

        if direccion:
            cleaned_data["direccion"] = direccion.strip().title()

        if barrio:
            cleaned_data["barrio"] = barrio.strip().title()

        return cleaned_data