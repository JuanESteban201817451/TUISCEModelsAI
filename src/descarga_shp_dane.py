# Externas
import argparse

# propias
from src.utils.utils_info_dane import download_file,descomprimir_zip
from src.statics.list_dict import default_urls_dsh, default_ruta_zip_dsh,default_carpeta_destino_zip_dsh

# Main
def main(urls, ruta_zip, carpeta_destino_zip):
    """
    Descarga y descomprime archivos desde las URLs proporcionadas.

    Parámetros:
    - urls: Lista de tuplas con (URL del archivo, nombre de archivo guardado).
    - ruta_zip: Ruta del archivo .zip descargado.
    - carpeta_destino_zip: Ruta de la carpeta donde se descomprimirá el archivo .zip.
    """
    # Descargar cada archivo
    for url, save_path in urls:
        download_file(url, save_path)

    # Descomprimir los archivos
    if ruta_zip.endswith('.zip'):
        descomprimir_zip(ruta_zip, carpeta_destino_zip)
        
if __name__ == "__main__":
    # Configurar los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description="Descargar y descomprimir archivos desde URLs.")
    parser.add_argument(
        '--urls',
        nargs='+',
        default=[f"{url},{name}" for url, name in default_urls_dsh],
        help="Lista de URLs en el formato: 'url,nombre_archivo'. Ejemplo: 'https://example.com/file1.zip,archivo1.zip'"
    )
    parser.add_argument('--ruta_zip', default=default_ruta_zip_dsh, help="Ruta del archivo .zip descargado.")
    parser.add_argument('--carpeta_destino_zip', default=default_carpeta_destino_zip_dsh, help="Carpeta de destino para el archivo .zip.")
    args = parser.parse_args()

    # Parsear las URLs y los nombres de archivo
    urls = [tuple(url.split(',')) for url in args.urls]

    # Ejecutar la función principal
    main(urls, args.ruta_zip, args.carpeta_destino_zip)
