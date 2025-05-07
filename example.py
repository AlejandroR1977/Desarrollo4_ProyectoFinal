import os
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

scimago_url = 'https://www.scimagojr.com'
search_url = 'https://www.scimagojr.com/journalsearch.php?q='
catalogo_path = 'datos/json/catalogo_revistas.json'

def scrap(url):
    page = requests.get(url, headers=headers, timeout=15)
    if page.status_code != 200:
        raise Exception(f"Error: {page.status_code} en {url}")
    return page

def find_journal_url(journal_title: str):
    ''' Busca la URL de la revista en Scimago '''
    journal_search_url = f"{search_url}{journal_title.replace(' ', '+')}"
    journal_search_page = scrap(journal_search_url)
    soup = BeautifulSoup(journal_search_page.text, 'html.parser')
    first_result = soup.select_one('span.jrnlname')
    journal_url = first_result.find_parent('a')['href'] if first_result else ''
    return f'{scimago_url}/{journal_url}' if journal_url else None

def get_journal_data(journal_url: str):
    ''' Extrae la información requerida de la página de la revista '''
    page = scrap(journal_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    def safe_text(selector):
        tag = soup.select_one(selector)
        return tag.text.strip() if tag else ''

    # H-Index
    h_index = safe_text('p.hindexnumber')

    # Sitio web
    website = soup.select_one('a[href^="http"]:not([href*="scimagojr"])')
    website_url = website['href'] if website else ''

    # Publisher, ISSN, Publication Type
    publisher, issn, pub_type = '', '', ''
    rows = soup.select('div.grid_12 > div.data > table tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            if 'Publisher' in key:
                publisher = value
            elif 'ISSN' in key:
                issn = value
            elif 'Type' in key:
                pub_type = value

    # Subject Area and category
    subjects = [li.text.strip() for li in soup.select('ul.subjectarealist li')]

    # Widget
    widget = ''
    widget_box = soup.find('textarea', {'id': 'embed'})
    if widget_box:
        widget = widget_box.text.strip()

    return {
        'Sitio web': website_url,
        'H-Index': h_index,
        'Subject Area and category': subjects,
        'Publisher': publisher,
        'ISSN': issn,
        'Widget': widget,
        'Publication Type': pub_type
    }

def load_catalog():
    if os.path.exists(catalogo_path):
        with open(catalogo_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_catalog(catalog):
    os.makedirs(os.path.dirname(catalogo_path), exist_ok=True)
    with open(catalogo_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

def main():
    catalog = load_catalog()

    revistas = [
        'Acta Materialia',
        'Nature',
        'Journal of Artificial Intelligence Research'
        # Puedes añadir más revistas aquí
    ]

    for nombre in revistas:
        if nombre in catalog:
            print(f'✔ {nombre} ya está en el catálogo. Se omite.')
            continue

        try:
            print(f'⏳ Buscando {nombre}...')
            url = find_journal_url(nombre)
            if not url:
                print(f'⚠ No se encontró la revista "{nombre}"')
                continue

            data = get_journal_data(url)
            catalog[nombre] = data
            print(f'✅ Datos obtenidos para: {nombre}')
        except Exception as e:
            print(f'❌ Error al procesar {nombre}: {e}')

    save_catalog(catalog)
    print('📁 Catálogo actualizado correctamente.')

if __name__ == '__main__':
    main()