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

# Cargar información existente
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

        info = {
            "url": url_revista,
            "h_index": None,
            "subject_area": [],
            "publisher": None,
            "issn": None,
            "widget": None,
            "publication_type": None
        }

        # Extraer H-Index
        try:
            h_index_tag = soup.find_all('p', class_='hindexnumber')[1]
            info["h_index"] = h_index_tag.text.strip()
        except Exception as e:
            print(f"Error extrayendo H-Index de {nombre_revista}: {e}")

        # Función auxiliar
        def safe_find(label):
            tag = soup.find(string=label)
            return tag.find_next().text.strip() if tag else None

        info["publisher"] = safe_find("Publisher")
        info["issn"] = safe_find("ISSN")

        # Extraer publicación type
        try:
            pub_type_tag = soup.find('h2', string="Publication type")
            if pub_type_tag:
                info["publication_type"] = pub_type_tag.find_next('p').text.strip()
        except:
            pass

        # Extraer área temática (subject areas y categorías)
        try:
            subject_areas = []
            subject_section = soup.find('h2', string="Subject Area and Category")
            if subject_section:
                div = subject_section.find_parent('div')
                for a in div.find_all('a'):
                    subject_areas.append(a.text.strip())
            info["subject_area"] = subject_areas
        except Exception as e:
            print(f"Error extrayendo subject_area de {nombre_revista}: {e}")

        # Extraer widget (en value de input con id embed_code)
        try:
            input_tag = soup.find('input', {'id': 'embed_code'})
            if input_tag and input_tag.has_attr('value'):
                info["widget"] = input_tag['value']
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
    time.sleep(3)

# Guardar nuevo JSON
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(datos_scrapeados, f, indent=4, ensure_ascii=False)



    


