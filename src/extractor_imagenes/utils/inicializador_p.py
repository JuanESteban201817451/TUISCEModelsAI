import subprocess
import time
import pyautogui
import os

# Importamos las funciones y constantes que ya tienes en tu proyecto.
from utils.helpers import guardado_aux, hacer_clic_en_coordenadas
from statics.cordenadas import (
    x_borrar_cache, y_borrar_cache,  # Si los necesitas, puedes usarlos.
    x_load_map_config, y_load_map_config,
    x_load_map_config_load, y_load_map_config_load,
    x_load_map_config_confirm, y_load_map_config_confirm,
    x_time, y_time,
    x_time_back, y_time_back,
    x_cierre_navegacion_foto, y_cierre_navegacion_foto
)
from statics.directorios_rutas import (
    ruta_google_earth, ruta_config_mapa, ruta_repair_tool
)


def abrir_google_earth(ruta_ejecutable: str) -> subprocess.Popen:
    """
    Abre la aplicación de Google Earth Pro y espera un tiempo fijo para
    que termine de iniciar.

    :param ruta_ejecutable: Ruta absoluta o relativa del ejecutable de Google Earth Pro.
    :type ruta_ejecutable: str
    :return: Objeto de tipo Popen que representa el proceso iniciado.
    :rtype: subprocess.Popen

    Ejemplo de uso:
        >>> proceso = abrir_google_earth(r"C:\\Program Files\\Google\\Google Earth Pro\\client\\googleearth.exe")
        >>> # Después puedes interactuar con 'proceso' si lo necesitas.
    """
    proceso = subprocess.Popen(ruta_ejecutable, shell=True)
    print("Google Earth Pro se ha iniciado...")
    time.sleep(30)  # Espera 30 segundos para que la aplicación termine de cargar
    return proceso


def guardar_y_cargar_configuracion(
    ruta_mapa: str,
    x_load_config: int,
    y_load_config: int,
    x_load_config_load: int,
    y_load_config_load: int,
    x_load_config_confirm: int,
    y_load_config_confirm: int,
    x_cierre_foto: int,
    y_cierre_foto: int
) -> None:
    """
    Guarda la configuración actual (por ejemplo, la imagen o los ajustes) y luego
    carga un archivo de configuración de mapa usando PyAutoGUI para automatizar los clics.

    :param ruta_mapa: Ruta del archivo que contiene la configuración del mapa.
    :type ruta_mapa: str
    :param x_load_config: Coordenada X del botón para abrir más opciones de configuración.
    :type x_load_config: int
    :param y_load_config: Coordenada Y del botón para abrir más opciones de configuración.
    :type y_load_config: int
    :param x_load_config_load: Coordenada X del botón "Load" (o equivalente).
    :type x_load_config_load: int
    :param y_load_config_load: Coordenada Y del botón "Load" (o equivalente).
    :type y_load_config_load: int
    :param x_load_config_confirm: Coordenada X del botón para confirmar la carga del mapa.
    :type x_load_config_confirm: int
    :param y_load_config_confirm: Coordenada Y del botón para confirmar la carga del mapa.
    :type y_load_config_confirm: int
    :param x_cierre_foto: Coordenada X del botón para cerrar la navegación de foto (ventana adicional).
    :type x_cierre_foto: int
    :param y_cierre_foto: Coordenada Y del botón para cerrar la navegación de foto (ventana adicional).
    :type y_cierre_foto: int

    :return: Esta función no devuelve nada.
    :rtype: None

    Ejemplo de uso:
        >>> guardar_y_cargar_configuracion(
        ...     ruta_mapa="C:\\ruta\\del\\map_config.kmz",
        ...     x_load_config=100, y_load_config=200,
        ...     x_load_config_load=150, y_load_config_load=250,
        ...     x_load_config_confirm=200, y_load_config_confirm=300,
        ...     x_cierre_foto=400, y_cierre_foto=500
        ... )
    """
    # Guardar configuración (presionando las teclas necesarias)
    print("Guardando datos con combinación de teclas...")
    guardado_aux()
    time.sleep(10)

    print("Abriendo opciones de configuración...")
    hacer_clic_en_coordenadas(x_load_config, y_load_config)
    time.sleep(3)

    print("Seleccionando botón 'Load' de la configuración...")
    hacer_clic_en_coordenadas(x_load_config_load, y_load_config_load)
    time.sleep(5)

    print("Escribiendo ruta del archivo de configuración y cargándolo...")
    pyautogui.typewrite(ruta_mapa)
    time.sleep(8)
    pyautogui.press("enter")
    time.sleep(5)

    print("Confirmando carga del mapa...")
    hacer_clic_en_coordenadas(x_load_config_confirm, y_load_config_confirm)
    time.sleep(5)

    print("Cerrando la ventana de navegación de foto...")
    hacer_clic_en_coordenadas(x_cierre_foto, y_cierre_foto)
    time.sleep(10)


