import pandas as pd
import json
import numpy as np
from utils.load_json import load_json
from utils.get_prompt import get_profile_manager_prompt, get_insights_prompt
from utils.get_txt_list import txt_to_list


from langchain_core.messages import HumanMessage

from langchain_core.messages import AIMessage
from functions.agent_functions import obtener_resumen

class ProfileManager:
    def __init__(self, model):
        self.model = model
        self.profile_data = pd.read_csv("data/profile_data.csv")
        self.profile_data['Fecha de Transaccion'] = pd.to_datetime(self.profile_data['Fecha de Transaccion'], format='%d/%m/%y')

        # Verifica si el DataFrame está vacío
        if self.profile_data.empty:
            self.min_date = "No history"
            self.max_date = "No history"
        else:
            self.min_date = self.profile_data['Fecha de Transaccion'].min()
            self.max_date = self.profile_data['Fecha de Transaccion'].max()

        self.functions = txt_to_list('data/functions.txt')
        self.client_info = load_json("data/personal_info.json")

    def view_data(self):
        print(self.profile_data)

    def get_function(self, human_query):
        prompt = get_profile_manager_prompt(
            file_path="prompts/profile_manager_prompt.txt",
            human_query=human_query,
            functions=self.functions,
            min_date=self.min_date,
            max_date=self.max_date
        )
        print(prompt)
        answer = self.model.invoke([HumanMessage(content=prompt)])
        print(answer.content)
        return answer.content

    def act(self, human_query):
        json_flag = False
        while not json_flag:
            try:
                json_data = self.get_function(human_query)
                data = json.loads(json_data)
                json_flag = True
                break
            except:
                pass

        # Extraer los argumentos
        try:
            function_name = data["function_call"]["name"]
            arguments = data["function_call"]["arguments"]

            # Verificar si el nombre de la función es "obtener_resumen" y llamarla
            if function_name == "obtener_resumen":
                context_data = obtener_resumen(self.profile_data, arguments["fecha_inicio"], arguments["fecha_final"])

                prompt = get_insights_prompt("prompts/insight_prompt.txt", self.client_info, context_data, human_query)
                print(prompt)
                resumen = self.model.invoke([HumanMessage(content=prompt)])
                return resumen.content

        except Exception as e:
            print("ACT Error:", e)
