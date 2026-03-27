import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

_langfuse_instance = None

def get_langfuse():
    global _langfuse_instance
    if _langfuse_instance is None:
        _langfuse_instance = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        )
    return _langfuse_instance

def create_trace(name: str, user_id: str, input_data: dict):
    lf = get_langfuse()
    trace = lf.trace(
        name=name,
        user_id=user_id,
        input=input_data,
        tags=["customer-support", "multi-agent"]
    )
    return trace

def flush():
    lf = get_langfuse()
    lf.flush()