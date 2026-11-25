# Metodología Waterfall - Generador de Contratos

## 1. Análisis de requisitos
Identificar datos del cliente y del crédito, cálculo de amortización, validación, generación PDF, envío por correo y documentación API.

## 2. Diseño
Separar frontend (HTML/CSS) y backend (Flask, Pydantic, amortización, ReportLab y SMTP). Definir endpoints y esquema OpenAPI para Swagger.

## 3. Implementación
Construir el formulario, las rutas Flask, validaciones, cálculo financiero, PDF y envío Gmail. Gestionar configuración privada con `.env`.

## 4. Pruebas
Ejecutar pruebas automatizadas con pytest: salud API, amortización válida e inválida, generación PDF y envío simulado desde el formulario.

## 5. Entrega y mantenimiento
Entregar el código organizado para Visual Studio Code, documentar instalación y configuración, y mantener las credenciales fuera del código fuente.
