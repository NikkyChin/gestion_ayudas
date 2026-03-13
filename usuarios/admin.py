from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "secretaria", "es_admin_general")
    search_fields = ("user__username",)
    list_filter = ("secretaria", "es_admin_general")