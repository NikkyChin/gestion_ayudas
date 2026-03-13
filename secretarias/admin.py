from django.contrib import admin
from .models import Ayuda, Secretaria

@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)


@admin.register(Ayuda)
class AyudaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "secretaria", "activa")
    search_fields = ("nombre", "secretaria__nombre")
    list_filter = ("secretaria", "activa")