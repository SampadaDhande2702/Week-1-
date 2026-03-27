import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_llm():
    config = load_config()
    provider = config["llm"]["provider"]

    if provider == "gemini":
        from llm.gemini_provider import get_gemini_llm
        return get_gemini_llm(config["llm"]["gemini"]), "gemini"
    elif provider == "groq":
        from llm.groq_provider import get_groq_llm
        return get_groq_llm(config["llm"]["groq"]), "groq"
    elif provider == "ollama":
        from llm.ollama_provider import get_ollama_llm
        return get_ollama_llm(config["llm"]["ollama"]), "ollama"
    else:
        raise ValueError(f"Unknown provider: {provider}")