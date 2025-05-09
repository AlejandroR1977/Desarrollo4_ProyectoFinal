from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open('datos/scimago_data.json', encoding='utf-8') as f:
    revistas = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explorar')
def explorar():
    return render_template('explorar.html', revistas=revistas)

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '').lower()
    resultados = [r for r in revistas if query in r['title'].lower()]
    return render_template('buscar.html', resultados=resultados, query=query)

@app.route('/catalogos')
def catalogos():
    return render_template('catalogos.html')

@app.route('/area')
def area():
    return render_template('area.html')

@app.route('/creditos')
def creditos():
    return render_template('creditos.html')

if __name__ == '__main__':
    app.run(debug=True)

    


