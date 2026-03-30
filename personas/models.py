from django.db import models


class Persona(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    barrio = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - DNI {self.dni}"


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