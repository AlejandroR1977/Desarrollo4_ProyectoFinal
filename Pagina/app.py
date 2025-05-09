from flask import Flask, render_template, request
import json
<<<<<<< HEAD
import os
from flask_session import Session
from flask import session, redirect, url_for, flash

app = Flask(__name__)

# Configuración de la sesión
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Datos ficticios de usuarios (en un entorno real, esto iría en una base de datos)
USUARIOS = {
    "admin": "1234",
    "user1": "password1",
    "user2": "password2"
}

with open('../datos/json/scimago_data.json', encoding='utf-8') as f:
    revistas = json.load(f)

# Obtener áreas y catálogos únicas
def obtener_areas():
    areas = set()
    for revista in scimago_data.values():
        areas.update(revista.get("subject_area", []))
    return sorted(areas)

def obtener_catalogos():
    catalogos = set()
    for revista in scimago_data.values():
        publisher = revista.get("publisher", "Desconocido")
        catalogos.add(publisher)
    return sorted(catalogos)

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USUARIOS and USUARIOS[username] == password:
            session['usuario'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Ruta de cierre de sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'usuario' not in session:
        flash('Debes iniciar sesión primero.', 'warning')
        return redirect(url_for('login'))
    return render_template('index.html')


=======

app = Flask(__name__)

with open('datos/scimago_data.json', encoding='utf-8') as f:
    revistas = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

>>>>>>> bcf605a6a8798875833f0d1bc0061a5faa86c548
@app.route('/explorar')
def explorar():
    return render_template('explorar.html', revistas=revistas)

<<<<<<< HEAD
@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    query = request.args.get('query', '').strip().lower()
    resultados = []

    if query:
        for titulo, data in scimago_data.items():
            if query in titulo.lower():
                resultados.append({
                    "titulo": titulo,
                    "h_index": data["h_index"],
                    "url": data["url"],
                    "areas": data["subject_area"],
                    "catalogo": data.get("publisher", "Desconocido")
                })

    return render_template('busqueda.html', query=query, resultados=resultados)

@app.route('/catalogos')
def catalogos_view():
    catalogos = obtener_catalogos()
    return render_template('catalogos.html', catalogos=catalogos)

@app.route('/catalogos/<catalogo>')
def catalogo_detalle(catalogo):
    resultados = [
        {"titulo": titulo, "h_index": data["h_index"], "url": data["url"]}
        for titulo, data in scimago_data.items()
        if catalogo == data.get("publisher", "Desconocido")
    ]
    return render_template('catalogos.html', catalogo=catalogo, resultados=resultados)
=======
@app.route('/buscar')
def buscar():
    query = request.args.get('q', '').lower()
    resultados = [r for r in revistas if query in r['title'].lower()]
    return render_template('buscar.html', resultados=resultados, query=query)

@app.route('/catalogos')
def catalogos():
    return render_template('catalogos.html')
>>>>>>> bcf605a6a8798875833f0d1bc0061a5faa86c548

@app.route('/area')
def area():
    return render_template('area.html')

@app.route('/creditos')
def creditos():
    return render_template('creditos.html')

if __name__ == '__main__':
    app.run(debug=True)

    


