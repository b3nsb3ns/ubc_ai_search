

KEY_WORDS_PROMPT = """You are charged with finding sponsors and people that could attend an event \
such as a hackathon or workshop. Find key words within the user provided description of the event. \
"""

IMPORTANCE_PROMPT = """You are charged with ranking the importance of the given list of keywords in \
relation to the user provided description of the event, from most important to least important. """

ENRICHMENT_PROMPT = """You are charged with generating context words from the list of key words that \
could be used as additional key words for the user provided event. """

QUERY_PROMPT = """You are looking for relevant sponsorships and people for an event, based on the \
given list of keywords, ordered from most important to least important. \
Generate a list of search queries that will gather any relevant sponsorships and/or people. \
Only generate {num_queries} queries max."""
