from utils.get_prompt import get_location_prompt


from langchain_core.messages import HumanMessage

from langchain_core.messages import AIMessage

class LocationAgent:
    def __init__(self, model,human_query):
        self.model = model
        self.prompt = get_location_prompt("prompts/location_prompt.txt",human_query)

    def get_keyword(self):
        answer = self.model.invoke([HumanMessage(content=self.prompt)])
        return answer.content