# Externas
import os 
import argparse
import time
import json
# Propias
from src.utils.procesador import procesar_kml_y_foto
from src.utils.init_closer import inicializador_and_config, limpiar_y_cerrar_earth, tomar_captura, obtener_fecha_hora_para_nombre
from src.statics.diccionario_time import diccionario_tiempo

# Main
def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Procesar archivos KML y fotos desde una ruta específica.")
    parser.add_argument(
        "--ruta_base",
        required=True,
        help="Ruta base donde están las subcarpetas a procesar."
    )
    parser.add_argument(
        "--nombre_foto",
        default="2022_5",
        help="Nombre del archivo de la foto (por defecto:2022_5)."
    )
    parser.add_argument(
        "--tipo_guardado",
        default=1,
        type=int,
        help="Tipo de Guardado recistido por el Dispostivo."
    )


    args = parser.parse_args()
    ruta_base = args.ruta_base
    nombre_foto = args.nombre_foto
    tipo_guardado=args.tipo_guardado

    # Contador para saber cuántas veces procesamos una imagen
    contador_procesadas = 0

    # Validar que la ruta existe
    if not os.path.exists(ruta_base):
        print(f"La carpeta {ruta_base} no existe. Verifica la ruta.")
        return

    for carpeta_localidad in os.listdir(ruta_base):
        ruta_localidad = os.path.join(ruta_base, carpeta_localidad)
        for subcarpeta in os.listdir(ruta_localidad):
            ruta_subcarpeta = os.path.join(ruta_localidad, subcarpeta)
            if os.path.isdir(ruta_subcarpeta):
                print(f"Procesando carpeta: {ruta_subcarpeta}")
                ruta_jpg=ruta_subcarpeta + fr'\{nombre_foto}.jpg'
                if os.path.exists(ruta_jpg):
                    continue
                try:
                    try:
                        foto_range=diccionario_tiempo.get(nombre_foto)
                    except:
                        raise(f'El periodo {nombre_foto} no esta disponible seleccione uno de aca {diccionario_tiempo.keys}')
                    
                    # Aumentamos el contador antes de hacer nada
                    contador_procesadas += 1
                    # Verificamos si es la iteración 1 o múltiplo de 40
                    # Incia el proceso
                    if contador_procesadas == 1 or (contador_procesadas % 40 == 0):
                        time.sleep(5)  # Espera 5 segundos
                        inicializador_and_config(foto_range=foto_range, tipo_guardado=tipo_guardado)
                        time.sleep(10)  # Espera 5 segundos
                        inicio = time.time()
                        hora=obtener_fecha_hora_para_nombre()
                        tomar_captura(ruta_destino=fr'.\data\interim\comprobador\comprobador_{nombre_foto}_{hora}.png')
                        with open(fr'.\data\interim\comprobador\comprobador_{nombre_foto}_{hora}.txt', "w", encoding="utf-8") as archivo:
                            # Escribimos la variable en el archivo.
                            archivo.write(str(ruta_subcarpeta))

                    ## Procesa los poligonos
                    procesar_kml_y_foto(ruta_subcarpeta, nombre_foto, tipo_guardado=tipo_guardado)

                    # cierra uno antes de los multiplos de 40.
                    if ((contador_procesadas+1) % 40) == 0:
                        time.sleep(5)  # Espera 5 segundos
                        limpiar_y_cerrar_earth()
                        time.sleep(10)  # Espera 5 segundos
                        fin = time.time()
                        total=fin-inicio
                        dicci_time={'inicio':inicio,
                                     'fin':fin,
                                     'total':total}
                        # Guardar el diccionario en un archivo JSON
                        with open(rf"./data/interim/time/datos_time{contador_procesadas}.json", "w", encoding="utf-8") as archivo:
                            json.dump(dicci_time, archivo, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Error procesando {ruta_subcarpeta}: {e}")
            else:
                print(f"{ruta_subcarpeta} no es una carpeta. Ignorando...")        

if __name__ == "__main__":
    main()
