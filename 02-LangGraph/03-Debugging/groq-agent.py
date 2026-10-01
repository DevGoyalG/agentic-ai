# ============================================================
# Building a Groq Tool-Calling Agent using LangGraph Studio
# ============================================================

from typing import Annotated
from typing_extensions import TypedDict

from langchain_groq import ChatGroq

from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Set the LangSmith API key for tracing and monitoring
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# Define the Graph State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Create a Groq chat model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# Create a Basic LangGraph Agent
def make_default_graph():

    graph_workflow = StateGraph(State)

    def call_model(state):
        return {
            "messages": [
                model.invoke(state["messages"])
            ]
        }

    graph_workflow.add_node("agent", call_model)

    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_edge("agent", END)

    agent = graph_workflow.compile()

    return agent


# Create a Tool-Calling LangGraph Agent
def make_alternative_graph():
    """Make a tool-calling agent"""

    @tool
    def add(a: float, b: float):
        """Adds two numbers."""
        return a + b

    # Tool node
    tool_node = ToolNode([add])

    # Bind tools to Groq model
    model_with_tools = model.bind_tools([add])

    def call_model(state):
        return {
            "messages": [
                model_with_tools.invoke(state["messages"])
            ]
        }

    def should_continue(state: State):

        if state["messages"][-1].tool_calls:
            return "tools"
        else:
            return END

    # Create graph
    graph_workflow = StateGraph(State)

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_node("tools", tool_node)

    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_edge("tools", "agent")

    graph_workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    agent = graph_workflow.compile()

    return agent


# Create Agent
agent = make_alternative_graph()


# ============================================================
# Run LangGraph Studio
# ============================================================

# 1. Open Command Prompt

# 2. Activate the virtual environment
# Example:
# D:\agentic-ai\02-LangGraph\03-Debugging>conda activate venv/

# 3. Install LangGraph CLI with in-memory support
# pip install -U "langgraph-cli[inmem]"

# 4. Move to the project folder
# cd 02-Debugging

# 5. Start LangGraph development server
# langgraph dev