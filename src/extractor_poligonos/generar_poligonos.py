import argparse
from utils.query_poligonos import extractor_poligonos_localidades, creador_poligono_municipio
from utils.utils_poligonos import crear_diccionario_subpoligonos, filtrar_poligonos_por_distancia, creardor_carpetas_y_kmls
from statics.list_dict import archivo_mun_gp, municipio_gp, lista_localidades_bogota_gp, url_base_gp, lista_localidades_estaciones_a_comparar_gp, distancia_maxima_gp, base_path_gp

def main(archivo_mun: str, 
         municipio: str, 
         localidades: list, 
         url_base: str, 
         estaciones_a_comparar: list,
         distancia_max: int,
         base_path: str):
    """
    Ejecuta el proceso de generación de polígonos y creación de estructuras de carpetas.
    
    Args:
        archivo_mun (str): Ruta al archivo SHP de municipios.
        municipio (str): Nombre del municipio.
        localidades (list): Lista de localidades de Bogotá a procesar.
        url_base (str): URL base de la API de polígonos.
        estaciones_a_comparar (list): Lista de localidades y estaciones a analizar.
        distancia_max (int): Distancia máxima a estaciones de TransMiCable.
        base_path (str): Ruta base donde se guardarán los archivos generados.
    """
    poligono_municipio = creador_poligono_municipio(path=archivo_mun, municipio=municipio)
    poligono_localidades = extractor_poligonos_localidades(localidades, url_base=url_base)
    poligonos_combinados = poligono_localidades | poligono_municipio
    subpoligonos_diccionario = crear_diccionario_subpoligonos(poligonos_combinados, tamano_m=200)

    conjunto_total = []
    for dict_interes in estaciones_a_comparar:
        subpoligonos_cercanos = filtrar_poligonos_por_distancia(
            localidad=dict_interes.get('Localidad'),
            subpoligonos=subpoligonos_diccionario,
            estaciones=dict_interes.get('Diccionario de estaciones'),
            distancia_maxima=distancia_max
        )
        conjunto_total.append(subpoligonos_cercanos)
    
    creardor_carpetas_y_kmls(conjunto_total=conjunto_total, base_path=base_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera polígonos y estructura de carpetas para descarga de imágenes.")
    parser.add_argument("--archivo_mun", type=str, default=archivo_mun_gp, help="Ruta al archivo SHP de municipios")
    parser.add_argument("--municipio", type=str, default=municipio_gp, help="Nombre del municipio a descargar")
    parser.add_argument("--localidades", type=str, nargs='+', default=lista_localidades_bogota_gp, help="Lista de localidades de interés en Bogotá")
    parser.add_argument("--url_base", type=str, default=url_base_gp, help="URL base de la API de polígonos de localidades")
    parser.add_argument("--estaciones_a_comparar", type=str, default=str(lista_localidades_estaciones_a_comparar_gp), help="Lista de localidades y estaciones a analizar")
    parser.add_argument("--distancia_max", type=int, default=distancia_maxima_gp, help="Distancia máxima a estaciones de TransMiCable")
    parser.add_argument("--base_path", type=str, default=base_path_gp, help="Ruta base donde se guardarán los archivos generados")
    
    args = parser.parse_args()
    main(args.archivo_mun, args.municipio, args.localidades, args.url_base, eval(args.estaciones_a_comparar), args.distancia_max, args.base_path)
