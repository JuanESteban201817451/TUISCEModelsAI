# Bibliotecas estándar
from math import radians, cos, sin, sqrt, atan2  # Para cálculos matemáticos como la fórmula de haversine
from typing import Union, List, Dict,Any, Optional  # Para anotaciones de tipos en funciones
from itertools import cycle
import os
# Bibliotecas de terceros para trabajar con geometrías y datos espaciales
from shapely.geometry import box, Polygon, MultiPolygon  # Para manipulación de geometrías (polígonos, multipolígonos)
import geopandas as gpd  # Para manejo de datos espaciales y operaciones GIS
import folium # para crear el mapa
import simplekml

def dividir_poligono(poligono: Union[Polygon, MultiPolygon], tamano_m: int = 200) -> List[Polygon]:
    """
    Divide un polígono o multipolígono en una grilla de subpolígonos cuadrados de tamaño tamano_m x tamano_m (en metros),
    restringidos al área del polígono original.
    
    Args:
        poligono (Polygon or MultiPolygon): Polígono o multipolígono original (en coordenadas EPSG:4326).
        tamano_m (int): Tamaño de los subpolígonos (en metros).
    
    Returns:
        list: Lista de subpolígonos (en coordenadas EPSG:4326).
    """
    # Convertir el polígono al sistema de coordenadas UTM para trabajar en metros
    gdf = gpd.GeoDataFrame({'geometry': [poligono]}, crs="EPSG:4326")
    gdf_utm = gdf.to_crs(gdf.estimate_utm_crs())

    # Obtener los límites del polígono
    bounds = gdf_utm.geometry[0].bounds
    xmin, ymin, xmax, ymax = bounds

    subpoligonos = []

    # Crear una grilla de subpolígonos y recortar al polígono original
    x = xmin
    while x < xmax:
        y = ymin
        while y < ymax:
            subpoligono = box(x, y, x + tamano_m, y + tamano_m)
            # Recortar el subpolígono al polígono original
            interseccion = gdf_utm.geometry[0].intersection(subpoligono)
            if not interseccion.is_empty:
                subpoligonos.append(interseccion)
            y += tamano_m
        x += tamano_m

    # Convertir los subpolígonos de vuelta a EPSG:4326
    gdf_subpoligonos = gpd.GeoDataFrame({'geometry': subpoligonos}, crs=gdf_utm.crs)
    gdf_subpoligonos = gdf_subpoligonos.to_crs("EPSG:4326")

    return gdf_subpoligonos.geometry.tolist()


def crear_diccionario_subpoligonos(poligonos_localidades: Dict[str, Dict],
                                   tamano_m: int = 200) -> Dict[str, Dict[str, Dict]]:
    """
    Crea un diccionario estructurado con los subpolígonos de cada localidad.
    
    Args:
        poligonos_localidades (dict): Diccionario de localidades y sus polígonos originales.
        tamano_m (int): Tamaño de los subpolígonos en metros.
    
    Returns:
        dict: Diccionario estructurado con los subpolígonos.
    """
    diccionario = {}

    for localidad, geojson in poligonos_localidades.items():
        # Convertir el GeoJSON a un objeto Shapely (Polygon o MultiPolygon)
        if geojson['type'] == "MultiPolygon":
            poligono = MultiPolygon([Polygon(shell[0], shell[1:]) for shell in geojson['coordinates']])
        elif geojson['type'] == "Polygon":
            poligono = Polygon(shell=geojson['coordinates'][0], holes=geojson['coordinates'][1:])
        else:
            print(f"Tipo de geometría no soportado: {geojson['type']}")
            continue

        # Dividir el polígono o multipolígono en subpolígonos
        subpoligonos = dividir_poligono(poligono, tamano_m)

        # Crear el diccionario de subpolígonos
        diccionario[localidad] = {
            f"subpoligono_{i+1}_{localidad}": subpoligono.__geo_interface__
            for i, subpoligono in enumerate(subpoligonos)
        }

    return diccionario


