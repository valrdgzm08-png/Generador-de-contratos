"""
Motor financiero: amortizacion francesa y tabla de pagos.
"""
from .schemas import CreditoRequest

def validar_credito(Monto_credito: float, Tasa_anual: float, Plazo_meses: int) -> bool:
    """Valida los datos del credito con el esquema Pydantic."""
    try:
        CreditoRequest(monto=Monto_credito, tasa_anual=Tasa_anual,
                      plazo_meses=Plazo_meses)
        return True
    except Exception:
        return False

def calcular_amortizacion(Monto_credito: float, Tasa_anual: float,
                          Plazo_meses: int) -> dict:
    """
    Calcula la amortizacion francesa.
    Retorna mensualidad, totales y tabla_amortizacion.
    """
    datos = CreditoRequest(monto=Monto_credito, tasa_anual=Tasa_anual,
                           plazo_meses=Plazo_meses)
    tasa_mensual = datos.tasa_anual / 100 / 12
    saldo = round(datos.monto, 2)

    if tasa_mensual == 0:
        mensualidad = round(saldo / datos.plazo_meses, 2)
    else:
        factor = (1 + tasa_mensual) ** datos.plazo_meses
        mensualidad = round(saldo * tasa_mensual * factor / (factor - 1), 2)

    tabla_amortizacion = []
    total_intereses = 0.0
    total_pagado = 0.0

    for mes in range(1, datos.plazo_meses + 1):
        interes = round(saldo * tasa_mensual, 2)
        if mes == datos.plazo_meses:
            cuota = round(saldo + interes, 2)
        else:
            cuota = mensualidad
        capital = round(cuota - interes, 2)
        nuevo_saldo = round(saldo - capital, 2)
        if mes == datos.plazo_meses:
            nuevo_saldo = 0.0

        tabla_amortizacion.append({
            "mes": mes,
            "cuota": cuota,
            "interes": interes,
            "capital": capital,
            "saldo": nuevo_saldo
        })
        total_intereses = round(total_intereses + interes, 2)
        total_pagado = round(total_pagado + cuota, 2)
        saldo = nuevo_saldo

    return {
        "monto_credito": round(datos.monto, 2),
        "tasa_anual": datos.tasa_anual,
        "plazo_meses": datos.plazo_meses,
        "mensualidad": mensualidad,
        "total_intereses": total_intereses,
        "total_pagado": total_pagado,
        "tabla_amortizacion": tabla_amortizacion
    }
