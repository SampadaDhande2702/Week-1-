import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_groq_llm(config: dict):
    return ChatGroq(
        model=config["model"],
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=config["temperature"],
        max_tokens=config["max_tokens"]
    )