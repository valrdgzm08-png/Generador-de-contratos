"""Configuracion de la aplicacion y lectura segura del archivo .env."""
import os
from pathlib import Path
from dotenv import load_dotenv

# El .env se encuentra en la raiz del proyecto, un nivel arriba de backend/.
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-academica-cambiar-en-produccion")
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", "")
    SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
