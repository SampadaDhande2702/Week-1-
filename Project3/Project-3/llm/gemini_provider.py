import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_gemini_llm(config: dict):
    return ChatGoogleGenerativeAI(
        model=config["model"],
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=config["temperature"],
        max_output_tokens=config["max_tokens"],
        convert_system_message_to_human=True
    )