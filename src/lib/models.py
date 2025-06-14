import os
from langchain_openai import ChatOpenAI


# Create the model with tools bound
gpt4dot1 = ChatOpenAI(
    model="openai/gpt-4.1-nano",
    temperature=1,
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
)
