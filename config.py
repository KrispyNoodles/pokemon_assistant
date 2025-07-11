from langchain_openai import AzureChatOpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")

API_KEY=config.get("API_KEY")
API_ENDPOINT=config.get("ENDPOINT")
API_MODEL=config.get("MODEL")

# Initialize the LLM
llm = AzureChatOpenAI(
                model=API_MODEL, 
                openai_api_version="2024-05-01-preview",
                temperature=0,
                api_key= API_KEY,
                azure_endpoint=API_ENDPOINT
                )
