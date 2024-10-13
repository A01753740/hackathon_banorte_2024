from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import MessagesPlaceholder
import json
import numpy as np

# Function to read the prompt from a text file
def read_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        prompt_content = file.read()
    return prompt_content

def dict_to_str(d):
    return "\n".join(f"{key}: {value}" for key, value in d.items())

def get_chat_prompt(file_path, personal_info):
    # Read the system message from the file
    system_message = read_prompt_from_file(file_path)

    # Convert personal_info (dictionary) to a custom string
    personal_info_str = dict_to_str(personal_info)

    # Define the variables to be substituted in the prompt
    variables = {
        'personal_info': personal_info_str
    }

    # Apply variable substitutions
    system_message_formatted = system_message.format(**variables)

    # Define the prompt with the system message from the file
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message_formatted,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    return prompt
def topics_prompt(file_path, topics):
    # Leer el archivo .txt y convertirlo en string
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()

    # Convertir la lista de tópicos en un string separado por comas
    topics_str = ', '.join(topics)

    # Reemplazar {topics} en el prompt con la lista de tópicos
    prompt = prompt.replace("{topics}", topics_str)

    return prompt

def get_profile_manager_prompt(file_path,human_query,functions,min_date,max_date):
    # Leer el archivo y convertirlo en string
    with open(file_path, 'r') as archivo:
        prompt = archivo.read()

    # Reemplazar las variables en el prompt
    prompt_reemplazado = prompt.replace("{functions}", str(functions)) \
                               .replace("{min_date}", str(min_date)) \
                               .replace("{max_date}", str(max_date))

    prompt = prompt_reemplazado + "\n{human_query}".replace("{human_query}",human_query)

    return prompt_reemplazado

def convert_numpy_types(data):
    """Convierte los tipos de numpy a tipos nativos de Python"""
    if isinstance(data, dict):
        return {k: convert_numpy_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(v) for v in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()  # Convierte arrays de numpy a listas de Python
    else:
        return data

def get_insights_prompt(file_path, user_info, context_data, human_query):
    # Leer el archivo que contiene el template del prompt
    with open(file_path, "r") as file:
        prompt_template = file.read()

    # Convertir los tipos de numpy a tipos nativos de Python en user_info y context_data
    user_info = convert_numpy_types(user_info)
    context_data = convert_numpy_types(context_data)

    # Convertir los diccionarios a formato JSON para que se vean bien en el prompt
    user_info_str = json.dumps(user_info, indent=4)
    context_data_str = json.dumps(context_data, indent=4)

    # Reemplazar las variables en el template
    prompt = prompt_template.format(
        user_info=user_info_str,
        context_data=context_data_str,
        human_query=human_query
    )

    # Retornar el prompt generado
    return prompt

def get_location_prompt(file_path, human_query):
    # Leer el contenido del archivo txt
    with open(file_path, 'r') as file:
        prompt = file.read()

    # Reemplazar la variable {human_query} en el contenido
    prompt_final = prompt.replace('{human_query}', human_query)

    # Retornar el prompt final
    return prompt_final