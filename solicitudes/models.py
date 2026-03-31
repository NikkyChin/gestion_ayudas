from django.db import models
from django.contrib.auth.models import User
from personas.models import Persona, Conviviente
from secretarias.models import Ayuda


class EntregaAyuda(models.Model):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.PROTECT,
        related_name="entregas"
    )
    ayuda = models.ForeignKey(
        Ayuda,
        on_delete=models.PROTECT,
        related_name="entregas"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="entregas_realizadas"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Entrega de ayuda"
        verbose_name_plural = "Entregas de ayuda"

    def __str__(self):
        return f"{self.persona} - {self.ayuda} - {self.fecha.strftime('%d/%m/%Y')}"


class EntregaAyudaConviviente(models.Model):
    entrega = models.ForeignKey(
        EntregaAyuda,
        on_delete=models.CASCADE,
        related_name="convivientes_relacionados"
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True)
    parentesco = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Conviviente relacionado"
        verbose_name_plural = "Convivientes relacionados"

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"