# loading csv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.retrievers import TFIDFRetriever
from langchain.tools.retriever import create_retriever_tool

# pokedex taken from "https://www.kaggle.com/datasets/brdata/complete-pokemon-dataset-gen-iiv"
loader = CSVLoader(file_path='./pokedex_database/Pokedex_Cleaned.csv', encoding="ISO-8859-1")
documents = loader.load()
retriever = TFIDFRetriever.from_documents(documents, k=2)

retriever_pokemon_tool = create_retriever_tool(
    retriever,
    name="pokemon_type_lookup_tool",
    description="Use this tool to find information about the type of the Pokémon from its name in a database, not file path"
)

# Pokemon Viewer
import base64
from config import llm
from langchain_core.tools import tool

# the tool takes in a pdf_path in a string format and it returns the function back with an int
@tool(return_direct=True)
def pokemon_identifier(image_path: str) -> str:
    """This tool views the picture from an image path and returns only the name of the pokemon."""

    system_prompt = "Return only the name of the Pokemon"

    try:
        with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

    except Exception as e:
        return f"Error is {e}, invalid file or no file uploaded"

    message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt,
                },
                {
                    "type": "image",
                    "source_type": "base64",
                    "data": image_data,
                    "mime_type": "image/jpeg",
                },
            ],
        }

    # using the name of pokemon to query
    response = llm.invoke([message])
    name_of_pokemon = response.content

    # querying in database
    result = retriever_pokemon_tool.invoke(name_of_pokemon)
        
    return result

from langgraph.prebuilt import create_react_agent

pokemon_identifier_agent = create_react_agent(
    llm,
    tools=[pokemon_identifier, retriever_pokemon_tool],
    prompt=(
        "You are a Pokemon Identifier Agent. Your job is to identify a Pokemon using either text or an image input.\n\n"
        "When given an image path, analyze the image file to determine the name of the pokemon."
        "Use the `pokemon_identifier` tool to analyze the image, or then use `retriever_pokemon_tool` to query a text.\n\n"

        "INSTRUCTIONS:\n"
        "- Only perform Pokémon identification tasks.\n"
        "- Use the image analysis tool instead of assuming from filenames.\n"
        "- After you're done, respond only with your result.\n"
    ),
    name="pokemon_identifier_agent",
)