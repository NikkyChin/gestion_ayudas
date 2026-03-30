from django.contrib import admin
from .models import Persona, Conviviente


class ConvivienteInline(admin.TabularInline):
    model = Conviviente
    extra = 1


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("dni", "apellido", "nombre", "barrio", "activa")
    search_fields = ("dni", "nombre", "apellido")
    list_filter = ("barrio", "activa")
    inlines = [ConvivienteInline]


@admin.register(Conviviente)
class ConvivienteAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "dni", "parentesco", "persona")
    search_fields = ("dni", "nombre", "apellido", "persona__nombre", "persona__apellido")
    list_filter = ("parentesco",)