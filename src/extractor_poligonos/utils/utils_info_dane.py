import requests
import aspose.zip as az
import zipfile

def download_file(url, save_path):
    """
    Descarga un archivo desde una URL y lo guarda en una ubicación local.

    Args:
        url (str): La URL del archivo que se desea descargar.
        save_path (str): La ruta local donde se guardará el archivo descargado.

    Raises:
        requests.exceptions.RequestException: Si ocurre un error durante la solicitud HTTP.

    Funcionamiento:
        - Realiza una solicitud HTTP GET a la URL especificada.
        - Descarga el contenido en partes utilizando streaming para manejar archivos grandes.
        - Guarda el archivo descargado en modo binario en la ubicación especificada.

    Ejemplo:
        download_file(
            url="https://example.com/file.zip",
            save_path="file.zip"
        )
    """
    try:
        print(f"Descargando {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica si hubo errores en la solicitud

        # Escribe el contenido del archivo en modo binario
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Archivo guardado en: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar {url}: {e}")

# Función para descomprimir archivos .zip
def descomprimir_zip(ruta_zip, carpeta_destino):
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_destino)
    print(f"Archivo {ruta_zip} descomprimido en {carpeta_destino}")
