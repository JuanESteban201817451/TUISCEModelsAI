
# Valores predeterminado Listas y Dicionarios

## descarga_shp_dane.py ---- Ejecutable destinado a la descarga de shp del dane ----------

### Ruta donde se guarda el ZIP
default_ruta_zip_dsh = r".\data\external\MGN2023_MPIO_POLITICO.zip"

### (url de descargs, ruta descarga)
default_urls_dsh  = [
    ("https://geoportal.dane.gov.co/descargas/mgn_2023/MGN2023_MPIO_POLITICO.zip", default_ruta_zip_dsh)
]

### Ruta de destino descomprimida
default_carpeta_destino_zip_dsh  = r".\data\external\MGN2023_MPIO_POLITICO"

## generar_poligonos.py ---- Ejecutable destinado a crear poligonos y archivos para facilitar descarga de imagenes

### Ruta a SHP para descargar municipios
archivo_mun_gp= r'./data/external/MGN2023_MPIO_POLITICO/MGN_ADM_MPIO_GRAFICO.shp'

## Municipio a descargar 
municipio_gp='SOACHA'

### Lista localidades interes
lista_localidades_bogota_gp=['Ciudad Bolívar', 'San Cristóbal']

### URL base para la API de poligonos de localidades en Bogotá
url_base_gp = "https://bogota-laburbano.opendatasoft.com/api/records/1.0/search/?dataset=poligonos-localidades&refine.Nombre+de+la+localidad="

### Distancia maxima a una estacion de transmicable
distancia_maxima_gp=3000

### Diccionario Estaciones de transmicable de interes (Llave nombre de la estacion)
estaciones_transmicable_gp = {
    "Potosí": {
        'PORTAl_SUR': (4.597663047655793, -74.16942291534492),
        'TRES_REYES': (4.583517154195488, -74.17998854232754),
        'SANTA_VIVIANA': (4.577548820375602, -74.17632291534493),
        'POTOSI': (4.569668547284284, -74.1712978134913)
    },
    "Ciudad Bolívar": {
        "PORTAL_DEL_TUNAL": (4.568874258616699, -74.13946745553427),
        "JUAN_PABLO_II": (4.555992907670105, -74.14740979258688),
        "MANITAS": (4.5505494740333985, -74.15058826560421),
        "MIRADOR_DEL_PARAISO": (4.5502151330274065, -74.15891333669026)
    },
    "San Cristóbal": {
        'PORTAL_20_DE_JULIO': (4.56516773895769, -74.09641625108391),
        'LA_VICTORIA': (4.550883883505155, -74.09388602539592),
        'ALTAMIRA': (4.544586492181246, -74.08494407133428)
    }
}

### Dicciona de localidades a buscar poligonos cercanos a una estacion espesifica

dict_localidades_comparar_gp={"Potosí":['CIUDAD_BOLIVAR', 'SOACHA'],
                            "Ciudad Bolívar":['CIUDAD_BOLIVAR'],
                            "San Cristóbal":['SAN_CRISTOBAL']}

### Elemento final localodades, llave, diccionario estaciones
lista_localidades_estaciones_a_comparar_gp= []

for localidad, estaciones in estaciones_transmicable_gp.items():
    localidades_a_comparar = dict_localidades_comparar_gp.get(localidad,[])
    if len(localidades_a_comparar) > 1:
        for localidad_comparar in localidades_a_comparar:
            estructura = {
                "Llave": localidad,
                "Localidad": localidad_comparar,  # Un localidad a la vez
                "Diccionario de estaciones": estaciones
            }
            lista_localidades_estaciones_a_comparar_gp.append(estructura)
    else:
        estructura = {
            "Llave": localidad,
            "Localidad": localidades_a_comparar[0],  # Toma el único elemento
            "Diccionario de estaciones": estaciones
        }
        lista_localidades_estaciones_a_comparar_gp.append(estructura)
