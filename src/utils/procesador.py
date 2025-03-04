# bibliotecas
# Externas
import os
import pyautogui
import pyperclip
import time
import math
# Propias
from src.utils.helpers import cargar_archivo_kml, click_centro_vista_cenital, mantener_tecla_oprimida, hacer_clic_en_coordenadas,guardado_aux, guardado_aux_2, guardado_aux_3
from src.utils.cordenadas import x_cierre_navegacion_foto,y_cierre_navegacion_foto, x_guardado_imagen,y_guardado_imagen, x_boton_file,y_boton_file, x_boton_save,y_boton_save,x_boton_save_imag,y_boton_save_imag

def procesar_kml_y_foto(ruta_base: str, nombre_foto: str = "2022_5",tipo_guardado=1, dilatador_tiempo=1, tipo_zoom=1):
    """
    Procesa un archivo KML en Google Earth Pro, ajusta la vista y guarda una imagen.

    Parámetros:
        ruta_base (str): Ruta base donde se encuentran el archivo KML y la foto.
        nombre_foto (str, opcional): Nombre del archivo de la foto a cargar. 
                                     Por defecto, "2022_5".
        tipo_guardado (int,optiona): tipo de Guardado
        Tipo zoom (int): Tipo de zoom

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
    cargar_archivo_kml(ruta_kml, dilatador_tiempo=dilatador_tiempo)

    print("Ajustando vista cenital inicial...")
    click_centro_vista_cenital(dilatador_tiempo=dilatador_tiempo)

    print("Aumentando zoom con tecla '='...")
    if tipo_zoom==1:
        mantener_tecla_oprimida('=', duracion=1, intentos=16,dilatador_tiempo=dilatador_tiempo )
    else:
        print("Haciendo clic en botón específico '+' ...")
        mantener_tecla_oprimida('+', duracion=1, intentos=16,dilatador_tiempo=dilatador_tiempo )

    print("Ajustando vista cenital nuevamente...")
    click_centro_vista_cenital(dilatador_tiempo=dilatador_tiempo)
    time.sleep(math.ceil(20*dilatador_tiempo))

    print("Guardando datos con combinación de teclas...")
    if tipo_guardado==1:
        guardado_aux()
        time.sleep(math.ceil(21*dilatador_tiempo))
    if tipo_guardado==2: 
        guardado_aux_2()
        time.sleep(math.ceil(21*dilatador_tiempo))
    if tipo_guardado==3:
        guardado_aux_3(x_boton_file=x_boton_file,
                       y_boton_file=y_boton_file,
                       x_boton_save=x_boton_save,
                       y_boton_save=y_boton_save,
                       x_boton_save_imag=x_boton_save_imag,
                       y_boton_save_imag=y_boton_save_imag,
                       dilatador_tiempo=dilatador_tiempo)

    print("Haciendo clic en botón específico...")
    hacer_clic_en_coordenadas(x=x_guardado_imagen, y=y_guardado_imagen)
    time.sleep(math.ceil(35*dilatador_tiempo))

    print("Escribiendo ruta de la foto y cargándola...")
    print(ruta_foto)


    # Copiar al portapapeles
    pyperclip.copy(ruta_foto)

    # Simular Ctrl + V para pegar
    pyautogui.hotkey("ctrl", "v")

    # Presionar Enter si es necesario
    #pyautogui.press("enter")
    #pyautogui.typewrite(ruta_foto,interval=0.2)




    time.sleep(math.ceil(15*dilatador_tiempo))
    pyautogui.press("enter")
    time.sleep(math.ceil(20*dilatador_tiempo))

    print("Haciendo clic en segundo botón específico...")
    hacer_clic_en_coordenadas(x=x_cierre_navegacion_foto, y=y_cierre_navegacion_foto)
    time.sleep(math.ceil(10*dilatador_tiempo))

    print("Eliminando con tecla Suprimir...")
    pyautogui.press('delete')
    time.sleep(math.ceil(8*dilatador_tiempo))
    pyautogui.press("enter")
    print("Proceso completado.")
    time.sleep(math.ceil(5*dilatador_tiempo))