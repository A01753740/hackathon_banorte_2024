def get_category(text, category_list):
    for category in category_list:
        if category in text:
            return category  # Devuelve la categoría encontrada
    return None  # Si no hay coincidencia, devuelve None