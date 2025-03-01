# bibliotecas
# Externas
import json

# Cargar el JSON con las coordenadas
with open("./config_coordenadas.json", "r", encoding="utf-8") as f:
    coordenadas = json.load(f)

# Asignar cada coordenada a variables individuales
x_borrar_cache, y_borrar_cache = coordenadas["borrar_cache"]["x"], coordenadas["borrar_cache"]["y"]
x_load_map_config, y_load_map_config = coordenadas["load_map_config"]["x"], coordenadas["load_map_config"]["y"]
x_load_map_config_load, y_load_map_config_load = coordenadas["load_map_config_load"]["x"], coordenadas["load_map_config_load"]["y"]
x_load_map_config_confirm, y_load_map_config_confirm = coordenadas["load_map_config_confirm"]["x"], coordenadas["load_map_config_confirm"]["y"]
x_time, y_time = coordenadas["time"]["x"], coordenadas["time"]["y"]
x_time_back, y_time_back = coordenadas["time_back"]["x"], coordenadas["time_back"]["y"]
x_cierre_navegacion_foto, y_cierre_navegacion_foto = coordenadas["cierre_navegacion_foto"]["x"], coordenadas["cierre_navegacion_foto"]["y"]
x_guardado_imagen, y_guardado_imagen = coordenadas["guardado_imagen"]["x"], coordenadas["guardado_imagen"]["y"]

x_boton_file,y_boton_file=coordenadas["boton_file"]["x"], coordenadas["boton_file"]["y"]
x_boton_save,y_boton_save=coordenadas["boton_save"]["x"], coordenadas["boton_save"]["y"]
x_boton_save_imag,y_boton_save_imag=coordenadas["boton_save_imag"]["x"], coordenadas["boton_save_imag"]["y"]

