import os
os.environ['USER_AGENT'] = 'myagent'
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from utils.load_json import load_json
from agents.profile_manager import ProfileManager
import chromadb
from chromadb import Client



class WebsiteExpert:
    def __init__(self,model,topic,topics):
        self.model = model
        self.topic = topic
        self.topics = topics
        self.data_urls = load_json("data/urls.json")
        self.profile_manager = ProfileManager(model)
        self.client = Client()
        print("Website Expert Initialized")

    def find_category_urls(self):
        for t in self.data_urls:
            if t['categoria'] == self.topic:
                print("Categoría encontrada", t['categoria'])
                return t['urls']
        print('No se encontraron URLS del tema.')
        return None  

    def answer(self,human_query,api):
        chromadb.api.client.SharedSystemClient.clear_system_cache()
        urls = self.find_category_urls()
        all_documents = []
        if urls:
        # Iteramos sobre cada URL y cargamos los datos
            for url in urls:
                loader = WebBaseLoader(url)
                data = loader.load()
                all_documents.extend(data)  # Añadimos los documentos cargados a la lista

            # Dividimos todos los documentos en trozos
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
            all_splits = text_splitter.split_documents(all_documents)


            # Creamos el vectorstore a partir de los documentos divididos
            vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(api_key=api),client=Client())

            # k is the number of chunks to retrieve
            retriever = vectorstore.as_retriever(k=4)

            docs = retriever.invoke(human_query)

            SYSTEM_TEMPLATE = """
Contesta la consulta del usuario basada en el contexto proporcionado.
Si la pregunta no tiene que ver con uno de estos temas {topics}, contesta "No sé".
Puede que el usuario quiera recomendaciones en base al contexto proporcionado. Para dar una respuesta acertada en esos casos, también te proporcionaré la información del usuario:
{client_info}

<contexto proporcionado>
{context}
</contexto proporcionado>
            """

            question_answering_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        SYSTEM_TEMPLATE,
                    ),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )

            document_chain = create_stuff_documents_chain(self.model, question_answering_prompt)

            answer = document_chain.invoke(
                {
                    "context": docs,
                    "topics": self.topics,
                    "client_info": self.profile_manager.client_info,
                    "messages": [
                        HumanMessage(content=human_query)
                    ],
                }
            )
            return answer

