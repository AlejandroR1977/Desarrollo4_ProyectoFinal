from flask import Flask, render_template, request

app = Flask(_name_)

# Datos de ejemplo para las áreas, catálogos y revistas (estos deberían ser reemplazados por datos reales de tu base de datos)
areas = ['Matemáticas', 'Física', 'Biología']
catalogos = ['Scopus', 'Springer', 'Scimago']
revistas = [
    {'titulo': 'Revista de Física Avanzada', 'h_index': 25, 'area': 'Física', 'catalogo': 'Scopus'},
    {'titulo': 'Biología Molecular', 'h_index': 30, 'area': 'Biología', 'catalogo': 'Springer'},
    {'titulo': 'Matemáticas Aplicadas', 'h_index': 20, 'area': 'Matemáticas', 'catalogo': 'Scimago'}
]

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/area')
def area():
    return render_template('area.html', areas=areas)

@app.route('/catalogos')
def catalogos_view():
    return render_template('catalogos.html', catalogos=catalogos)

@app.route('/explorar')
def explorar():
    return render_template('explorar.html', revistas=revistas)

@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    query = request.args.get('query', '')
    # Realizar búsqueda en las revistas (por título en este ejemplo)
    resultados = [revista for revista in revistas if query.lower() in revista['titulo'].lower()]
    return render_template('busqueda.html', resultados=resultados)

@app.route('/creditos')
def creditos():
    return render_template('creditos.html')

if _name_ == '_main_':
    app.run(debug=True)
