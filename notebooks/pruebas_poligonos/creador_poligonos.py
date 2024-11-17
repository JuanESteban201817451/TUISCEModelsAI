from shapely.geometry import Polygon
import unicodedata
import requests
from shapely.ops import transform
import pyproj
from tqdm import tqdm
import numpy as np
from shapely.geometry import box

# URL base para la API de poligonos de localidades en Bogotá
url_base = "https://bogota-laburbano.opendatasoft.com/api/records/1.0/search/?dataset=poligonos-localidades&refine.Nombre+de+la+localidad="

def procesador_nombre_localidad(nombre_localidad: str) -> str:
    """
    Procesa el nombre de una localidad eliminando tildes, espacios y convirtiendo a mayúsculas.
    Si el nombre contiene la letra 'Ñ', se retorna directamente sin procesar las tildes.

    Args:
        nombre_localidad (str): El nombre de la localidad que se desea procesar.

    Returns:
        str: Nombre de la localidad procesado, con tildes eliminadas, sin espacios iniciales y finales, 
        y con espacios entre palabras reemplazados por el símbolo '+'.
    """
    # Si el nombre contiene 'Ñ', se deja tal cual y se reemplazan espacios por '+'
    if 'Ñ' in nombre_localidad.upper():
        return nombre_localidad.strip().upper().replace(" ", "+")

    # Eliminar tildes y caracteres diacríticos
    nombre_localidad = ''.join(
        (c for c in unicodedata.normalize('NFD', nombre_localidad) if unicodedata.category(c) != 'Mn')
    )

    # Eliminar espacios iniciales y finales, convertir a mayúsculas y reemplazar espacios entre palabras por '+'
    return nombre_localidad.strip().upper().replace(" ", "+")

def reproyectar_poligono_a_metros(polygon: Polygon) -> Polygon:
    """
    Reproyecta un polígono desde EPSG:4326 (coordenadas geográficas) a EPSG:3116 (metros para Colombia).

    Args:
        polygon (Polygon): El polígono en coordenadas geográficas (EPSG:4326).

    Returns:
        Polygon: El polígono reproyectado en EPSG:3116 (metros).
    """
    # Definir las proyecciones de origen (EPSG:4326) y destino (EPSG:3116)
    project = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3116", always_xy=True).transform

    # Aplicar la transformación al polígono
    return transform(project, polygon)


def subdivide_polygon_with_names(polygon, localidad_name, cell_size=50):
    """
    Divide un polígono en sub-polígonos cuadrados de tamaño especificado (por defecto 50x50 metros) 
    y genera nombres únicos para cada bloque. Los sub-polígonos que no estén completamente dentro 
    del polígono original son descartados.

    Args:
        polygon (Polygon): El polígono original que se desea subdividir.
        localidad_name (str): El nombre de la localidad asociado al polígono. Se utiliza para 
                              generar los nombres de los bloques.
        cell_size (int, optional): El tamaño de cada sub-polígono en metros. Por defecto es 50x50 metros.

    Returns:
        list: Una lista de sub-polígonos que están completamente dentro del polígono original.
        list: Una lista de nombres únicos para cada sub-polígono, generados a partir del nombre 
              de la localidad y un contador.
    
    Example:
        >>> subdivide_polygon_with_names(polygon, "CiudadBolivar", cell_size=20)
        ([<Polygon>, <Polygon>, ...], ['CiudadBolivar_bloque_1_20_x_20', 'CiudadBolivar_bloque_2_20_x_20', ...])

    """
    # Obtener los límites del polígono original
    minx, miny, maxx, maxy = polygon.bounds
    # Generar una lista de coordenadas para los ejes X e Y, espaciadas según el tamaño de celda
    x_coords = np.arange(minx, maxx, cell_size)
    y_coords = np.arange(miny, maxy, cell_size)
    
    sub_polygons = []  # Lista para almacenar los sub-polígonos válidos
    block_names = []   # Lista para almacenar los nombres de cada bloque
    block_counter = 1  # Contador para generar nombres de bloques

    # Iterar sobre las coordenadas X
    for x in tqdm(x_coords, desc=f'Procesando {localidad_name} eje X'):
        # Iterar sobre las coordenadas Y
        for y in tqdm(y_coords, desc=f'Procesando {localidad_name} eje Y', leave=False):
            # Crear un sub-polígono de tamaño cell_size x cell_size
            sub_polygon = box(x, y, x + cell_size, y + cell_size)
            # Verificar si el sub-polígono está completamente dentro del polígono original
            if polygon.contains(sub_polygon):
                sub_polygons.append(sub_polygon)  # Agregar el sub-polígono a la lista
                # Generar el nombre del bloque
                block_name = f"{localidad_name}_bloque_{block_counter}_{cell_size}_x_{cell_size}"
                block_names.append(block_name)  # Agregar el nombre del bloque a la lista
                block_counter += 1  # Incrementar el contador de bloques
    
    # Retornar la lista de sub-polígonos válidos y sus nombres
    return sub_polygons, block_names



def extractor_poligonos_localidades(nombre_localidad: list, url_base=url_base) -> Polygon:
    """
    Extrae el polígono de una localidad específica en Bogotá, consultando una API pública y
    devolviendo las coordenadas del polígono en formato `Polygon` de Shapely.

    Args:
        nombre_localidad (str): El nombre de la localidad cuyo polígono se desea extraer.
        url_base (str): URL base de la API de la cual se extraen los datos. Por defecto, 
                        apunta a la API de poligonos de localidades de Bogotá.

    Returns:
        Polygon: Un objeto `Polygon` de Shapely que contiene las coordenadas del polígono de la localidad.
    """
    # Procesar el nombre de la localidad
    nombre_localidad = procesador_nombre_localidad(nombre_localidad)
    
    # Construir la URL final para la API usando el nombre de la localidad procesado
    url = url_base + nombre_localidad
    
    # Hacer la solicitud HTTP a la API y obtener la respuesta en formato JSON
    response = requests.get(url).json()
    p=Polygon(response['records'][0]['fields']['geometry']['coordinates'][0][0])
    p=reproyectar_poligono_a_metros(p)
    # Extraer las coordenadas del polígono de la respuesta JSON y crear un objeto Polygon de Shapely
    return p