# Bibliotecas externas
import json
import os

# Obtener la ruta base del proyecto (subir dos niveles desde /src/utils/)
ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Cargar el JSON con las rutas desde la raíz del proyecto
with open(os.path.join(ruta_proyecto, "config_rutas.json"), "r", encoding="utf-8") as f:
    rutas = json.load(f)

# Asignar cada ruta a su variable correspondiente
ruta_google_earth = rutas["google_earth"]
ruta_repair_tool = rutas["repair_tool"]
ruta_config_mapa = os.path.join(ruta_proyecto, "data", "raw", "Configuracion_base.geprint")

# Verificación
print("Ruta base del proyecto:", ruta_proyecto)
print("Ruta configuración mapa:", ruta_config_mapa)
