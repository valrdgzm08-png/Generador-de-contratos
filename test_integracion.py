import io
from app import crear_aplicacion

def cliente_prueba():
    app = crear_aplicacion({"TESTING": True})
    return app.test_client()

def test_salud():
    respuesta = cliente_prueba().get("/api/salud")
    assert respuesta.status_code == 200
    assert respuesta.json["estado"] == "correcto"

def test_amortizacion_correcta():
    respuesta = cliente_prueba().post("/api/amortizacion", json={
        "monto": 100000, "tasa_anual": 12, "plazo_meses": 12
    })
    assert respuesta.status_code == 200
    assert len(respuesta.json["tabla_amortizacion"]) == 12
    assert respuesta.json["tabla_amortizacion"][-1]["saldo"] == 0

def test_amortizacion_invalida():
    respuesta = cliente_prueba().post("/api/amortizacion", json={
        "monto": -1, "tasa_anual": 12, "plazo_meses": 12
    })
    assert respuesta.status_code == 400

def test_generar_pdf():
    respuesta = cliente_prueba().post("/api/contrato", json={
        "nombre_cliente": "Ana Lopez",
        "identificacion": "ABC12345",
        "correo": "ana@example.com",
        "monto": 100000,
        "tasa_anual": 12,
        "plazo_meses": 12
    })
    assert respuesta.status_code == 200
    assert respuesta.mimetype == "application/pdf"
    assert respuesta.data.startswith(b"%PDF")


def test_formulario_genera_pdf_y_envia_el_mismo_archivo(monkeypatch):
    from backend import routes
    enviados = {}

    def correo_falso(destinatario, nombre_cliente, pdf_bytes):
        enviados["destinatario"] = destinatario
        enviados["nombre"] = nombre_cliente
        enviados["pdf"] = pdf_bytes

    monkeypatch.setattr(routes, "enviar_pdf_por_correo", correo_falso)
    respuesta = cliente_prueba().post("/contrato", data={
        "nombre_cliente": "Cliente Desde Formulario",
        "identificacion": "ID123456",
        "correo": "cliente@example.com",
        "monto": "25000",
        "tasa_anual": "10",
        "plazo_meses": "12"
    })
    assert respuesta.status_code == 200
    assert respuesta.mimetype == "application/pdf"
    assert respuesta.data.startswith(b"%PDF")
    assert enviados["destinatario"] == "cliente@example.com"
    assert enviados["nombre"] == "Cliente Desde Formulario"
    assert enviados["pdf"] == respuesta.data
