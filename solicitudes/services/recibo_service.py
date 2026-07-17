from .pdf_service import generar_pdf_recibo
from .email_service import enviar_comprobante


def procesar_recibo(entrega, regenerar_pdf=False):
    """
    Genera el comprobante (si es necesario) y lo envía por email.
    """

    try:

        if regenerar_pdf or not entrega.pdf_recibo:
            generar_pdf_recibo(entrega)

        if entrega.persona.email:
            enviar_comprobante(entrega)

    except Exception as e:

        entrega.email_enviado = False
        entrega.error_envio = str(e)

        entrega.save(
            update_fields=[
                "email_enviado",
                "error_envio",
            ]
        )

        raise