import os
from dotenv import load_dotenv

load_dotenv()

# Required to satisfy internal crewai_tools validation
os.environ["OPENAI_API_KEY"] = "dummy-key"

from crewai_tools import YoutubeChannelSearchTool

yt_tool = YoutubeChannelSearchTool(
    youtube_channel_handle='https://www.youtube.com/@krishnaik06',
    config=dict(
        llm=dict(
            provider="groq",
            config=dict(
                model="llama3-8b-8192",
                api_key=os.environ.get("GROQ_API_KEY"),
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="sentence-transformers/all-MiniLM-L6-v2",
            ),
        ),
    )
)