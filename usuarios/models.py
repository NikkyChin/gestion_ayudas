from django.db import models
from django.contrib.auth.models import User
from secretarias.models import Secretaria

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    secretaria = models.ForeignKey(Secretaria, on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios")

    es_admin_general = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username