def haversine(lat1: float,
              lon1: float,
              lat2: float,
              lon2: float) -> float:
    """
    Calcula la distancia geodésica entre dos puntos dados por sus coordenadas latitud/longitud.

    Parámetros:
        lat1 (float): Latitud del primer punto en grados.
        lon1 (float): Longitud del primer punto en grados.
        lat2 (float): Latitud del segundo punto en grados.
        lon2 (float): Longitud del segundo punto en grados.

    Retorna:
        float: Distancia entre los dos puntos en metros.
    """
    R = 6371000  # Radio de la Tierra en metros
    phi1, phi2 = radians(lat1), radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def calcular_centroide(polygon: dict) -> tuple:
    """
    Calcula el centroide de un polígono o multipolígono.

    Parámetros:
        polygon (dict): Geometría del polígono en formato GeoJSON. Debe tener las claves:
            - 'type' (str): Tipo de geometría, puede ser 'Polygon' o 'MultiPolygon'.
            - 'coordinates' (list): Coordenadas del polígono. Si es un MultiPolygon, será una lista de listas.

    Retorna:
        tuple: Coordenadas del centroide en formato (latitud, longitud).

    Ejemplo:
        polygon = {
            'type': 'Polygon',
            'coordinates': [[
                (-74.1, 4.6),
                (-74.2, 4.6),
                (-74.2, 4.7),
                (-74.1, 4.7),
                (-74.1, 4.6)
            ]]
        }
        calcular_centroide(polygon) -> (4.65, -74.15)
    """
    # Si es un multipolígono, procesa el primer anillo del primer polígono
    if polygon['type'] == 'MultiPolygon':
        coords = polygon['coordinates'][0][0]  # Primer anillo exterior del primer polígono
    else:  # Caso de polígono simple
        coords = polygon['coordinates'][0]
    x, y = zip(*coords)  # Separar latitudes (y) y longitudes (x)
    return sum(y) / len(y), sum(x) / len(x)  # Retorna (latitud, longitud)

from typing import Dict

def filtrar_poligonos_por_distancia(
    localidad: str,
    subpoligonos: Dict[str, Dict],
    estaciones: Dict[str, tuple],
    distancia_maxima: float = 800
) -> Dict[str, Dict]:
    """
    Filtra los subpolígonos que están dentro de una distancia máxima desde al menos una estación
    y agrega información adicional en la salida.

    Parámetros:
        localidad (str): Nombre de la localidad para filtrar los subpolígonos correspondientes.
        subpoligonos (dict): Diccionario principal de subpolígonos por localidad en formato GeoJSON. Ejemplo:
            {
                "Localidad 1": {
                    "subpoligono_1": {"type": "Polygon", "coordinates": [...]},
                    "subpoligono_2": {"type": "Polygon", "coordinates": [...]}
                },
                "Localidad 2": {
                    ...
                }
            }
        estaciones (dict): Diccionario con los nombres de estaciones y sus coordenadas (latitud, longitud). Ejemplo:
            {
                "Estación 1": (lat1, lon1),
                "Estación 2": (lat2, lon2)
            }
        distancia_maxima (float): Distancia máxima en metros para considerar un polígono como "cercano". Por defecto es 800 metros.

    Retorna:
        dict: Diccionario de subpolígonos que cumplen con la condición de estar dentro de la distancia máxima a alguna estación.
        Cada elemento incluye:
            - 'localida' (str): Nombre de la localidad correspondiente.
            - 'nombre' (str): Nombre del subpolígono.
            - 'Estacion_cercana' (str): Nombre de la estación más cercana dentro del rango.
            - 'Dict_poligono' (dict): Geometría del subpolígono en formato GeoJSON.
    """

    # Diccionario para almacenar los subpolígonos que cumplen con la condición
    poligonos_filtrados = {}
    subpoligonos_sub=subpoligonos[localidad]
    # Iterar sobre cada subpolígono en el diccionario
    for nombre, poligono in subpoligonos_sub.items():
        # Calcular el centroide del subpolígono
        centroide_lat, centroide_lon = calcular_centroide(poligono)
        dentro_del_radio = False  # Bandera para verificar si está dentro del rango
        estacion_cercana = None  # Almacena la estación más cercana dentro del rango

        # Comparar la distancia del centroide a cada estación
        for estacion, (lat, lon) in estaciones.items():
            distancia = haversine(centroide_lat, centroide_lon, lat, lon)
            if distancia <= distancia_maxima:  # Si está dentro de la distancia máxima
                dentro_del_radio = True
                estacion_cercana = estacion
                break  # No es necesario seguir verificando con otras estaciones

        # Si el subpolígono está dentro del rango de alguna estación, añadirlo al resultado
        if dentro_del_radio:
            poligonos_filtrados[nombre] = {
                'localida':localidad,
                'nombre': nombre,
                'Estacion_cercana': estacion_cercana,
                'Dict_poligono': poligono
            }

    return poligonos_filtrados




