from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.conf import settings

from weasyprint import HTML

from solicitudes.models import EntregaAyuda


def generar_pdf_recibo(entrega: EntregaAyuda):



    logo = Path(settings.STATICFILES_DIRS[0]) / "img" / "logo_muni.png"

    contexto = {
        "entrega": entrega,
        "persona": entrega.persona,
        "ayuda": entrega.ayuda,
        "secretaria": entrega.ayuda.secretaria,
        "fecha": entrega.fecha,
        "logo": logo.as_uri(),
    }

    html = render_to_string(
        "solicitudes/recibo_ayuda.html",
        contexto
    )

    pdf = HTML(
        string=html,
        base_url=settings.MEDIA_ROOT
    ).write_pdf()

    nombre_archivo = (
        f"comprobante_"
        f"{entrega.persona.dni}_"
        f"{entrega.fecha.strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    entrega.pdf_recibo.save(
        nombre_archivo,
        ContentFile(pdf),
        save=True
    )

    return entrega.pdf_recibo.path