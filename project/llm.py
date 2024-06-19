from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.prompts import PromptTemplate
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
import os

os.environ["OPENAI_API_KEY"] = "OPENAI API KEY"

messages_chat = []
messages_chat_data = []


global llm
global p_agent
global chain

# def load_embedding_model(model_path, normalize_embedding=True):
#     return OllamaEmbeddings(model=model_path)

template = "You are an AI.\nDon't repeat answers from your History.\nEntities: {entities}\nHistory: {history}\nAnswer the following question:\nHuman: {input}\nPlease provide a relevant response.\nAI:"
    
def get_response(query, chain):
    return chain.invoke(input=query)["response"]

def input_message(inp):
    global chain
    return get_response(inp, chain)

def add_to_messages_and_gen(inp):
    ai = input_message(inp)
    print(ai)
    messages_chat.append({"title" : "User", "text" : inp})
    messages_chat.append({"title" : "AI", "text" : ai})



def input_message_data(inp):
    global p_agent
    return p_agent.run(inp)

def add_to_messages_and_gen_data(inp):
    ai = input_message_data(inp)
    print(ai)
    messages_chat_data.append({"title" : "User", "text" : inp})
    messages_chat_data.append({"title" : "AI", "text" : ai})

def setup_chat():
    global chain,llm, p_agent
    drivers = pd.read_csv("./data/drivers.csv")
    parcels = pd.read_csv("./data/parcels.csv")
    users = pd.read_csv("./data/user_activity.csv")
    delivery = pd.read_csv("./data/parcel_delivery.csv")

    llm = OpenAI()
    p_agent = create_pandas_dataframe_agent(llm=llm,df=[drivers, parcels, users, delivery],verbose=True)

    PROMPT = PromptTemplate(input_variables=['entities', 'history', 'input'], template=template)
    chain = ConversationChain(llm=llm, memory=ConversationEntityMemory(llm=llm), prompt=PROMPT, verbose=False)
