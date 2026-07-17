from django.core.mail import EmailMessage, get_connection
from django.utils import timezone

from secretarias.models import ConfiguracionCorreo


def obtener_conexion(secretaria):
    """
    Devuelve una conexión SMTP según la configuración
    de la secretaría.
    """

    config = ConfiguracionCorreo.objects.get(
        secretaria=secretaria,
        activo=True,
    )

    connection = get_connection(
        host=config.smtp_host,
        port=config.smtp_port,
        username=config.email,
        password=config.password,
        use_tls=config.usar_tls,
    )

    return connection, config


def enviar_comprobante(entrega):
    """
    Envía el comprobante PDF al beneficiario.
    """

    connection, config = obtener_conexion(entrega.ayuda.secretaria)

    try:

        asunto = "Comprobante de entrega de ayuda"

        mensaje = f"""
Estimado/a {entrega.persona.nombre}:

Adjuntamos el comprobante correspondiente a la ayuda recibida.

Este correo fue generado automáticamente por el Sistema de Gestión Social de la Municipalidad de Rawson.

Por favor, no responder este correo.
        """

        email = EmailMessage(
            subject=asunto,
            body=mensaje,
            from_email=f"{config.nombre_remitente} <{config.email}>",
            to=[entrega.persona.email],
            connection=connection,
        )

        email.attach_file(entrega.pdf_recibo.path)

        email.send()

        entrega.email_enviado = True
        entrega.fecha_envio_email = timezone.now()
        entrega.error_envio = ""

    except Exception as e:

        entrega.email_enviado = False
        entrega.error_envio = str(e)

        raise

    finally:

        entrega.save(
            update_fields=[
                "email_enviado",
                "fecha_envio_email",
                "error_envio",
            ]
        )

        connection.close()


def enviar_email_prueba(config):
    """
    Envía un correo de prueba utilizando la configuración SMTP
    de la secretaría.
    """

    connection = get_connection(
        host=config.smtp_host,
        port=config.smtp_port,
        username=config.email,
        password=config.password,
        use_tls=config.usar_tls,
    )

    try:

        email = EmailMessage(
            subject="Prueba de configuración de correo",
            body=(
                "Este es un correo de prueba enviado desde el "
                "Sistema de Gestión Social.\n\n"
                "Si recibió este mensaje, la configuración SMTP "
                "es correcta."
            ),
            from_email=f"{config.nombre_remitente} <{config.email}>",
            to=[config.email],
            connection=connection,
        )

        email.send()

    finally:

        connection.close()
