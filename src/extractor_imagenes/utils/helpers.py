import pyautogui
import time

def cargar_archivo_kml(ruta_kml: str):
    print("Buscando la ventana de Google Earth Pro...")
    ventanas = pyautogui.getWindowsWithTitle("Google Earth Pro")
    if not ventanas:
        print("No se encontró la ventana de Google Earth Pro.")
        return

    ventana = ventanas[0]
    ventana.activate()
    time.sleep(5)

    print("Abriendo cuadro de diálogo para cargar archivos...")
    pyautogui.hotkey("ctrl", "o")
    time.sleep(10)

    print(f"Cargando archivo KML desde: {ruta_kml}")
    pyautogui.typewrite(ruta_kml)
    time.sleep(5)
    pyautogui.press("enter")
    time.sleep(15)

def click_centro_vista_cenital():
    pantalla_ancho, pantalla_alto = pyautogui.size()
    centro_x, centro_y = pantalla_ancho // 2, pantalla_alto // 2

    print(f"Haciendo clic en el centro de la pantalla: ({centro_x}, {centro_y})")
    pyautogui.click(x=centro_x, y=centro_y)
    time.sleep(2)

    print("Ajustando vista cenital...")
    for _ in range(2):
        pyautogui.press('u')
        time.sleep(2)
    for _ in range(2):
        pyautogui.press('n')
        time.sleep(1)

def mantener_tecla_oprimida(tecla: str, duracion: float = 1, intentos: int = 16):
    print(f"Simulando mantener la tecla '{tecla}' presionada {intentos} veces...")
    for i in range(intentos):
        pyautogui.keyDown(tecla)
        time.sleep(duracion)
        pyautogui.keyUp(tecla)
        print(f"Presión {i + 1} de {intentos} completada.")
        time.sleep(0.5)

def hacer_clic_en_coordenadas(x: int, y: int):
    print(f"Haciendo clic en las coordenadas ({x}, {y})...")
    pyautogui.click(x=x, y=y)
    print("Clic realizado.")


def guardado_aux():
      """
      Guarda datos en Google Earth Pro a través del menú de archivo.
      """
      print("Guardando datos mediante el menú de archivo...")
      pyautogui.hotkey('alt', 'f')
      time.sleep(1)
      pyautogui.press('down')
      time.sleep(1)
      pyautogui.press("enter")
      time.sleep(2)
      for _ in range(3):
          pyautogui.press('down')
          time.sleep(1)
      pyautogui.press("enter")
      print("Datos guardados.")