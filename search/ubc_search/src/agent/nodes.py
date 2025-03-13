from dotenv import load_dotenv
_ = load_dotenv()

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from tavily import TavilyClient
import os
from agent.prompts import *

class AgentState(TypedDict):
    task: str
    content: List[str]
    revision_number: int
    max_revisions: int
    key_words: List[str]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class Queries(BaseModel):
    queries: List[str]

class KeyWords(BaseModel):
    list_of_key_words: List[str]

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def key_words_node(state: AgentState):
    new_key_words = model.with_structured_output(KeyWords).invoke([
        SystemMessage(content=KEY_WORDS_PROMPT),
        HumanMessage(content=state['task'])
    ])
    # key_words = state["key_words"] or []
    key_words = state.get("key_words", [])

    # for r in new_key_words["results"]:
    #     key_words.append(r)
    key_words.extend(new_key_words.list_of_key_words)

    return {**state, "key_words": key_words}

def importance_node(state: AgentState):
    description = f"This is the event description: \n {state['task']} \n\n"
    key_words_for_llm = f"These are the key words: {state['key_words']}"
    ranked_key_words = model.with_structured_output(KeyWords).invoke([
        SystemMessage(content=IMPORTANCE_PROMPT),
        HumanMessage(content=description + key_words_for_llm)
    ])
    return {**state, "key_words": ranked_key_words}

def enrichment_node(state: AgentState): # note: this node should be named 'enrichment'
    description = f"This is the event description: \n {state['task']} \n\n"
    key_words_for_llm = f"These are the key words: {state['key_words']}"
    enriched_key_words = model.with_structured_output(KeyWords).invoke([
        SystemMessage(content=ENRICHMENT_PROMPT),
        HumanMessage(content=description + key_words_for_llm)
    ])
    # key_words = state["key_words"] or []
    key_words = state.get("key_words", [])
    # for r in enriched_key_words.list_of_key_words:
    #     key_words.append(r)

    # Extract the actual keyword list
    enriched_list = enriched_key_words.list_of_key_words

    # Ensure state["key_words"] is a list
    if isinstance(state["key_words"], KeyWords):
        key_words = state["key_words"].list_of_key_words
    else:
        key_words = state["key_words"] or []

    # Combine both lists
    key_words.extend(enriched_list)

    # Increment revision_number
    revision_number = state.get("revision_number") + 1

    return {**state, "key_words": key_words, "revision_number": revision_number}

def query_node(state: AgentState):
    num_queries = 3
    
    keywords = state['key_words']
    if hasattr(keywords, "list_of_key_words"):
        keywords = ", ".join(keywords.list_of_key_words)

    queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=QUERY_PROMPT),
        HumanMessage(content=keywords)
    ])
    
    # content = state['content'] or []
    content = state.get('content', [])
    for q in queries.queries:
        response = tavily.search(query=q, max_results=2)
        # for r in response['results']:
        #     content.append(r['content'])
        for r in response.get("results", []):
            content.append(r.get("content", ""))
    return {**state, "content": content}

def should_continue_key_words(state):
    if state["revision_number"] >= state["max_revisions"]:
        return "query"
    return "enrichment"