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
    secretaria = models.ForeignKey(
        Secretaria,
        on_delete=models.PROTECT,
        related_name="ayudas"
    )

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


class Oficina(models.Model):

    secretaria = models.ForeignKey(
        Secretaria,
        on_delete=models.CASCADE,
        related_name="oficinas"
    )

    nombre = models.CharField(
        max_length=100
    )

    activa = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Oficina"
        verbose_name_plural = "Oficinas"
        ordering = ["nombre"]
        unique_together = ("secretaria", "nombre")

    def __str__(self):
        return f"{self.nombre} - {self.secretaria.nombre}"

class ConfiguracionCorreo(models.Model):
    secretaria = models.OneToOneField(
        Secretaria,
        on_delete=models.CASCADE,
        related_name="configuracion_correo"
    )

    nombre_remitente = models.CharField(
        max_length=150,
        help_text="Nombre que verá el destinatario.",
        blank=True
    )

    email = models.EmailField(
        unique=True,
        blank=True
    )

    password = models.CharField(
        max_length=255,
        blank=True
    )

    smtp_host = models.CharField(
        max_length=100,
        default="smtp.gmail.com"
    )

    smtp_port = models.PositiveIntegerField(
        default=587
    )

    usar_tls = models.BooleanField(
        default=True
    )

    activo = models.BooleanField(
        default=True
    )

    creado = models.DateTimeField(
        auto_now_add=True
    )

    actualizado = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Configuración de correo"
        verbose_name_plural = "Configuraciones de correo"

    def __str__(self):
        if self.email:
            return f"{self.secretaria.nombre} ({self.email})"
        return self.secretaria.nombre