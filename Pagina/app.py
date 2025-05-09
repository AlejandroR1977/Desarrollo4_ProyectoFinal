from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_session import Session
import json
import os

app = Flask(__name__)

# Configuración de la sesión
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Datos ficticios de usuarios
USUARIOS = {
    "admin": "1234",
    "user1": "password1",
    "user2": "password2"
}

# Cargar datos de revistas
with open('../datos/json/scimago_data.json', encoding='utf-8') as f:
    scimago_data = json.load(f)

# Obtener áreas únicas
def obtener_areas():
    areas = set()
    for revista in scimago_data.values():
        areas.update(revista.get("subject_area", []))
    return sorted(areas)

# Obtener catálogos únicos
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

# Ruta principal
@app.route('/')
def index():
    if 'usuario' not in session:
        flash('Debes iniciar sesión primero.', 'warning')
        return redirect(url_for('login'))
    return render_template('index.html')

# Ruta de exploración
@app.route('/explorar')
def explorar():
    return render_template('explorar.html', revistas=scimago_data)

# Ruta de búsqueda
@app.route('/busqueda', methods=['GET'])
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

# Ruta de catálogos generales
@app.route('/catalogos')
def catalogos_view():
    catalogos = obtener_catalogos()
    return render_template('catalogos.html', catalogos=catalogos)

# Ruta de catálogo específico
@app.route('/catalogos/<catalogo>')
def catalogo_detalle(catalogo):
    resultados = [
        {
            "id": idx,
            "titulo": titulo,
            "h_index": data.get("h_index", "N/A"),
            "url": data.get("url", "#")
        }
        for idx, (titulo, data) in enumerate(scimago_data.items())
        if catalogo == data.get("publisher", "Desconocido")
    ]
    catalogos = obtener_catalogos()
    return render_template('catalogos.html', catalogo=catalogo, resultados=resultados, catalogos=catalogos)

# Ruta de áreas
@app.route('/area', methods=['GET'])
def area():
    areas = obtener_areas()
    area_seleccionada = None
    revistas = []

    if 'area' in request.args:
        area_id = request.args['area']
        area_seleccionada = area_id
        # Filtra las revistas que pertenecen al área seleccionada
        revistas = [
            {
                "id": idx,
                "titulo": titulo,
                "h_index": data.get("h_index", "N/A"),
                "url": data.get("url", "#")
            }
            for idx, (titulo, data) in enumerate(scimago_data.items())
            if area_id in data.get("subject_area", [])
        ]
    
    return render_template('area.html', areas=areas, area_seleccionada=area_seleccionada, revistas=revistas)

@app.route('/area/<area_nombre>')
def area_detalle(area_nombre):
    resultados = [
        {
            "id": idx,
            "titulo": titulo,
            "h_index": data.get("h_index", "N/A"),
            "url": data.get("url", "#")
        }
        for idx, (titulo, data) in enumerate(scimago_data.items())
        if area_nombre in data.get("subject_area", [])
    ]
    areas = obtener_areas()
    return render_template('area.html', area_nombre=area_nombre, resultados=resultados, areas=areas)

# Ruta de créditos
@app.route('/creditos')
def creditos():
    return render_template('creditos.html')


if __name__ == '__main__':
    app.run(debug=True)

    


