from typing import Tuple, List, Dict
import math

class DatosMeteorologicos:
    def __init__(self, nombre_archivo: str = 'datos.txt'):
        self.nombre_archivo = nombre_archivo

    def _direccion_viento_a_grados(self, direccion: str) -> float:
        direcciones = {
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90,
            'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180,
            'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270,
            'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }
        return direcciones.get(direccion, 0)

    def _grados_a_direccion(self, grados: float) -> str:
        direcciones = [
            ('N', 0), ('NNE', 22.5), ('NE', 45), ('ENE', 67.5), ('E', 90),
            ('ESE', 112.5), ('SE', 135), ('SSE', 157.5), ('S', 180),
            ('SSW', 202.5), ('SW', 225), ('WSW', 247.5), ('W', 270),
            ('WNW', 292.5), ('NW', 315), ('NNW', 337.5)
        ]
        # Encuentra la dirección más cercana al valor en grados
        return min(direcciones, key=lambda x: abs(grados - x[1]))[0]

    def procesar_datos(self) -> Tuple[float, float, float, float, str]:
        temperaturas = []
        humedades = []
        presiones = []
        velocidades_viento = []
        direcciones_viento = []

        with open(self.nombre_archivo, 'r') as archivo:
            while True:
                linea = archivo.readline()
                if not linea:
                    break  # Salir si no hay más líneas

                if linea.startswith("Temperatura:"):
                    # Extraer valores de la línea de Temperatura
                    temperatura = float(linea.split()[1])
                    humedad = float(archivo.readline().split()[1])
                    presion = float(archivo.readline().split()[1])
                    
                    # Leer la línea de Viento
                    linea_viento = archivo.readline().strip().split()
                    velocidad_viento, direccion_viento = linea_viento[1].split(',')

                    # Agregar los valores a las listas correspondientes
                    temperaturas.append(temperatura)
                    humedades.append(humedad)
                    presiones.append(presion)
                    velocidades_viento.append(float(velocidad_viento))
                    direcciones_viento.append(self._direccion_viento_a_grados(direccion_viento))

        # Calcular promedios
        promedio_temperatura = sum(temperaturas) / len(temperaturas)
        promedio_humedad = sum(humedades) / len(humedades)
        promedio_presion = sum(presiones) / len(presiones)
        promedio_velocidad_viento = sum(velocidades_viento) / len(velocidades_viento)

        # Calcular la dirección predominante del viento como el promedio de los grados
        promedio_grados_viento = sum(direcciones_viento) / len(direcciones_viento)
        direccion_predominante_viento = self._grados_a_direccion(promedio_grados_viento)

        return (promedio_temperatura, promedio_humedad, promedio_presion, promedio_velocidad_viento, direccion_predominante_viento)

datos = DatosMeteorologicos("datos.txt")
estadisticas = datos.procesar_datos()
print(f"Temperatura Promedio: {estadisticas[0]:.2f}°C")
print(f"Humedad Promedio: {estadisticas[1]:.2f}%")
print(f"Presión Promedio: {estadisticas[2]:.2f}")
print(f"Velocidad Promedio del Viento: {estadisticas[3]:.2f} m/s")
print(f"Dirección Predominante del Viento: {estadisticas[4]}")
