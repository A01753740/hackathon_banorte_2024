# Install required libraries
from agents.chatbot import Chatbot
from langchain_openai import ChatOpenAI

def main(message):
   # Set up the API key and initialize the model
    API = "KEY"
    model = ChatOpenAI(model="gpt-4o-2024-08-06", openai_api_key=API)
    chatbot = Chatbot(model)

    conversation = True
    while conversation:
        chatbot.verify_topics()
        human_query = message
        answer = chatbot.chat(human_query,API)
        return answer
