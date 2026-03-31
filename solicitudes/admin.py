from django.contrib import admin
from .models import EntregaAyuda, EntregaAyudaConviviente


class EntregaAyudaConvivienteInline(admin.TabularInline):
    model = EntregaAyudaConviviente
    extra = 0
    can_delete = False


@admin.register(EntregaAyuda)
class EntregaAyudaAdmin(admin.ModelAdmin):
    list_display = ("id", "persona", "ayuda", "usuario", "fecha")
    search_fields = ("persona__dni", "persona__nombre", "persona__apellido")
    list_filter = ("ayuda__secretaria", "fecha")
    inlines = [EntregaAyudaConvivienteInline]