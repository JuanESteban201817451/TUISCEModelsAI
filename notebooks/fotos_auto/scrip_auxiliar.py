import pyautogui
import json

print("Mueve el mouse al botón y presiona Enter para guardar las coordenadas...")
input("Presiona Enter cuando el mouse esté sobre el botón.")
x, y = pyautogui.position()

# Guardar las coordenadas en un archivo JSON
with open("coordenadas.json", "w") as file:
    json.dump({"x": x, "y": y}, file)

print(f"Coordenadas guardadas: X={x}, Y={y}")