def creador_mapa(
    diccionario_poligonos: Dict[str, Any],
    diccionario_sub_poligonos: Optional[Dict[str, Dict[str, Any]]] = None,
    guardar_path: Optional[str] = None
) -> folium.Map:
    """
    Crea un mapa interactivo centrado en Bogotá con polígonos y, opcionalmente, subpolígonos.

    Parámetros:
        diccionario_poligonos (dict): Diccionario con las geometrías principales de las localidades.
                                       Claves son los nombres de las localidades y valores son geometrías GeoJSON.
        diccionario_sub_poligonos (dict, opcional): Diccionario con subpolígonos organizados por localidad.
                                                    Claves son los nombres de las localidades y valores son diccionarios con subpolígonos.
                                                    Si se proporciona, los subpolígonos se grafican automáticamente.
        guardar_path (str, opcional): Ruta donde se guardará el archivo HTML del mapa. Si es `None`, no guarda el archivo.

    Retorna:
        folium.Map: El mapa interactivo generado.
    """
    # Crear el mapa centrado en Bogotá, ajustado 1 km al sur
    m = folium.Map(location=[4.6 - 0.05, -74.1], zoom_start=12)

    # Lista de colores para asignar dinámicamente a las localidades
    colores = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray']
    colores_ciclo = cycle(colores)  # Ciclo infinito de colores

    # Crear un diccionario de colores asignados dinámicamente a cada localidad
    colores_localidades = {localidad: next(colores_ciclo) for localidad in diccionario_poligonos.keys()}

    # Función para definir estilos en función de la localidad
    def get_style_function(localidad):
        color = colores_localidades.get(localidad, 'black')  # Color predeterminado: negro si no se encuentra
        return lambda x: {'color': color, 'fillOpacity': 0.5}

    # Agregar las localidades originales al mapa
    for localidad, geojson in diccionario_poligonos.items():
        folium.GeoJson(
            data=geojson,
            name=localidad,
            style_function=get_style_function(localidad),  # Llamar a la función de estilo
            popup=folium.Popup(localidad)  # Muestra el nombre del subpolígono al hacer clic
        ).add_to(m)

    # Agregar los subpolígonos al mapa si se proporciona el diccionario
    if diccionario_sub_poligonos:
        for localidad, subpoligonos in diccionario_sub_poligonos.items():
            for subpoligono_nombre, subpoligono_geojson in subpoligonos.items():
                folium.GeoJson(
                    data=subpoligono_geojson,
                    style_function=lambda x: {'color': 'black', 'fillOpacity': 0},  # Cuadraditos en negro sin relleno
                    popup=folium.Popup(subpoligono_nombre)  # Muestra el nombre del subpolígono al hacer clic
                ).add_to(m)

    # Guardar el mapa si se proporciona una ruta
    if guardar_path:
        m.save(guardar_path)

    return m



# Ruta base donde se crearán las carpetas
def creardor_carpetas_y_kmls(conjunto_total:list[dict],base_path:str = r"D:\Tesis_JE_fotos"):
    for subpoligonos_cercanos in conjunto_total:
        print("Su ruta base será el lugar donde se descargarán y generarán las carpetas para almacenar los archivos. Se recomienda usar una unidad externa o una carpeta con suficiente espacio de almacenamiento.")
        # Crear las carpetas y archivos necesarios
        for subpoligono, datos in subpoligonos_cercanos.items():
            localidad = datos['localida']
            estacion_cercana = datos['Estacion_cercana']
            nombre = datos['nombre']
            dict_poligono = datos['Dict_poligono']

            # Rutas de las carpetas
            ruta_localidad = os.path.join(base_path, localidad)
            ruta_estacion = os.path.join(ruta_localidad, estacion_cercana)
            ruta_subpoligono = os.path.join(ruta_estacion, nombre)

            # Crear las carpetas si no existen
            os.makedirs(ruta_subpoligono, exist_ok=True)

            # Crear el archivo KML en la carpeta correspondiente
            kml = simplekml.Kml()

            # Manejar Polygon y MultiPolygon
            if dict_poligono['type'] == 'Polygon':
                # Polígono simple
                coordinates = [
                    (coord[0], coord[1]) for coord in dict_poligono['coordinates'][0]
                ]
                pol = kml.newpolygon(name=nombre)
                pol.outerboundaryis = coordinates
                pol.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.green)  # Sin relleno
                pol.style.polystyle.fill = False  # Desactiva el relleno
                pol.style.linestyle.color = simplekml.Color.red  # Contorno rojo
                pol.style.linestyle.width = 2  # Grosor del contorno
            elif dict_poligono['type'] == 'MultiPolygon':
                # Multipolígono
                for i, multipolygon_coords in enumerate(dict_poligono['coordinates']):
                    coordinates = [
                        (coord[0], coord[1]) for coord in multipolygon_coords[0]
                    ]
                    pol = kml.newpolygon(name=f"{nombre}_part_{i+1}")
                    pol.outerboundaryis = coordinates
                    pol.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.green)  # Sin relleno
                    pol.style.polystyle.fill = False  # Desactiva el relleno
                    pol.style.linestyle.color = simplekml.Color.red  # Contorno rojo
                    pol.style.linestyle.width = 2  # Grosor del contorno

            # Guardar el archivo KML
            kml_file_path = os.path.join(ruta_subpoligono, f"poligono.kml")
            kml.save(kml_file_path)

            print(f"Archivo KML creado: {kml_file_path}")

            # Guardar el diccionario filtrado en un archivo de texto dentro de la carpeta
            dict_file_path = os.path.join(ruta_subpoligono, f"{nombre}_datos.txt")
            with open(dict_file_path, "w", encoding="utf-8") as f:
                f.write(str(datos))

            print(f"Archivo de diccionario creado: {dict_file_path}")

        print("Proceso completado.")
