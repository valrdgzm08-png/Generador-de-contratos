"""
Rutas web y API del generador de contratos.
"""
from flask import Blueprint, request, jsonify, render_template, send_file
from pydantic import ValidationError
from io import BytesIO
from .schemas import CreditoRequest, ContratoRequest
from .amortizacion import calcular_amortizacion
from .pdf_contrato import generar_pdf_contrato
from .correo import enviar_pdf_por_correo

rutas = Blueprint("rutas", __name__)

@rutas.route("/api/salud", methods=["GET"])
def salud():
    return jsonify({"estado": "correcto", "mensaje": "API funcionando"}), 200

@rutas.route("/api/amortizacion", methods=["POST"])
def api_amortizacion():
    try:
        datos = CreditoRequest.model_validate(request.get_json(force=True))
        resultado = calcular_amortizacion(datos.monto, datos.tasa_anual, datos.plazo_meses)
        return jsonify(resultado), 200
    except ValidationError as error:
        return jsonify({"error": "Datos invalidos", "detalles": error.errors()}), 400
    except Exception:
        return jsonify({"error": "No se pudo procesar la amortizacion"}), 400

@rutas.route("/contrato", methods=["GET"])
def formulario_contrato():
    return render_template("index.html")

@rutas.route("/contrato", methods=["POST"])
def descargar_contrato():
    """Genera el PDF con los datos del formulario, lo envia por correo y lo descarga."""
    try:
        datos = ContratoRequest.model_validate(request.form.to_dict())
        resultado = calcular_amortizacion(datos.monto, datos.tasa_anual, datos.plazo_meses)
        # Se genera una sola vez: estos mismos bytes se adjuntan al correo y se descargan.
        pdf = generar_pdf_contrato(datos.model_dump(), resultado)
        enviar_pdf_por_correo(str(datos.correo), datos.nombre_cliente, pdf)
        respuesta = send_file(
            BytesIO(pdf), mimetype="application/pdf", as_attachment=True,
            download_name="contrato_credito.pdf"
        )
        respuesta.headers["X-Contrato-Email"] = "enviado"
        return respuesta
    except ValidationError as error:
        return render_template("index.html", error="Revisa los datos: " + str(error)), 400
    except Exception as error:
        # No se muestra informacion de autenticacion ni contrasenas al usuario.
        return render_template(
            "index.html",
            error=("El PDF se pudo preparar, pero no se pudo enviar por correo. "
                   "Revisa las variables SMTP y la conexion a Gmail. Detalle: "
                   + str(error))
        ), 500

@rutas.route("/api/contrato", methods=["POST"])
def api_contrato():
    try:
        datos = ContratoRequest.model_validate(request.get_json(force=True))
        resultado = calcular_amortizacion(datos.monto, datos.tasa_anual, datos.plazo_meses)
        pdf = generar_pdf_contrato(datos.model_dump(), resultado)
        return send_file(BytesIO(pdf), mimetype="application/pdf",
                         as_attachment=True, download_name="contrato_credito.pdf")
    except ValidationError as error:
        return jsonify({"error": "Datos invalidos", "detalles": error.errors()}), 400

@rutas.route("/api/enviar-contrato", methods=["POST"])
def api_enviar_contrato():
    try:
        datos = ContratoRequest.model_validate(request.get_json(force=True))
        resultado = calcular_amortizacion(datos.monto, datos.tasa_anual, datos.plazo_meses)
        pdf = generar_pdf_contrato(datos.model_dump(), resultado)
        enviar_pdf_por_correo(str(datos.correo), datos.nombre_cliente, pdf)
        return jsonify({"mensaje": "Contrato enviado correctamente."}), 200
    except ValidationError as error:
        return jsonify({"error": "Datos invalidos", "detalles": error.errors()}), 400
    except (RuntimeError, OSError, Exception) as error:
        return jsonify({"error": "No se pudo enviar el correo.", "detalle": str(error)}), 500
