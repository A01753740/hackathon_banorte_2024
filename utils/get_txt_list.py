def txt_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lineas = file.readlines()  # Lee todas las líneas del archivo
    lista_strings = [linea.strip() for linea in lineas]  # Elimina espacios en blanco y saltos de línea
    return lista_strings