from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

research_task = Task(
    description=(
        'Identify the relevant video content for the topic {topic} '
        'from the YouTube channel. Extract key points and insights.'
    ),
    expected_output=(
        'A comprehensive 3-paragraph report summarizing the relevant '
        'video content for the topic {topic} from the YT channel.'
    ),
    agent=blog_researcher,
    tools=[yt_tool],
)

write_task = Task(
    description=(
        'Write a well-structured blog post based on the research content '
        'extracted by the blog researcher for the topic {topic}.'
    ),
    expected_output=(
        'A well-structured and engaging blog post in markdown format '
        'about the topic {topic}, ready to publish.'
    ),
    agent=blog_writer,
    tools=[yt_tool],
    async_execution=False,
    output_file='new_blog_post.md',
)