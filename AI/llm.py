from dotenv import load_dotenv
import os 
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():

    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )