"""Punto de entrada Flask. Ejecutar con: python app.py"""
from pathlib import Path
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from backend.routes import rutas
from backend.config import Config

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"

def crear_aplicacion(configuracion=None):
    app = Flask(
        __name__,
        template_folder=str(FRONTEND_DIR / "templates"),
        static_folder=str(FRONTEND_DIR / "static"),
    )
    app.config.from_object(Config)
    if configuracion:
        app.config.update(configuracion)
    app.register_blueprint(rutas)
    swaggerui = get_swaggerui_blueprint(
        "/docs", "/static/openapi.yaml",
        config={"app_name": "Generador de contratos - API"}
    )
    app.register_blueprint(swaggerui, url_prefix="/docs")

    @app.route("/")
    def inicio():
        return jsonify({
            "proyecto": "Generador de contratos",
            "interfaz": "/contrato",
            "documentacion": "/docs",
            "salud": "/api/salud"
        })

    @app.errorhandler(404)
    def no_encontrado(error):
        return jsonify({"error": "Ruta no encontrada"}), 404
    return app

app = crear_aplicacion()

if __name__ == "__main__":
    print("Frontend: http://127.0.0.1:5000/contrato")
    print("Swagger: http://127.0.0.1:5000/docs")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
