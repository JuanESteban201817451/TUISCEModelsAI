import os 
import argparse
from utils.procesador import procesar_kml_y_foto

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

    args = parser.parse_args()
    ruta_base = args.ruta_base
    nombre_foto = args.nombre_foto

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
                ruta_jpg=ruta_subcarpeta + f'\{nombre_foto}.jpg'
                if os.path.exists(ruta_jpg):
                    continue
                try:
                    procesar_kml_y_foto(ruta_subcarpeta, nombre_foto)
                except Exception as e:
                    print(f"Error procesando {ruta_subcarpeta}: {e}")
            else:
                print(f"{ruta_subcarpeta} no es una carpeta. Ignorando...")        


if __name__ == "__main__":
    main()
