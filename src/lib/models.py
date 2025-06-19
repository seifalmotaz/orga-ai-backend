import os
from langchain_openai import ChatOpenAI

# Valid models
## Mistral
# mistralai/mistral-saba
## OpenAI
# openai/gpt-4.1-nano - (0.10$ in, 0.40$ out) (0.31 seconds latency)
## Meta
# meta-llama/llama-3.3-70b-instruct - (0.05$ in, 0.30$ out) (0.60 seconds latency)

# Create the model with tools bound
gpt4dot1 = ChatOpenAI(
    model="openai/gpt-4.1-nano",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
)
