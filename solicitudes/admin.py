from django.contrib import admin
from .models import SolicitudAyuda


@admin.register(SolicitudAyuda)
class SolicitudAyudaAdmin(admin.ModelAdmin):
    list_display = ("id", "persona", "ayuda", "estado", "fecha", "usuario")
    search_fields = ("persona__nombre", "persona__apellido", "persona__dni")
    list_filter = ("estado", "ayuda__secretaria", "fecha")