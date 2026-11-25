"""
Envio de contratos PDF por SMTP.
"""
import smtplib
from email.message import EmailMessage
from .config import Config

def enviar_pdf_por_correo(destinatario: str, nombre_cliente: str, pdf_bytes: bytes) -> None:
    """Envia un PDF adjunto. Requiere configurar variables SMTP."""
    if not all([Config.SMTP_HOST, Config.SMTP_USER, Config.SMTP_PASSWORD, Config.SMTP_FROM]):
        raise RuntimeError("Falta configurar SMTP_HOST, SMTP_USER, SMTP_PASSWORD o SMTP_FROM.")

    mensaje = EmailMessage()
    mensaje["Subject"] = "Contrato de credito"
    mensaje["From"] = Config.SMTP_FROM
    mensaje["To"] = destinatario
    mensaje.set_content(
        f"Hola {nombre_cliente},\\n\\nAdjuntamos el PDF de tu contrato de credito. "
        "Revisa su contenido antes de firmarlo.\\n"
    )
    mensaje.add_attachment(pdf_bytes, maintype="application", subtype="pdf",
                           filename="contrato_credito.pdf")

    servidor = None
    try:
        if Config.SMTP_USE_SSL:
            servidor = smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT, timeout=20)
        else:
            servidor = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=20)
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
        servidor.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        servidor.send_message(mensaje)
    finally:
        if servidor is not None:
            try:
                servidor.quit()
            except Exception:
                servidor.close()
