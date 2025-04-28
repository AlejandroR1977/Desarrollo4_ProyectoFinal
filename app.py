from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Rutas de los archivos JSON
ruta_json = 'datos/json'
archivo_revistas_completas = os.path.join(ruta_json, 'revistas_completas.json')

# Verificamos si ya existe un catálogo completo previo
if os.path.exists(archivo_revistas_completas):
    with open(archivo_revistas_completas, 'r', encoding='utf-8') as f:
        revistas_completas = json.load(f)
else:
    revistas_completas = {}

@app.route('/')
def index():
    """
    Página principal que muestra la lista de revistas completas.
    """
    return render_template('index.html', revistas_completas=revistas_completas)

@app.route('/scrape', methods=['GET'])
def scrape():
    """
    Endpoint que devuelve un mensaje indicando que el scraping se ha completado.
    Aquí podrías agregar la lógica para iniciar el scraping.
    """
    return jsonify({"status": "Proceso de scraping iniciado"})

if __name__ == '__main__':
    app.run(debug=True)
