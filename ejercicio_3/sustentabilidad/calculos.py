def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Emisiones de CO2 (kg) = consumo (kWh) * factor de emisión (kg CO2/kWh)."""
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros, factor_emision=0.4):
    """
    Procesa un historial de consumos por planta.

    registros: lista de dicts, ej. [{"planta": "Norte", "consumo_kwh": 1200}, ...]
    Una misma planta puede aparecer varias veces (historial); se acumula.
    Propaga ValueError si algún registro tiene consumo negativo.
    """
    consumo_por_planta = {}
    emisiones_por_planta = {}

    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]
        emision = calcular_emisiones_carbono(consumo, factor_emision)  # valida cada registro
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + consumo
        emisiones_por_planta[planta] = emisiones_por_planta.get(planta, 0) + emision

    if consumo_por_planta:
        planta_mayor = max(consumo_por_planta, key=consumo_por_planta.get)
        consumo_mayor = consumo_por_planta[planta_mayor]
    else:
        planta_mayor, consumo_mayor = None, 0

    return {
        "total_emisiones": sum(emisiones_por_planta.values()),
        "planta_mayor_consumo": planta_mayor,
        "consumo_mayor_kwh": consumo_mayor,
        "consumo_por_planta": consumo_por_planta,
        "emisiones_por_planta": emisiones_por_planta,
    }
