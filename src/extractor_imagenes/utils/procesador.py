import os
import pyautogui
import time
from utils.helpers import cargar_archivo_kml, click_centro_vista_cenital, mantener_tecla_oprimida, hacer_clic_en_coordenadas,guardado_aux


def procesar_kml_y_foto(ruta_base: str, nombre_foto: str = "2022_5"):
    """
    Función para procesar un archivo KML en Google Earth Pro y realizar las acciones necesarias.

    :param ruta_base: Ruta base donde se encuentran el archivo KML y la foto.
    :param nombre_foto: Nombre del archivo de la foto (por defecto "2022_5").
    """
    # Generar las rutas necesarias
    ruta_kml = os.path.join(ruta_base, "poligono.kml")
    ruta_foto = os.path.join(ruta_base, nombre_foto)

    # Validar que los archivos existen
    if not os.path.exists(ruta_kml):
        print(f"Archivo KML no encontrado: {ruta_kml}")
        return
    
    print("Cargando archivo KML...")
    cargar_archivo_kml(ruta_kml)

    print("Ajustando vista cenital inicial...")
    click_centro_vista_cenital()

    print("Aumentando zoom con tecla '='...")
    mantener_tecla_oprimida('=', duracion=1, intentos=16)

    print("Ajustando vista cenital nuevamente...")
    click_centro_vista_cenital()
    time.sleep(20)

    print("Guardando datos con combinación de teclas...")
    guardado_aux()
    time.sleep(21)

    print("Haciendo clic en botón específico...")
    hacer_clic_en_coordenadas(x=1301, y=112)
    time.sleep(24)

    print("Escribiendo ruta de la foto y cargándola...")
    pyautogui.typewrite(ruta_foto)
    time.sleep(8)
    pyautogui.press("enter")
    time.sleep(24)

    print("Haciendo clic en segundo botón específico...")
    hacer_clic_en_coordenadas(x=1401, y=111)
    time.sleep(10)

    print("Eliminando con tecla Suprimir...")
    pyautogui.press('delete')
    time.sleep(6)
    pyautogui.press("enter")
    print("Proceso completado.")
    time.sleep(5)
