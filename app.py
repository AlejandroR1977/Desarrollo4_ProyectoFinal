from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)  # CORREGIDO

# Ruta para obtener la información de todas las revistas
@app.route('/revistas', methods=['GET'])
def obtener_revistas():
    try:
        with open("datos/json/revistas_info.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "No se encontraron datos."}), 404

# Ruta para la página principal (interfaz de usuario)
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':  # CORREGIDO
    app.run(debug=True)
