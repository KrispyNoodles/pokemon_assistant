from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Command
from langgraph.types import Send
from langchain.tools import tool

# importing the agents
from identifier_agent import pokemon_identifier_agent
from move_agent import pokemon_decision_move_agent

from langgraph.prebuilt import create_react_agent
from config import llm

# this creates tools for the Supervisor to handoff the conversation history and call the different tools

# the * means that all arguments needs to be passed as keyword arguments
def create_handoff_tool(*, agent_name: str, description: str | None = None):
    
    name = f"transfer_to_{agent_name}"
    description = description or f"Ask {agent_name} for help."

    # creating a handoff tool
    @tool(name, description=description)
    def handoff_tool(

        # This field is populated by the supervisor LLM. It provides a rephrased and focused version 
        # of the task based on the full conversation context, ensuring the next agent receives 
        # only the relevant instructions instead of the entire message history.
        
        task_description: Annotated[
            str,
            "Description of what the next agent should do, including all of the relevant context.",
        ],
        
        # InjectedState allows the LangGraph system to inject the state automatically
        state: Annotated[MessagesState, InjectedState],

        # the function expects to returns a command type, where command is a custom LangGraph class
    ) -> Command:
        
        # Adjusting the agent_inpiut instead of sending the whole conversation
        task_description_message = {"role": "user", "content": task_description}
        agent_input = {**state, "messages": [task_description_message]}

        return Command(
            # highlight-next-line
            goto=[Send(agent_name, agent_input)],
            graph=Command.PARENT,
        )

    return handoff_tool


# Handoffs tool for the Supervisor to handoff to the other agents
pokemon_identifier_agent_with_descript = create_handoff_tool(
    agent_name="pokemon_identifier_agent",
    description="Assign pokemon identification task to this identifier agent",
)

pokemon_decision_move_agent_with_descript = create_handoff_tool(
    agent_name="pokemon_decision_move_agent",
    description="Assign pokemon selection of moves task to this pokmeon decision agent.",
)

# creating the supervisor agent
supervisor_agent = create_react_agent(
    llm,
    tools=[
        pokemon_identifier_agent_with_descript,
        pokemon_decision_move_agent_with_descript,
    ],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- A **pokemon identifier agent**: Assign tasks related to identifying the Pokémon and determining its type.\n"
        "- A **pokemon decision move agent**: Assign tasks related to choosing effective moves against the Pokémon.\n\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    name="supervisor",
)


# Define the multi-agent supervisor graph
supervisor = (
    StateGraph(MessagesState)
    # NOTE: `destinations` is only needed for visualization and doesn't affect runtime behavior
    .add_node(supervisor_agent, destinations=("pokemon_identifier_agent", "pokemon_decision_move_agent", END))
    .add_node(pokemon_identifier_agent)
    .add_node(pokemon_decision_move_agent)
    .add_edge(START, "supervisor")

    # always return back to the supervisor
    .add_edge("pokemon_identifier_agent", "supervisor")
    .add_edge("pokemon_decision_move_agent", "supervisor")
    .compile()
)