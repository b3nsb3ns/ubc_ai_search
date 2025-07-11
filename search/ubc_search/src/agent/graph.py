"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from typing import Any, Dict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START

from src.agent.configuration import Configuration
from src.agent.state import State


from langgraph.checkpoint.memory import MemorySaver
from agent.nodes import *

memory = MemorySaver()

keyword_graph = StateGraph(AgentState)

keyword_graph.add_node("init", init_state)
keyword_graph.add_node("location", location_node)
keyword_graph.add_node("industry", industry_node)
# keyword_graph.add_node("keywords", key_words_node)
# keyword_graph.add_node("importance", importance_node)
# keyword_graph.add_node("enrichment", enrichment_node)
keyword_graph.add_node("query", query_node)
keyword_graph.add_node("tavily", tavily_node)
keyword_graph.add_node("extract", extraction_node)

keyword_graph.set_entry_point("init")

# keyword_graph.add_conditional_edges(
#     "importance", 
#     should_continue_key_words, 
#     {"query": "query", "enrichment": "enrichment"}
# )

# keyword_graph.add_edge("init", "keywords")
# keyword_graph.add_edge("keywords", "importance")
# keyword_graph.add_edge("enrichment", "importance")

keyword_graph.add_edge(START, "init")
keyword_graph.add_edge("init", "location")
keyword_graph.add_edge("location", "industry")
keyword_graph.add_edge("industry", "query")
keyword_graph.add_edge("query", "tavily")
keyword_graph.add_edge("tavily", "extract")

graph = keyword_graph.compile(checkpointer=memory)
# Compile the workflow into an executable graph
#graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
