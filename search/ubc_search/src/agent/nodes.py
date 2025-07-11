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

# class AgentState(TypedDict):
#     task: str
#     content: List[str]
#     search_result: SearchResult
#     revision_number: int
#     max_revisions: int
#     key_words: List[str]

class AgentState(TypedDict):
    task: str
    locations: List[str]
    industries: List[str]
    queries: List[str]
    content: List[str]
    companies: List[str]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class Queries(BaseModel):
    list_queries: List[str]

class Locations(BaseModel):
    list_locations: List[str]

class Industries(BaseModel):
    list_industries: List[str]

class Companies(BaseModel):
    list_companies: List[str]

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def init_state(state: AgentState):
    return {
        **state, 
        "task": state.get("task", ""),
        "content": [],
        "locations": [],
        "industries": [],
        "queries": [],
        "companies": []
    }

def location_node(state: AgentState):
    task = state.get('task', '')
    if not isinstance(task, str):
        task = str(task)  # Convert to string as a fallback

    new_locations = model.with_structured_output(Locations).invoke([
        SystemMessage(content=LOCATION_PROMPT.format(event_description=task)),
        HumanMessage(content=task)
    ])

    locations = state.get("locations", [])
    if not isinstance(locations, list):
        locations = [locations]

    list_locations = getattr(new_locations, 'list_locations', [])
    if isinstance(list_locations, list):
        locations.extend(list_locations)
    elif isinstance(list_locations, str):
        locations.append(list_locations)

    return {**state, "locations": locations}

def industry_node(state: AgentState):
    task = state.get('task', '')
    if not isinstance(task, str):
        task = str(task)  # Convert to string as a fallback

    new_industries = model.with_structured_output(Industries).invoke([
        SystemMessage(content=INDUSTRY_PROMPT.format(event_description=task)),
        HumanMessage(content=task)
    ])

    industries = state.get("industries", [])
    if not isinstance(industries, list):
        industries = [industries]

    list_industries = getattr(new_industries, 'list_industries', [])
    if isinstance(list_industries, list):
        industries.extend(list_industries)
    elif isinstance(list_industries, str):
        industries.append(list_industries)

    return {**state, "industries": industries}

def query_node(state: AgentState):
    num_queries = 10

    task = state.get('task', '')
    if not isinstance(task, str):
        task = str(task)  # Convert to string as a fallback

    locations = state["locations"]
    industries = state["industries"]

    new_queries = model.with_structured_output(Queries).invoke([
        SystemMessage(content=QUERY_PROMPT.format(
            num_queries=num_queries, locations=locations, industries=industries))
    ])

    queries = state.get("queries", [])
    if not isinstance(queries, list):
        queries = [queries]

    list_queries = getattr(new_queries, 'list_queries', [])
    if isinstance(list_queries, list):
        queries.extend(list_queries)
    elif isinstance(list_queries, str):
        queries.append(list_queries)
    
    return {**state, "queries": queries}

def tavily_node(state: AgentState):

    task = state.get('task', '')
    if not isinstance(task, str):
        task = str(task)  # Convert to string as a fallback

    # content = state['content'] or []
    content = state.get('content', [])
    if not isinstance(content, list):
        content = [content]  # Convert non-list content to a list

    queries = state.get("queries", [])
    if not isinstance(queries, list):
        queries = [queries]

    for q in queries:
        response = tavily.search(query=q, max_results=2)
        for r in response['results']:
            content.append(r['content'])

    return {**state, "content": content}

def extraction_node(state: AgentState):

    task = state.get('task', '')
    if not isinstance(task, str):
        task = str(task)  # Convert to string as a fallback

    content = state.get('content', [])
    if not isinstance(content, list):
        content = [content]

    new_companies = model.with_structured_output(Companies).invoke([
        SystemMessage(content=EXTRACT_PROMPT.format(companies=content))
    ])

    companies = state.get("companies", [])
    if not isinstance(companies, list):
        companies = [companies]

    list_companies = getattr(new_companies, 'list_companies', [])
    if isinstance(list_companies, list):
        companies.extend(list_companies)
    elif isinstance(list_companies, str):
        companies.append(list_companies)
    
    return {**state, "companies": companies}