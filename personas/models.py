from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):

    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    observaciones = models.TextField(blank=True)
    email = models.EmailField("Correo electrónico", blank=True, null=True)

    encuesta_social_pendiente = models.BooleanField(default=False)

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personas_creadas"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    modificado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personas_modificadas"
    )

    fecha_modificacion = models.DateTimeField(
        auto_now=True
    )

    activa = models.BooleanField(default=True)


class Conviviente(models.Model):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="convivientes"
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True)
    parentesco = models.CharField(max_length=50, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "Conviviente"
        verbose_name_plural = "Convivientes"

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.parentesco})"