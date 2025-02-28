# Bibliotecas
import subprocess
import time
import pyautogui
import os
# Importamos las funciones y constantes.
from utils.helpers import guardado_aux, hacer_clic_en_coordenadas
from statics.cordenadas import (
    x_borrar_cache, y_borrar_cache,
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
        time.sleep(4)


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



### limpiadro cache
def limpiar_y_cerrar_earth(
    ruta_repair_tool: str=ruta_repair_tool,
    x_borrar_cache: int=x_borrar_cache,
    y_borrar_cache: int=y_borrar_cache
) -> None:
    """
    Cierra la aplicación Google Earth Pro de forma suave, abre la herramienta
    de reparación (Repair Tool) para limpiar la caché y la cierra finalmente.

    :param ruta_repair_tool: Ruta absoluta o relativa del ejecutable de la herramienta de reparación.
    :type ruta_repair_tool: str
    :param x_borrar_cache: Coordenada X del botón "Borrar Caché" en el Repair Tool.
    :type x_borrar_cache: int
    :param y_borrar_cache: Coordenada Y del botón "Borrar Caché" en el Repair Tool.
    :type y_borrar_cache: int

    :return: Esta función no devuelve ningún valor.
    :rtype: None

    Ejemplo de uso:
        >>> limpiar_y_cerrar_earth(
        ...     ruta_repair_tool="C:\\Program Files\\Google\\Google Earth Pro\\client\\repair_tool.exe",
        ...     x_borrar_cache=500,
        ...     y_borrar_cache=300
        ... )
    """
    # Paso 1: Cerrar Google Earth Pro de forma suave (ALT + F4)
    pyautogui.hotkey("alt", "f4")
    time.sleep(5)  # Esperamos para asegurar que se cerró
    print("Google Earth Pro se ha cerrado.")

    # Paso 2: Abrir el Repair Tool
    print("Abriendo Google Earth Repair Tool...")
    repair_proceso = subprocess.Popen(ruta_repair_tool, shell=True)
    time.sleep(10)  # Esperar a que cargue

    # Paso 3: Hacer clic en el botón "Borrar Caché"
    print("Borrando caché de Google Earth Pro...")
    hacer_clic_en_coordenadas(x_borrar_cache, y_borrar_cache)
    time.sleep(2)

    # Paso 4: Cerrar el Repair Tool (ALT + F4)
    pyautogui.hotkey("alt", "f4")
    print("Google Earth Repair Tool se ha cerrado.")


def tomar_captura(ruta_destino):
    # Esperar unos segundos antes de tomar la captura (por ejemplo 3s).
    time.sleep(3)
    
    # Toma la captura de pantalla.
    captura = pyautogui.screenshot()
    
    # Guarda la captura en la ruta especificada.
    captura.save(ruta_destino)
    print(f"Captura de pantalla guardada en: {ruta_destino}")


from datetime import datetime

def obtener_fecha_hora_para_nombre():
    # Obtenemos la fecha y hora actual
    fecha_hora_actual = datetime.now()
    
    # Formateamos la fecha y hora para que cada campo esté separado por '_'
    # Resultado del estilo: "2025_02_23_17_05_30"
    nombre_formateado = fecha_hora_actual.strftime("%Y_%m_%d_%H")
    
    return nombre_formateado
