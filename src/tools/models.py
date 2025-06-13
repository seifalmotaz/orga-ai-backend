import os
from langchain_openai import ChatOpenAI


# Create the model with tools bound
gpt_4o_mini = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)
