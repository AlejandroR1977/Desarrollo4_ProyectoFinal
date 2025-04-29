import json
import os
import time
import requests
from bs4 import BeautifulSoup

input_json_path = 'datos/json/revistas.json'
output_json_path = 'datos/json/scimago_data.json'

# Cargar catálogo
with open(input_json_path, 'r', encoding='utf-8') as f:
    revistas = json.load(f)

# Cargar información existente si ya fue guardada antes
if os.path.exists(output_json_path):
    with open(output_json_path, 'r', encoding='utf-8') as f:
        datos_scrapeados = json.load(f)
else:
    datos_scrapeados = {}

# Función para buscar la revista en SCImago
def buscar_info_scimago(nombre_revista):
    url_busqueda = f"https://www.scimagojr.com/journalsearch.php?q={nombre_revista.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        r = requests.get(url_busqueda, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        tabla = soup.find('div', class_='search_results')
        if not tabla:
            return None

        primer_resultado = tabla.find('a', href=True)
        if not primer_resultado:
            return None

        url_revista = "https://www.scimagojr.com/" + primer_resultado['href']
        r = requests.get(url_revista, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        def safe_find(label):
            tag = soup.find(string=label)
            return tag.find_next().text.strip() if tag else None

        info = {
            "url": url_revista,
            "h_index": safe_find("H index"),
            "subject_area": None,
            "publisher": safe_find("Publisher"),
            "issn": safe_find("ISSN"),
            "widget": None,
            "publication_type": safe_find("Type")
        }

        # Subject area
        try:
            info["subject_area"] = soup.find('div', class_='journaldescription').find_all('span')[1].text.strip()
        except:
            pass

        # Widget iframe
        try:
            info["widget"] = soup.find('iframe')['src']
        except:
            pass

        return info
    except Exception as e:
        print(f"Error con {nombre_revista}: {e}")
        return None


# Scraping
for revista in revistas:
    if revista in datos_scrapeados:
        continue
    print(f"Buscando información de: {revista}")
    info = buscar_info_scimago(revista)
    if info:
        datos_scrapeados[revista] = info
        time.sleep(3)  # Evitar sobrecargar el sitio

# Guardar nuevo JSON
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(datos_scrapeados, f, indent=4, ensure_ascii=False)



    


