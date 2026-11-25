"""
Esquemas y validaciones de entrada con Pydantic.
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

class CreditoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    monto: float = Field(gt=0, description="Monto del credito en pesos")
    tasa_anual: float = Field(ge=0, le=100, description="Tasa anual en porcentaje")
    plazo_meses: int = Field(ge=1, le=600, description="Plazo entre 1 y 600 meses")

    @field_validator("monto", "tasa_anual")
    @classmethod
    def validar_valores_financieros(cls, valor):
        if not float(valor) < float("inf"):
            raise ValueError("El valor debe ser finito")
        return valor

class ContratoRequest(CreditoRequest):
    nombre_cliente: str = Field(min_length=3, max_length=120)
    identificacion: str = Field(min_length=4, max_length=40)
    correo: EmailStr

    @field_validator("nombre_cliente", "identificacion")
    @classmethod
    def limpiar_texto(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("Este campo no puede estar vacio")
        return valor
