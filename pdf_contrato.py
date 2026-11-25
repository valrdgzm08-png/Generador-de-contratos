"""
Generacion del contrato PDF con ReportLab.
"""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generar_pdf_contrato(datos: dict, resultados: dict) -> bytes:
    """Crea el contrato y devuelve sus bytes para descargar o adjuntar."""
    memoria = BytesIO()
    documento = SimpleDocTemplate(
        memoria, pagesize=letter,
        rightMargin=1.7*cm, leftMargin=1.7*cm,
        topMargin=1.7*cm, bottomMargin=1.7*cm
    )
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle("TituloContrato", parent=estilos["Title"],
                            textColor=colors.HexColor("#17365D"), fontSize=17)
    elementos = [
        Paragraph("CONTRATO DE CREDITO", titulo),
        Spacer(1, 12),
        Paragraph(
            "Este documento es un formato de ejemplo generado por el sistema. "
            "Debe revisarse y adaptarse legalmente antes de utilizarse como contrato vinculante.",
            estilos["BodyText"]
        ),
        Spacer(1, 14),
        Paragraph("<b>DATOS DE LAS PARTES</b>", estilos["Heading2"]),
        Paragraph(f"Cliente: {datos['nombre_cliente']}", estilos["BodyText"]),
        Paragraph(f"Identificacion: {datos['identificacion']}", estilos["BodyText"]),
        Paragraph(f"Correo: {datos['correo']}", estilos["BodyText"]),
        Spacer(1, 12),
        Paragraph("<b>CONDICIONES FINANCIERAS</b>", estilos["Heading2"]),
    ]
    filas = [
        ["Concepto", "Importe / dato"],
        ["Monto del credito", f"${resultados['monto_credito']:,.2f} MXN"],
        ["Tasa anual", f"{resultados['tasa_anual']:.2f}%"],
        ["Plazo", f"{resultados['plazo_meses']} meses"],
        ["Mensualidad aproximada", f"${resultados['mensualidad']:,.2f} MXN"],
        ["Intereses totales", f"${resultados['total_intereses']:,.2f} MXN"],
        ["Total pagado", f"${resultados['total_pagado']:,.2f} MXN"],
    ]
    tabla = Table(filas, colWidths=[8*cm, 8*cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elementos.extend([
        tabla, Spacer(1, 18),
        Paragraph(
            "Las partes manifiestan que revisaran las condiciones, fechas, "
            "obligaciones, intereses y demas clausulas antes de firmar.",
            estilos["BodyText"]
        ),
        Spacer(1, 32),
        Paragraph("______________________________　　　______________________________", estilos["BodyText"]),
        Paragraph("Firma del cliente　　　　　　　　　　 Firma de la institucion", estilos["BodyText"])
    ])
    documento.build(elementos)
    return memoria.getvalue()
