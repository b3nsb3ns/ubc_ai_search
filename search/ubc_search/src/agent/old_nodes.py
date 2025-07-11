

# class KeyWords(BaseModel):
#     list_of_key_words: List[str]

# def key_words_node(state: AgentState):
#     task = state.get('task', '')
#     if not isinstance(task, str):
#         task = str(task)  # Convert to string as a fallback

#     new_key_words = model.with_structured_output(KeyWords).invoke([
#         SystemMessage(content=KEY_WORDS_PROMPT),
#         HumanMessage(content=task)
#     ])
#     # key_words = state["key_words"] or []
#     # key_words = state.get("key_words", [])

#     # for r in new_key_words["results"]:
#     #     key_words.append(r)
#     # key_words.extend(new_key_words.list_of_key_words)

#     key_words = state.get("key_words", [])
#     if not isinstance(key_words, list):
#         key_words = [key_words]

#     list_of_key_words = getattr(new_key_words, 'list_of_key_words', [])
#     if isinstance(list_of_key_words, list):
#         key_words.extend(list_of_key_words)
#     elif isinstance(list_of_key_words, str):
#         key_words.append(list_of_key_words)

#     return {**state, "key_words": key_words, "task": task}

# def importance_node(state: AgentState):
#     task = state.get('task', '')
#     if not isinstance(task, str):
#         task = str(task)  # Convert to string as a fallback

#     description = f"This is the event description: \n {state['task']} \n\n"
#     key_words_for_llm = f"These are the key words: {state['key_words']}"
#     ranked_key_words = model.with_structured_output(KeyWords).invoke([
#         SystemMessage(content=IMPORTANCE_PROMPT),
#         HumanMessage(content=description + key_words_for_llm)
#     ])
#     return {**state, "key_words": ranked_key_words, "task": task}

# def enrichment_node(state: AgentState): # note: this node should be named 'enrichment'
#     task = state.get('task', '')
#     if not isinstance(task, str):
#         task = str(task)  # Convert to string as a fallback

#     description = f"This is the event description: \n {state['task']} \n\n"
#     key_words_for_llm = f"These are the key words: {state['key_words']}"
#     enriched_key_words = model.with_structured_output(KeyWords).invoke([
#         SystemMessage(content=ENRICHMENT_PROMPT),
#         HumanMessage(content=description + key_words_for_llm)
#     ])
#     # key_words = state["key_words"] or []
#     key_words = state.get("key_words", [])
#     # for r in enriched_key_words.list_of_key_words:
#     #     key_words.append(r)

#     # Extract the actual keyword list
#     enriched_list = enriched_key_words.list_of_key_words

#     # Ensure state["key_words"] is a list
#     if isinstance(state["key_words"], KeyWords):
#         key_words = state["key_words"].list_of_key_words
#     else:
#         key_words = state["key_words"] or []

#     # Combine both lists
#     key_words.extend(enriched_list)

#     # Increment revision_number
#     revision_number = state.get("revision_number") + 1
#     # revision_number = state["revision_number"] + 1

#     return {**state, "key_words": key_words, "revision_number": revision_number, "task": task}

# def should_continue_key_words(state):
#     if state["revision_number"] >= state["max_revisions"]:
#         return "query"
#     return "enrichment"

# def should_continue_queries(state):
#     if state["revision_number"] >= state["max_revisions"]:
#         return "extraction"
#     return "query"