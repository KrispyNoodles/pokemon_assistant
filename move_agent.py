
# loading csv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.retrievers import TFIDFRetriever
from langchain.tools.retriever import create_retriever_tool
from config import llm
from langgraph.prebuilt import create_react_agent

# pokemon moves dataset taken from "https://www.kaggle.com/datasets/thiagoamancio/full-pokemons-and-moves-datasets"
loader = CSVLoader(file_path='./pokedex_database/metadata_pokemon_moves.csv')
documents = loader.load()
retriever = TFIDFRetriever.from_documents(documents, k=2)

retriever_moves_tool = create_retriever_tool(
    retriever,
    name="pokemon_moves_lookup_tool",
    description="Use this tool to find information all Pokémon moves and their type from a CSV file."
)

effectiveness_chart = {
    "normal": "fighting",
    "fire": "water",
    "water": "electric",
    "electric": "ground",
    "grass": "fire",
    "ice": "fire",
    "fighting": "flying",
    "poison": "psychic",
    "ground": "water",
    "flying": "electric",
    "psychic": "bug",
    "bug": "fire",
    "rock": "water",
    "ghost": "ghost",
    "dragon": "fairy",
    "dark": "fairy",
    "steel": "fire",
    "fairy": "poison"
}

pokemon_decision_move_agent = create_react_agent(
    llm,
    tools=[retriever_moves_tool],
    prompt=(
        "You are a Pokemon Move Decision Agent, where you can best which move to make against the oponnent's Pokemon.\n\n"

        "INSTRUCTIONS:\n"
        "- Assist ONLY with pokemon move related task\n"
        "- After you're done with your tasks, determine which moves are most effective\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."

        f"""
        Effectiveness Chart

        Use the following chart to determine the best move type against an opponent's Pokémon type.
        Each entry maps an opponent's type to the type that is super effective against it.

        {effectiveness_chart}

        For example:
        "fire": "water" — If the opponent is a Fire type, a Water-type move will be most effective.
        
        For example "fire": "water", it means that opponent is 'fire and the effective move against it is 'water'.
        Use this chart when choosing moves:
        If the opponent’s type is not listed, default to a "normal" type move. """
    ),
    name="pokemon_decision_move_agent",
)


