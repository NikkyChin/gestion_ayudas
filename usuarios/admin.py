from django.contrib import admin
from .models import PerfilUsuario, Oficina


@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "secretaria", "activa")
    search_fields = ("nombre",)
    list_filter = ("secretaria", "activa")


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "secretaria",
        "oficina",
        "es_admin_area",
        "es_admin_general",
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "secretaria",
        "oficina",
        "es_admin_area",
        "es_admin_general",
    )