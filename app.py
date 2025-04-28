from flask import Flask, jsonify, render_template
import json

<<<<<<< HEAD
app = Flask(__name__)  # CORREGIDO
=======
app = Flask(_name_)
>>>>>>> aba474b297384929895aa725ebb680f0389e6fda

# Ruta para obtener la información de todas las revistas
@app.route('/revistas', methods=['GET'])
def obtener_revistas():
    try:
        with open("datos/json/revistas_info.json", "r", encoding="utf-8") as file:
            data = json.load(file)
<<<<<<< HEAD
        return jsonify(data)
=======
        return jsonify(data)  # Devuelve la información de las revistas en formato JSON
>>>>>>> aba474b297384929895aa725ebb680f0389e6fda
    except FileNotFoundError:
        return jsonify({"error": "No se encontraron datos."}), 404

# Ruta para la página principal (interfaz de usuario)
@app.route('/')
def index():
<<<<<<< HEAD
    return render_template("index.html")

if __name__ == '__main__':  # CORREGIDO
    app.run(debug=True)
=======
    return render_template("index.html")  # Carga el archivo HTML

if _name_ == '_main_':
    app.run(debug=True)
>>>>>>> aba474b297384929895aa725ebb680f0389e6fda
