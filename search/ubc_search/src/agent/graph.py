"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from typing import Any, Dict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from src.agent.configuration import Configuration
from src.agent.state import State

from langgraph.checkpoint.memory import MemorySaver
from agent.nodes import *

memory = MemorySaver()

keyword_graph = StateGraph(AgentState)

keyword_graph.add_node("keywords", key_words_node)
keyword_graph.add_node("importance", importance_node)
keyword_graph.add_node("enrichment", enrichment_node)
keyword_graph.add_node("query", query_node)

keyword_graph.set_entry_point("keywords")

keyword_graph.add_conditional_edges(
    "importance", 
    should_continue_key_words, 
    {"query": "query", "enrichment": "enrichment"}
)

keyword_graph.add_edge("keywords", "importance")
keyword_graph.add_edge("enrichment", "importance")

graph = keyword_graph.compile(checkpointer=memory)
# Compile the workflow into an executable graph
#graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
