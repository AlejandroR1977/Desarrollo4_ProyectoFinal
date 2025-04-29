from flask import Flask, jsonify, render_template
import json
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def buscar_journal_id(nombre_revista):
    """Realiza una búsqueda flexible en SCImago y obtiene el journal_id si existe"""
    # Formatear la búsqueda
    query = nombre_revista.replace(' ', '+')
    url_busqueda = f"https://www.scimagojr.com/journalsearch.php?q={query}"
    
    try:
        response = requests.get(url_busqueda, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error al buscar {nombre_revista}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    resultados = soup.select('div.search_results a')

    if not resultados:
        print(f"❌ No se encontraron resultados para: {nombre_revista}")
        return None
    
    # Tomar el primer resultado de búsqueda
    primer_resultado = resultados[0]
    href = primer_resultado.get('href')
    if "journalrank.php?journal_id=" in href:
        journal_id = href.split('journal_id=')[1]
        print(f"✅ Encontrado: {nombre_revista} --> journal_id={journal_id}")
        return journal_id
    else:
        print(f"❌ No se encontró un journal_id para: {nombre_revista}")
        return None

# Ruta para obtener la información de todas las revistas
@app.route('/revistas', methods=['GET'])
def obtener_revistas():
    try:
        with open("datos/json/revistas_info.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        revistas_con_ids = []
        for revista in data:
            nombre = revista.get("nombre")
            print(f"🔍 Buscando journal_id para: {nombre}")
            journal_id = buscar_journal_id(nombre)
            time.sleep(1)  # Para no saturar SCImago
            if journal_id:
                revista["journal_id"] = journal_id
            else:
                revista["journal_id"] = None
            revistas_con_ids.append(revista)

        return jsonify(revistas_con_ids)  # Devuelve la información de las revistas en formato JSON
    except FileNotFoundError:
        return jsonify({"error": "No se encontraron datos."}), 404

# Ruta para la página principal (interfaz de usuario)
@app.route('/')
def index():
    return render_template("index.html")  # Carga el archivo HTML

if __name__ == '__main__':
    app.run(debug=True)
