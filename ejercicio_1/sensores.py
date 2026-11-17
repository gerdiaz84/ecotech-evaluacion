"""Ejercicio 1 - Sanitización y análisis estadístico de sensores."""

import re

UBICACION_POR_DEFECTO = "Desconocida"


def limpiar_registro_sensor(registro_raw):
    """
    Normaliza un registro crudo de sensor.

    - sensor_id: string sin espacios sobrantes.
    - temperatura: float sin sufijos de unidad (None si no se puede interpretar).
    - ubicacion: string sin espacios; "Desconocida" si falta o está vacía.
    """
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    temp_raw = str(registro_raw.get("temperatura", "")).strip().replace(",", ".")
    coincidencia = re.search(r"-?\d+(?:\.\d+)?", temp_raw)
    temperatura = float(coincidencia.group()) if coincidencia else None

    ubicacion = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion).strip() if ubicacion is not None else ""
    if not ubicacion:
        ubicacion = UBICACION_POR_DEFECTO

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Retorna (lista_sensores_alerta, promedio_temperatura).

    - lista_sensores_alerta: IDs cuya temperatura supera estrictamente el umbral.
    - promedio_temperatura: promedio global (0.0 si no hay lecturas válidas).
    Los registros con temperatura None se ignoran.
    """
    validos = [s for s in lista_sensores_limpios if s["temperatura"] is not None]

    lista_sensores_alerta = [
        s["sensor_id"] for s in validos if s["temperatura"] > umbral_temperatura
    ]
    promedio_temperatura = (
        sum(s["temperatura"] for s in validos) / len(validos) if validos else 0.0
    )
    return lista_sensores_alerta, promedio_temperatura


def ejercicio_1():
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002  ", "temperatura": " 31.2 °C", "ubicacion": "  Planta Sur "},
        {"sensor_id": "  SENSOR-003", "temperatura": "28,7C"},                         # sin ubicación
        {"sensor_id": "SENSOR-004", "temperatura": "35.0C", "ubicacion": ""},          # ubicación vacía
        {"sensor_id": " SENSOR-005 ", "temperatura": "error", "ubicacion": "Bodega"},  # lectura inválida
    ]
    umbral = 30.0

    sensores_limpios = [limpiar_registro_sensor(r) for r in registros_crudos]
    alertas, promedio = generar_resumen_sensores(sensores_limpios, umbral)

    print("=" * 50)
    print("     REPORTE TÉRMICO - ECOTECH SOLUTIONS")
    print("=" * 50)
    print(f"{'ID':<14}{'Temp (°C)':>10}  {'Ubicación'}")
    print("-" * 50)
    for s in sensores_limpios:
        temp = f"{s['temperatura']:.1f}" if s["temperatura"] is not None else "N/D"
        print(f"{s['sensor_id']:<14}{temp:>10}  {s['ubicacion']}")
    print("-" * 50)
    print(f"Umbral de alerta:     {umbral:.1f} °C")
    print(f"Sensores en alerta:   {', '.join(alertas) if alertas else 'Ninguno'}")
    print(f"Promedio de planta:   {promedio:.2f} °C")
    print("=" * 50)


if __name__ == "__main__":
    ejercicio_1()
