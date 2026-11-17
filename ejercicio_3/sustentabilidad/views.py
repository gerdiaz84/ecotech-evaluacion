from django.shortcuts import render

from .calculos import obtener_metricas_consumo

# Historial de ejemplo; en producción vendría de una base de datos o API.
REGISTROS_CONSUMO = [
    {"planta": "Planta Norte", "consumo_kwh": 1200},
    {"planta": "Planta Sur", "consumo_kwh": 1500},
    {"planta": "Planta Norte", "consumo_kwh": 800},
    {"planta": "Planta Este", "consumo_kwh": 500},
]


def vista_panel_sustentabilidad(request):
    metricas = obtener_metricas_consumo(REGISTROS_CONSUMO)

    plantas = [
        {
            "nombre": nombre,
            "consumo_kwh": consumo,
            "emisiones_kg": metricas["emisiones_por_planta"][nombre],
        }
        for nombre, consumo in metricas["consumo_por_planta"].items()
    ]

    contexto = {
        "titulo": "Panel de Sustentabilidad - EcoTech Solutions",
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "consumo_mayor_kwh": metricas["consumo_mayor_kwh"],
        "plantas": plantas,
    }
    return render(request, "sustentabilidad/panel.html", contexto)
