import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import yt_tool

load_dotenv()

# ✅ Using crewai's native LLM class with Groq — no langchain needed
llm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0.7,
)

blog_researcher = Agent(
    role='Blog Researcher for YouTube Videos',
    goal='Get the relevant video content for the topic {topic} from the YT channel',
    verbose=True,
    memory=True,
    backstory=(
        "Expert in understanding videos in AI and data science, "
        "and extracting relevant information for blog content creation."
    ),
    tools=[yt_tool],
    llm=llm,
    allow_delegation=True,
)

blog_writer = Agent(
    role='Blog Writer for YouTube Videos',
    goal='Write a blog post based on the content extracted by the blog researcher for the topic {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Skilled in crafting engaging and informative blog posts based on video content, "
        "with a focus on AI and data science topics."
    ),
    tools=[yt_tool],
    llm=llm,
    allow_delegation=False,
)