from utils.install_requirements import install_requirements
install_requirements()
import flask
from flask import request, jsonify, render_template
from flask_cors import CORS
from main import main
import requests

app = flask.Flask(__name__)
CORS(app)  # Permitir CORS en todas las rutas

API_KEY = ''  # Reemplaza con tu API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    #responses = "respuesta ||| ['line', [32,3,4,2], [3,2,4,2], 'nombre grafica']"
    responses = main(message)
    if "-> atm" in responses:
        responses = "Aqui esta el cajero mas cercano " + responses
    if "-> Banorte" in responses:
        responses = "Aqui estan la sucursual mas cercana de Banorte " + responses
    responses = responses.split(" ||| ")
    response = responses[0]
    dashboard = "False" 
    if len(responses) > 1:
        dashboard = responses[1]
    MAP = "False"
    if dashboard == "False":
        responses_aux = responses[0].split("->")
        if len(responses_aux) > 1:
            MAP = responses_aux[1]
            response = responses_aux[0]
    return jsonify({'response': response, 'dashboard':dashboard, 'map':MAP})

@app.route('/buscar_cajero', methods=['GET'])
def buscar_cajero():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    keyword = request.args.get('tipo')
    print(keyword)

    if not lat or not lng:
        return jsonify({'error': 'Faltan los parámetros lat o lng'}), 400

    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&keyword={keyword}&key={API_KEY}'


    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si hay un error HTTP

        data = response.json()
        return jsonify(data)  # Enviar respuesta JSON al frontend

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al conectar con la API de Google: {str(e)}'}), 500

@app.route('/obtener_direccion', methods=['GET'])
def obtener_direccion():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not origin or not destination:
        return jsonify({'error': 'Faltan los parámetros origin o destination'}), 400

    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si hay un error HTTP

        data = response.json()
        return jsonify(data)  # Devuelve la respuesta JSON al frontend

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al conectar con la API de Google: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
   # app.run(debug=True)
