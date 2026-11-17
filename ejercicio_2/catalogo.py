"""Ejercicio 2 - Modelo de productos, excepciones y persistencia."""

import json


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock inválido (negativo o no entero)."""

    def __init__(self, valor, mensaje="El stock no puede ser negativo"):
        self.valor = valor
        self.mensaje = mensaje
        super().__init__(f"{mensaje}: {valor!r}")


class DispositivoEcológico:
    """Clase base de los productos ecológicos del catálogo."""

    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0          # atributo privado (name mangling)
        self.stock = stock        # pasa por el setter, que valida

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise StockInvalidoError(valor, "El stock debe ser un número entero")
        if valor < 0:
            raise StockInvalidoError(valor)
        self.__stock = valor

    def ficha_tecnica(self):
        return (
            f"[{self.codigo}] {self.nombre}\n"
            f"  Precio: ${self.precio:,.2f} | Stock: {self.stock} unidades"
        )

    def to_dict(self):
        return {
            "tipo": type(self).__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcológico):
    """Panel solar: agrega potencia y eficiencia mediante herencia."""

    def __init__(self, codigo, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia  # porcentaje, ej. 21.5

    # Polimorfismo: redefine la ficha técnica
    def ficha_tecnica(self):
        return (
            f"PANEL SOLAR [{self.codigo}] {self.nombre}\n"
            f"  Potencia: {self.potencia_w} W | Eficiencia: {self.eficiencia}%\n"
            f"  Precio: ${self.precio:,.2f} | Stock: {self.stock} unidades"
        )

    def to_dict(self):
        datos = super().to_dict()
        datos.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return datos


class GestorInventario:
    """Gestiona la persistencia del catálogo."""

    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        datos = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)


def ejercicio_2():
    catalogo = [
        DispositivoEcológico("EC-001", "Cargador solar portátil", 4500.0, 25),
        PanelSolar("PS-100", "Panel Monocristalino 450W", 185000.0, 10, 450, 21.5),
    ]

    # Intento de creación con stock erróneo
    try:
        catalogo.append(PanelSolar("PS-200", "Panel defectuoso", 99000.0, -5, 300, 18.0))
    except StockInvalidoError as e:
        print(f"[ERROR CAPTURADO] No se creó el producto: {e}")

    # Intento de asignación errónea sobre un objeto existente
    try:
        catalogo[0].stock = -10
    except StockInvalidoError as e:
        print(f"[ERROR CAPTURADO] Asignación rechazada: {e}")
    print(f"Stock de {catalogo[0].codigo} se mantiene en {catalogo[0].stock}\n")

    # Polimorfismo
    for dispositivo in catalogo:
        print(dispositivo.ficha_tecnica())
        print()

    GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Catálogo exportado: {len(catalogo)} productos en catalogo_ecotech.json")


if __name__ == "__main__":
    ejercicio_2()
