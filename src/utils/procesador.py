# bibliotecas
# Externas
import os
import pyautogui
import time
# Propias
from src.utils.helpers import cargar_archivo_kml, click_centro_vista_cenital, mantener_tecla_oprimida, hacer_clic_en_coordenadas,guardado_aux
from src.utils.cordenadas import x_cierre_navegacion_foto,y_cierre_navegacion_foto, x_guardado_imagen,y_guardado_imagen

def procesar_kml_y_foto(ruta_base: str, nombre_foto: str = "2022_5"):
    """
    Procesa un archivo KML en Google Earth Pro, ajusta la vista y guarda una imagen.

    Parámetros:
        ruta_base (str): Ruta base donde se encuentran el archivo KML y la foto.
        nombre_foto (str, opcional): Nombre del archivo de la foto a cargar. 
                                     Por defecto, "2022_5".

    Proceso:
        - Genera las rutas del archivo KML y la foto.
        - Valida la existencia del archivo KML.
        - Carga el archivo KML en Google Earth Pro.
        - Ajusta la vista cenital inicial.
        - Aumenta el zoom manteniendo presionada la tecla '='.
        - Ajusta la vista cenital nuevamente.
        - Guarda los datos mediante combinación de teclas.
        - Hace clic en el botón de guardado de imagen.
        - Escribe la ruta de la foto y la carga en Google Earth.
        - Hace clic en el botón de cierre de navegación tras la carga de la imagen.
        - Elimina la imagen con la tecla "Suprimir".
    
    Retorna:
        None

    Ejemplo de uso:
        procesar_kml_y_foto("D:/Tesis_JE_fotos/Localidad1/Estacion1/Subpoligono1", "2022_5")
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
    hacer_clic_en_coordenadas(x=x_guardado_imagen, y=y_guardado_imagen)
    time.sleep(24)

    print("Escribiendo ruta de la foto y cargándola...")
    pyautogui.typewrite(ruta_foto)
    time.sleep(8)
    pyautogui.press("enter")
    time.sleep(24)

    print("Haciendo clic en segundo botón específico...")
    hacer_clic_en_coordenadas(x=x_cierre_navegacion_foto, y=y_cierre_navegacion_foto)
    time.sleep(10)

    print("Eliminando con tecla Suprimir...")
    pyautogui.press('delete')
    time.sleep(6)
    pyautogui.press("enter")
    print("Proceso completado.")
    time.sleep(5)