import pyautogui
import time
import os

def cargar_archivo_kml(ruta_kml: str):
    """
    Activa la ventana de Google Earth Pro, abre el cuadro de diálogo para cargar archivos,
    escribe la ruta del archivo KML y lo carga.

    :param ruta_kml: Ruta completa del archivo KML a cargar.
    """
    print("Buscando la ventana de Google Earth Pro...")
    ventanas = pyautogui.getWindowsWithTitle("Google Earth Pro")
    if not ventanas:
        print("No se encontró la ventana de Google Earth Pro. Asegúrate de que esté abierta.")
        return
    
    ventana = ventanas[0]
    ventana.activate()  # Llevar la ventana al frente
    time.sleep(5)  # Esperar para asegurarse de que esté activa

    print("Abriendo cuadro de diálogo para cargar archivos...")
    pyautogui.hotkey("ctrl", "o")
    time.sleep(10)  # Tiempo para que el cuadro de diálogo se abra completamente

    print(f"Cargando archivo KML desde: {ruta_kml}")
    pyautogui.typewrite(ruta_kml)
    time.sleep(5)
    pyautogui.press("enter")  # Confirmar la carga
    print(f"Archivo {ruta_kml} cargado en Google Earth Pro.")
    time.sleep(10)  # Esperar a que se procese el archivo


def click_centro_vista_cenital():
    """
    Hace clic en el centro de la pantalla y ajusta la vista cenital en Google Earth Pro.
    """
    pantalla_ancho, pantalla_alto = pyautogui.size()
    centro_x, centro_y = pantalla_ancho // 2, pantalla_alto // 2

    print(f"Haciendo clic en el centro de la pantalla: ({centro_x}, {centro_y})")
    pyautogui.click(x=centro_x, y=centro_y)
    time.sleep(2)

    print("Ajustando vista cenital...")
    for _ in range(2):
        pyautogui.press('u')  # Elevar la vista
        time.sleep(2)
    for _ in range(2):
        pyautogui.press('n')  # Centrar la vista
        time.sleep(1)


def mantener_tecla_oprimida(tecla: str, duracion: float = 1, intentos: int = 16):
    """
    Mantiene una tecla específica presionada varias veces.

    :param tecla: Tecla que se desea mantener presionada (por ejemplo, '=' o 'o').
    :param duracion: Tiempo en segundos entre cada acción.
    :param intentos: Número de veces que se presionará la tecla.
    """
    print(f"Simulando mantener la tecla '{tecla}' presionada {intentos} veces...")
    for i in range(intentos):
        pyautogui.keyDown(tecla)
        time.sleep(duracion)
        pyautogui.keyUp(tecla)
        print(f"Presión {i + 1} de {intentos} completada.")
        time.sleep(0.5)  # Intervalo entre repeticiones


# def presionar_control_alt_s():
#     """
#     Simula presionar la combinación de teclas Control + Alt + S.
#     """
#     print("Presionando Control + Alt + S...")
#     pyautogui.hotkey('ctrl', 'alt', 's')
#     time.sleep(2)
#     print("Control + Alt + S presionado.")


def guardado_aux():
      """
      Guarda datos en Google Earth Pro a través del menú de archivo.
      """
      print("Guardando datos mediante el menú de archivo...")
      pyautogui.hotkey('alt', 'f')
      time.sleep(1)
      pyautogui.press('down')
      pyautogui.press("enter")
      time.sleep(2)
      for _ in range(3):
          pyautogui.press('down')
          time.sleep(1)
      pyautogui.press("enter")
      print("Datos guardados.")


def hacer_clic_en_coordenadas(x: int, y: int):
    """
    Hace clic en una posición específica de la pantalla.

    :param x: Coordenada X del botón.
    :param y: Coordenada Y del botón.
    """
    print(f"Haciendo clic en las coordenadas ({x}, {y})...")
    pyautogui.click(x=x, y=y)
    print("Clic realizado.")


def procesar_kml_y_foto(ruta_base: str,
                        nombre_foto:str="2022_5.jpg"):
    """
    Función para procesar un archivo KML en Google Earth Pro y realizar las acciones necesarias.

    :param ruta_base: Ruta base donde se encuentran el archivo KML y la foto.
    """
    # Generar las rutas necesarias
    ruta_kml = os.path.join(ruta_base, "poligono.kml")
    ruta_foto = os.path.join(ruta_base, nombre_foto)
    
    # Validar que los archivos existen
    if not os.path.exists(ruta_kml):
        print(f"El archivo KML no existe en la ruta: {ruta_kml}")
        return
    if not os.path.exists(ruta_foto):
        print(f"El archivo de la foto no existe en la ruta: {ruta_foto}")
        return

    # Cargar un archivo KML
    print("Cargando archivo KML...")
    cargar_archivo_kml(ruta_kml)

    # Ajustar la vista cenital
    print("Ajustando vista cenital inicial...")
    click_centro_vista_cenital()

    # Mantener presionada la tecla '=' para acercar la vista
    print("Aumentando zoom con tecla '='...")
    mantener_tecla_oprimida('=', duracion=1, intentos=16)

    # Ajustar la vista nuevamente
    print("Ajustando vista cenital nuevamente...")
    click_centro_vista_cenital()
    time.sleep(10)

    # Presionar Control + Alt + S y guardar datos
    print("Guardando datos con combinación de teclas...")
    guardado_aux()
    time.sleep(10)

    # Hacer clic en un botón específico para procesar
    print("Haciendo clic en botón específico...")
    hacer_clic_en_coordenadas(x=1301, y=112)

    # Escribir la ruta de la foto y confirmarla
    print("Escribiendo ruta de la foto y cargándola...")
    time.sleep(5)
    pyautogui.typewrite(ruta_foto)
    time.sleep(5)
    pyautogui.press("enter")
    time.sleep(30)

    # Hacer clic en otro botón específico
    print("Haciendo clic en segundo botón específico...")
    hacer_clic_en_coordenadas(x=1401, y=111)
    time.sleep(5)

    # Simular presionar la tecla Delete o Suprimir
    print("Eliminando con tecla Suprimir...")
    pyautogui.press('delete')
    time.sleep(5)
    pyautogui.press("enter")  # Confirmar
    print("Proceso completado.")

# Ejemplo de uso
ruta_base = r'D:\Tesis_JE_fotos\SOACHA\SANTA_VIVIANA\subpoligono_4854'
procesar_kml_y_foto(ruta_base)
