from django.db import models

class Secretaria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Ayuda(models.Model):
    secretaria = models.ForeignKey(Secretaria, on_delete=models.PROTECT, related_name="ayudas")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ayuda"
        verbose_name_plural = "Ayudas"
        ordering = ["secretaria__nombre", "nombre"]
        unique_together = ("secretaria", "nombre")

    def __str__(self):
        return f"{self.nombre} - {self.secretaria.nombre}"