import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv()

def get_ollama_llm(config: dict):
    return Ollama(
        model=config["model"],
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=config["temperature"]
    )