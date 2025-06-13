import os
from langchain_openai import ChatOpenAI


# Create the model with tools bound
gpt4dot1 = ChatOpenAI(
    model="gpt-4.1",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)
