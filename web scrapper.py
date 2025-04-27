import json
import os
import time
import requests
from bs4 import BeautifulSoup

# Cargar revistas desde el archivo anterior
ruta_json = 'datos/json'
archivo_revistas = os.path.join(ruta_json, 'revistas.json')
archivo_revistas_completas = os.path.join(ruta_json, 'revistas_completas.json')

# Verificamos si ya existe un catálogo completo previo
if os.path.exists(archivo_revistas_completas):
    with open(archivo_revistas_completas, 'r', encoding='utf-8') as f:
        revistas_completas = json.load(f)
else:
    revistas_completas = {}

# Cargar el archivo original
with open(archivo_revistas, 'r', encoding='utf-8') as f:
    revistas = json.load(f)

# Función para buscar una revista en SCIMAGO
def buscar_info_scimago(nombre_revista):
    print(f"Buscando {nombre_revista} en SCIMAGO...")

    # Simular búsqueda: reemplazar espacios por %20
    url_busqueda = f"https://www.scimagojr.com/journalsearch.php?q={nombre_revista.replace(' ', '%20')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url_busqueda, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al buscar {nombre_revista}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Intentar encontrar la primera revista del resultado
    revista_link = soup.find('a', class_='search_results_title')
    if not revista_link:
        print(f"No encontrado: {nombre_revista}")
        return None

    # Acceder a la página de la revista
    revista_url = "https://www.scimagojr.com/" + revista_link['href']

    try:
        response = requests.get(revista_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a la revista {nombre_revista}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer los datos
    datos = {}
    try:
        datos['sitio_web'] = soup.find('div', class_='journaldescription').find('a')['href']
    except:
        datos['sitio_web'] = None

    try:
        datos['h_index'] = soup.find('div', class_='hindexnumber').text.strip()
    except:
        datos['h_index'] = None

    try:
        subject_area = soup.find('div', class_='areasection').text.strip()
        datos['subject_area_and_category'] = subject_area
    except:
        datos['subject_area_and_category'] = None

    try:
        publisher = soup.find('div', class_='publisher').text.replace('Publisher', '').strip()
        datos['publisher'] = publisher
    except:
        datos['publisher'] = None

    try:
        issn = soup.find('div', class_='issn').text.replace('ISSN', '').strip()
        datos['issn'] = issn
    except:
        datos['issn'] = None

    try:
        widget = soup.find('textarea', id='journalrank_widget_textarea').text.strip()
        datos['widget'] = widget
    except:
        datos['widget'] = None

    try:
        pub_type = soup.find('div', class_='publicationtype').text.replace('Publication type', '').strip()
        datos['publication_type'] = pub_type
    except:
        datos['publication_type'] = None

    return datos

# Recorremos cada revista
for revista in revistas:
    if revista in revistas_completas:
        print(f"{revista} ya está en el catálogo completo, se omite.")
        continue

    info = buscar_info_scimago(revista)
    if info:
        revistas_completas[revista] = info
        # Guardar inmediatamente para no perder avances
        with open(archivo_revistas_completas, 'w', encoding='utf-8') as f:
            json.dump(revistas_completas, f, indent=4, ensure_ascii=False)
    
    # Respetar al servidor
    time.sleep(2)

print("Proceso terminado.")
