import json

def load_json(file_path):

    # Cargar el archivo JSON y convertirlo en un diccionario
    with open(file_path, 'r') as archivo:
        diccionario = json.load(archivo)

    return diccionario
