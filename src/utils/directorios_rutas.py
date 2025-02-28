# bibliotecas
# Externas
import json

# Cargar el JSON con las rutas
with open("./config_rutas.json", "r", encoding="utf-8") as f:
    rutas = json.load(f)

# Asignar cada ruta a su variable correspondiente
ruta_google_earth = rutas["google_earth"]
ruta_repair_tool = rutas["repair_tool"]
ruta_config_mapa = rutas["config_mapa"]