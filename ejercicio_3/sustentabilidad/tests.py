import unittest

from django.test import TestCase
from django.urls import reverse

from .calculos import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """Auditoría de calcular_emisiones_carbono."""

    def test_calculo_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_calculo_con_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100, 0.5), 50.0)

    def test_consumo_decimal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(250.5), 100.2)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_mensaje_de_error_consumo_negativo(self):
        with self.assertRaises(ValueError) as ctx:
            calcular_emisiones_carbono(-50)
        self.assertIn("negativo", str(ctx.exception))


class TestMetricasConsumo(unittest.TestCase):
    def setUp(self):
        self.registros = [
            {"planta": "Norte", "consumo_kwh": 1200},
            {"planta": "Sur", "consumo_kwh": 1500},
            {"planta": "Norte", "consumo_kwh": 800},
        ]

    def test_total_y_planta_mayor(self):
        m = obtener_metricas_consumo(self.registros)
        self.assertAlmostEqual(m["total_emisiones"], 1400.0)
        self.assertEqual(m["planta_mayor_consumo"], "Norte")

    def test_sin_registros(self):
        m = obtener_metricas_consumo([])
        self.assertEqual(m["total_emisiones"], 0)
        self.assertIsNone(m["planta_mayor_consumo"])

    def test_consumo_negativo_propaga_error(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "X", "consumo_kwh": -5}])


class TestVistaPanel(TestCase):
    def test_vista_responde_y_usa_plantilla(self):
        respuesta = self.client.get(reverse("panel_sustentabilidad"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")
        self.assertEqual(respuesta.context["planta_mayor_consumo"], "Planta Norte")
        self.assertAlmostEqual(respuesta.context["total_emisiones"], 1600.0)
