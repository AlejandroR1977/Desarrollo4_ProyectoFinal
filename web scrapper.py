import requests
from bs4 import BeautifulSoup
import json
import os

# Función para obtener los detalles de una revista desde SCImago
def obtener_detalles_revista(url):
    """
    Realiza scraping de SCImago para obtener información de una revista.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al obtener la página: {url}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        # Extracción de los datos de la página de SCImago
        sitio_web = soup.find("a", {"class": "external"})["href"]
        h_index = soup.find("span", {"class": "h-index"}).text.strip()
        subject_area = soup.find("span", {"class": "subject-area"}).text.strip()
        publisher = soup.find("span", {"class": "publisher"}).text.strip()
        issn = soup.find("span", {"class": "issn"}).text.strip()
        widget = soup.find("div", {"class": "widget"}).text.strip()
        publication_type = soup.find("span", {"class": "publication-type"}).text.strip()

        # Crear el diccionario con la información extraída
        return {
            "sitio_web": sitio_web,
            "h_index": h_index,
            "subject_area": subject_area,
            "publisher": publisher,
            "issn": issn,
            "widget": widget,
            "publication_type": publication_type
        }
    except AttributeError as e:
        print(f"Error al extraer información de la revista: {url}")
        return None

# Función para verificar si la revista ya está en el JSON
def revista_existente(issn, archivo_json):
    """
    Verifica si la revista ya ha sido procesada, buscando su ISSN.
    """
    if os.path.exists(archivo_json):
        with open(archivo_json, "r", encoding="utf-8") as file:
            data = json.load(file)
            for revista in data:
                if revista["issn"] == issn:
                    return True
    return False

# Función para guardar la información en un archivo JSON
def guardar_en_json(archivo_json, data):
    """
    Guarda los datos recopilados en un archivo JSON.
    """
    with open(archivo_json, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Función para obtener información de las revistas desde el archivo JSON
def obtener_info_revistas(json_input, archivo_json_salida):
    """
    Lee el archivo JSON de revistas y obtiene información de SCImago.
    """
    data_revisadas = []

    # Leer el archivo JSON con el catálogo de revistas
    with open(json_input, "r", encoding="utf-8") as file:
        catalogo_revistas = json.load(file)

    for revista, info in catalogo_revistas.items():
        # Si la revista ya está procesada, no la volvemos a consultar
        issn = info["catalogos"]  # Asumimos que la clave ISSN está en catalogos
        if revista_existente(issn, archivo_json_salida):
            print(f"Revista {revista} ya está procesada.")
            continue
        
        # Obtener los detalles de la revista
        url = f"https://www.scimagojr.com/journalrank.php?journal_id={revista}"  # URL de SCImago, ajustada según sea necesario
        detalles = obtener_detalles_revista(url)

        if detalles:
            data_revisadas.append(detalles)
            print(f"Revista {revista} procesada.")
        
        # Guardar los detalles en el archivo JSON
        guardar_en_json(archivo_json_salida, data_revisadas)

# Ejecutar el scraper para obtener la información de las revistas
archivo_json_catalogo = 'datos/json/revistas.json'  # Archivo de entrada con los catálogos
archivo_json_salida = 'datos/json/revistas_info.json'  # Archivo de salida con la información extraída
obtener_info_revistas(archivo_json_catalogo, archivo_json_salida)

    


