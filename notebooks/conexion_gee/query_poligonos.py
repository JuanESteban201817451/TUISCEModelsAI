from typing import List, Dict
import requests
from shapely.geometry import Polygon, MultiPolygon
import unicodedata
import geopandas as gpd

# URL base para la API de poligonos de localidades en Bogotá
url_base = "https://bogota-laburbano.opendatasoft.com/api/records/1.0/search/?dataset=poligonos-localidades&refine.Nombre+de+la+localidad="


def extractor_poligonos_localidades(nombres_localidades: List[str],
                                    url_base: str = url_base) -> Dict[str, Dict]:
    """
    Extrae los polígonos de localidades específicas en Bogotá, consultando una API pública y
    devolviendo los polígonos en un formato compatible con Google Earth Engine (GEE) y GeoJSON.

    Args:
        nombres_localidades (List[str]): Lista de nombres de localidades cuyos polígonos se desean extraer.
        url_base (str): URL base de la API de la cual se extraen los datos. Por defecto, 
                        apunta a la API de polígonos de localidades de Bogotá.

    Returns:
        Dict[str, Dict]: Un diccionario donde las claves son los nombres de las localidades y los valores
                         son los polígonos o multipolígonos como objetos GeoJSON compatibles con GEE y Folium.
    """
    resultados: Dict[str, Dict] = {}
    for nombre_localidad in nombres_localidades:
        # Procesar el nombre de la localidad
        nombre_localidad_procesado = procesador_nombre_localidad(nombre_localidad)

        # Construir la URL final para la API usando el nombre de la localidad procesado
        url = url_base + nombre_localidad_procesado
        nombre_localidad_procesado=nombre_localidad_procesado.replace('+','_')
        try:
            # Hacer la solicitud HTTP a la API y obtener la respuesta en formato JSON
            response = requests.get(url)
            response.raise_for_status()  # Verificar si la solicitud fue exitosa

            data = response.json()

            # Verificar si hay resultados en la respuesta
            if 'records' not in data or not data['records']:
                print(f"No se encontró información para la localidad: {nombre_localidad}")
                continue

            # Extraer las coordenadas del polígono o multipolígono
            coordinates = data['records'][0]['fields']['geometry']['coordinates']
            geom_type = data['records'][0]['fields']['geometry']['type']

            if geom_type == "MultiPolygon":
                # Crear un MultiPolygon en Shapely
                multipolygon = MultiPolygon(
                    [Polygon(shell[0], shell[1:]) for shell in coordinates]
                )
                resultados[nombre_localidad_procesado] = multipolygon.__geo_interface__
            elif geom_type == "Polygon":
                # Crear un Polygon en Shapely
                polygon = Polygon(shell=coordinates[0], holes=coordinates[1:])
                resultados[nombre_localidad_procesado] = polygon.__geo_interface__
            else:
                print(f"Geometría no soportada para la localidad: {nombre_localidad_procesado}")

        except requests.exceptions.RequestException as e:
            print(f"Error al consultar la API para la localidad {nombre_localidad_procesado}: {e}")
        except KeyError as e:
            print(f"No se pudieron extraer las coordenadas para la localidad: {nombre_localidad_procesado}. Error: {e}")
        except TypeError as e:
            print(f"Formato de coordenadas inválido para {nombre_localidad_procesado}. Error: {e}")

    return resultados


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

def creador_poligono_municipio(path: str,
                               municipio: str = 'SOACHA') -> Dict[str, Dict]:
    """
    Crea un diccionario con la geometría en formato GeoJSON de un municipio específico 
    a partir de un archivo geoespacial.

    Parámetros:
        path (str): Ruta al archivo geoespacial (formato compatible con GeoPandas, como .shp, .geojson, etc.).
        municipio (str, opcional): Nombre del municipio para el cual extraer la geometría.
                                   Por defecto, se usa 'SOACHA'.

    Retorna:
        dict: Diccionario donde la clave es el nombre del municipio y el valor es 
              su geometría en formato GeoJSON. Ejemplo:
              {
                  "SOACHA": {
                      "type": "Polygon",
                      "coordinates": [[[...]]]
                  }
              }
    """
    resultados: Dict[str, Dict] = {}
    gdf_mun = gpd.read_file(path)
    gdf_mun_sub=gdf_mun.query(f"mpio_cnmbr=='{municipio}'").reset_index(drop=True)
    name=procesador_nombre_localidad(gdf_mun_sub['mpio_cnmbr'][0])
    resultados[name]=gdf_mun_sub['geometry'][0].__geo_interface__
    return resultados
