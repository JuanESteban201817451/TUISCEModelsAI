# bibliotecas
# Externas
import pyautogui
import time

print("Tienes 5 segundos para mover el cursor sobre el botón de 'Borrar Caché'.")
time.sleep(5)
x, y = pyautogui.position()
print(f"Coordenadas del botón: ({x}, {y})")
