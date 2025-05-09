from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/areas')
def areas():
    # Aquí se cargarán dinámicamente las áreas desde la base de datos o archivo
    areas_disponibles = ['Ingeniería', 'Ciencias Sociales', 'Salud']
    return render_template('areas.html', areas=areas_disponibles)

@app.route('/catalogos')
def catalogos():
    # Aquí se cargarán dinámicamente los catálogos desde la base de datos o archivo
    catalogos_disponibles = ['Scopus', 'WoS', 'Latindex']
    return render_template('catalogos.html', catalogos=catalogos_disponibles)

@app.route('/explorar')
def explorar():
    abecedario = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    return render_template('explorar.html', letras=abecedario)

@app.route('/explorar/<letra>')
def explorar_por_letra(letra):
    # Aquí deberías buscar en tu base de datos las revistas por letra
    revistas = []  # Revistas por letra (simulación)
    return render_template('revistas_por_letra.html', letra=letra, revistas=revistas)

@app.route('/busqueda')
def busqueda():
    query = request.args.get('q', '')
    # Aquí deberías realizar la búsqueda en tu base de datos
    resultados = []  # Resultados de búsqueda simulados
    return render_template('busqueda.html', query=query, resultados=resultados)

@app.route('/revista/<nombre>')
def detalles_revista(nombre):
    # Aquí deberías obtener los detalles desde tu base de datos
    detalles = {'titulo': nombre, 'HIndex': 30, 'descripcion': 'Descripción de la revista'}
    return render_template('detalles_revista.html', revista=detalles)

@app.route('/creditos')
def creditos():
    alumnos = [
        {'nombre': 'Nombre Apellido', 'foto': 'foto1.jpg'},
        {'nombre': 'Nombre Apellido', 'foto': 'foto2.jpg'}
    ]
    return render_template('creditos.html', alumnos=alumnos)

if __name__ == '__main__':
    app.run(debug=True)
