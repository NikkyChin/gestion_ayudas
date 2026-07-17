from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import get_object_or_404

from .models import Ayuda, Secretaria, ConfiguracionCorreo
from .forms import ConfiguracionCorreoAdminForm
from solicitudes.services.email_service import enviar_email_prueba

@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)


@admin.register(Ayuda)
class AyudaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "secretaria", "activa")
    search_fields = ("nombre", "secretaria__nombre")
    list_filter = ("secretaria", "activa")


@admin.register(ConfiguracionCorreo)
class ConfiguracionCorreoAdmin(admin.ModelAdmin):

    form = ConfiguracionCorreoAdminForm

    list_display = (
        "secretaria",
        "email",
        "activo",
        "actualizado",
    )

    search_fields = (
        "secretaria__nombre",
        "email",
    )

    list_filter = (
        "activo",
    )

    readonly_fields = (
        "creado",
        "actualizado",
    )

    fieldsets = (
        (
            "Secretaría",
            {
                "fields": (
                    "secretaria",
                    "activo",
                )
            },
        ),
        (
            "Remitente",
            {
                "fields": (
                    "nombre_remitente",
                    "email",
                    "password",
                )
            },
        ),
        (
            "Servidor SMTP",
            {
                "fields": (
                    "smtp_host",
                    "smtp_port",
                    "usar_tls",
                )
            },
        ),
        (
            "Información",
            {
                "fields": (
                    "creado",
                    "actualizado",
                )
            },
        ),
    )

    change_form_template = "admin/secretarias/configuracioncorreo/change_form.html"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:config_id>/probar-envio/",
                self.admin_site.admin_view(self.probar_envio),
                name="secretarias_configuracioncorreo_probar_envio",
            ),
        ]

        return custom_urls + urls

    def probar_envio(self, request, config_id):

        config = get_object_or_404(
            ConfiguracionCorreo,
            pk=config_id
        )

        try:
            enviar_email_prueba(config)

            messages.success(
                request,
                "Correo de prueba enviado correctamente."
            )

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

        return HttpResponseRedirect(
            request.META.get(
                "HTTP_REFERER",
                "../"
            )
        )