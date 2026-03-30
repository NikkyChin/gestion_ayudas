from django.db import models
from django.contrib.auth.models import User
from personas.models import Persona
from secretarias.models import Ayuda


class SolicitudAyuda(models.Model):

    ESTADO_CHOICES = [
        ("OTORGADA", "Otorgada"),
        ("RECHAZADA", "Rechazada"),
    ]

    persona = models.ForeignKey(
        Persona,
        on_delete=models.PROTECT,
        related_name="solicitudes"
    )

    ayuda = models.ForeignKey(
        Ayuda,
        on_delete=models.PROTECT
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    fecha = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES
    )

    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Solicitud de ayuda"
        verbose_name_plural = "Solicitudes de ayuda"

    def __str__(self):
        return f"{self.persona} - {self.ayuda} - {self.estado}"