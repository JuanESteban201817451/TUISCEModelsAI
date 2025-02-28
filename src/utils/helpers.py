# bibliotecas
# Externas
import pyautogui  # Biblioteca para automatización de la GUI
import time  # Biblioteca para manejar tiempos de espera

def cargar_archivo_kml(ruta_kml: str):
    """
    Carga un archivo KML en Google Earth Pro.

    Parámetros:
        ruta_kml (str): Ruta completa del archivo KML a cargar.

    Retorna:
        None
    """
    print("Buscando la ventana de Google Earth Pro...")
    ventanas = pyautogui.getWindowsWithTitle("Google Earth Pro")
    if not ventanas:
        print("No se encontró la ventana de Google Earth Pro.")
        return

    ventana = ventanas[0]
    ventana.activate()  # Activa la ventana de Google Earth Pro
    time.sleep(5)  # Espera para asegurar la activación de la ventana

    print("Abriendo cuadro de diálogo para cargar archivos...")
    pyautogui.hotkey("ctrl", "o")  # Combinación de teclas para abrir archivo
    time.sleep(10)  # Espera para que aparezca el cuadro de diálogo

    print(f"Cargando archivo KML desde: {ruta_kml}")
    pyautogui.typewrite(ruta_kml)  # Escribe la ruta del archivo en el cuadro de diálogo
    time.sleep(5)
    pyautogui.press("enter")  # Presiona "Enter" para confirmar la carga
    time.sleep(15)  # Espera a que el archivo se cargue completamente

def click_centro_vista_cenital():
    """
    Realiza un clic en el centro de la pantalla y ajusta la vista cenital en Google Earth Pro.

    Retorna:
        None
    """
    pantalla_ancho, pantalla_alto = pyautogui.size()  # Obtiene las dimensiones de la pantalla
    centro_x, centro_y = pantalla_ancho // 2, pantalla_alto // 2  # Calcula el centro de la pantalla

    print(f"Haciendo clic en el centro de la pantalla: ({centro_x}, {centro_y})")
    pyautogui.click(x=centro_x, y=centro_y)  # Hace clic en el centro de la pantalla
    time.sleep(2)

    print("Ajustando vista cenital...")
    for _ in range(2):
        pyautogui.press('u')  # Restablece la inclinación de la cámara
        time.sleep(2)
    for _ in range(2):
        pyautogui.press('n')  # Orienta la vista hacia el norte
        time.sleep(1)

def mantener_tecla_oprimida(tecla: str, duracion: float = 1, intentos: int = 16):
    """
    Simula la pulsación repetida de una tecla durante un tiempo determinado.

    Parámetros:
        tecla (str): La tecla a presionar.
        duracion (float): Duración en segundos de cada pulsación. (Por defecto 1 seg)
        intentos (int): Número de veces que se presiona la tecla. (Por defecto 16)

    Retorna:
        None
    """
    print(f"Simulando mantener la tecla '{tecla}' presionada {intentos} veces...")
    for i in range(intentos):
        pyautogui.keyDown(tecla)  # Mantiene presionada la tecla
        time.sleep(duracion)  # Espera el tiempo indicado
        pyautogui.keyUp(tecla)  # Suelta la tecla
        print(f"Presión {i + 1} de {intentos} completada.")
        time.sleep(0.5)  # Pausa entre intentos

def hacer_clic_en_coordenadas(x: int, y: int):
    """
    Hace clic en una posición específica de la pantalla.

    Parámetros:
        x (int): Coordenada X del clic.
        y (int): Coordenada Y del clic.

    Retorna:
        None
    """
    print(f"Haciendo clic en las coordenadas ({x}, {y})...")
    pyautogui.click(x=x, y=y)  # Ejecuta el clic en las coordenadas indicadas
    print("Clic realizado.")

def guardado_aux():
    """
    Guarda datos en Google Earth Pro a través del menú de archivo.

    Retorna:
        None
    """
    print("Guardando datos mediante el menú de archivo...")
    pyautogui.hotkey('alt', 'f')  # Abre el menú "Archivo"
    time.sleep(1)
    pyautogui.press('down')  # Baja una opción en el menú
    time.sleep(1)
    pyautogui.press("enter")  # Selecciona la opción actual
    time.sleep(2)
    for _ in range(3):
        pyautogui.press('down')  # Navega hacia la opción de guardado
        time.sleep(1)
    pyautogui.press("enter")  # Confirma el guardado
    print("Datos guardados.")

def guardado_aux_2():
    """
    Guarda datos en Google Earth Pro a través del menú de archivo.

    Retorna:
        None
    """
    print("Guardando datos mediante el menú de archivo...")
    pyautogui.hotkey('alt', 'f', 's')  # Abre el menú "Archivo"
    time.sleep(1)