def retroceder_tiempo(
    rango_fotos: int,
    x_time_coord: int,
    y_time_coord: int,
    x_time_back_coord: int,
    y_time_back_coord: int
) -> None:
    """
    Realiza clics para retroceder en el tiempo (historial de imágenes) 
    en Google Earth Pro, tantas veces como se indique en 'rango_fotos'.

    :param rango_fotos: Número de veces que se realizará el clic de retroceso de tiempo.
    :type rango_fotos: int
    :param x_time_coord: Coordenada X del botón/slider de tiempo.
    :type x_time_coord: int
    :param y_time_coord: Coordenada Y del botón/slider de tiempo.
    :type y_time_coord: int
    :param x_time_back_coord: Coordenada X del botón para retroceder una imagen en el tiempo.
    :type x_time_back_coord: int
    :param y_time_back_coord: Coordenada Y del botón para retroceder una imagen en el tiempo.
    :type y_time_back_coord: int

    :return: Esta función no devuelve nada.
    :rtype: None

    Ejemplo de uso:
        >>> retroceder_tiempo(
        ...     rango_fotos=5,
        ...     x_time_coord=300, y_time_coord=400,
        ...     x_time_back_coord=310, y_time_back_coord=410
        ... )
    """
    # Primero, hacemos clic en la barra de tiempo para activarla (opcional).
    print("Haciendo clic para activar el control de tiempo...")
    hacer_clic_en_coordenadas(x_time_coord, y_time_coord)
    time.sleep(5)

    for i in range(rango_fotos):
        print(f"Retroceso de tiempo número {i+1}...")
        hacer_clic_en_coordenadas(x_time_back_coord, y_time_back_coord)
        time.sleep(5)


def inicializador_and_config(foto_range: int) -> None:
    """
    Función principal que orquesta la apertura de Google Earth,
    la carga de configuración de mapas y el retroceso de tiempo 
    en el historial de imágenes, según 'foto_range'.

    :param foto_range: Número de veces que se retrocederá en el tiempo.
    :type foto_range: int

    :return: Esta función no devuelve nada.
    :rtype: None

    Ejemplo de uso:
        >>> inicializador_and_config(foto_range=5)
    """
    # 1. Abrir Google Earth
    abrir_google_earth(ruta_google_earth)

    # 2. Guardar config y cargar archivo de configuración
    guardar_y_cargar_configuracion(
        ruta_mapa=ruta_config_mapa,
        x_load_config=x_load_map_config,
        y_load_config=y_load_map_config,
        x_load_config_load=x_load_map_config_load,
        y_load_config_load=y_load_map_config_load,
        x_load_config_confirm=x_load_map_config_confirm,
        y_load_config_confirm=y_load_map_config_confirm,
        x_cierre_foto=x_cierre_navegacion_foto,
        y_cierre_foto=y_cierre_navegacion_foto
    )

    # 3. Retroceder tiempo en el historial de imágenes
    retroceder_tiempo(
        rango_fotos=foto_range,
        x_time_coord=x_time,
        y_time_coord=y_time,
        x_time_back_coord=x_time_back,
        y_time_back_coord=y_time_back
    )

if __name__ == "__main__":
    inicializador_and_config(foto_range=16)
