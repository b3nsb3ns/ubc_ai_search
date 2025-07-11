

KEY_WORDS_PROMPT = """You are charged with finding sponsors and people that could attend an event \
such as a hackathon or workshop. Find key words within the user provided description of the event. 

Make sure location of the event and topic is included. 
For example, a hackathon in Vancouver, BC, Canada about diversity and equity in tech would include key words such as:
Vancouver BC, technology, coding, equity, diversity, etc. \
"""

IMPORTANCE_PROMPT = """You are charged with ranking the importance of the given list of keywords in \
relation to the user provided description of the event, from most important to least important. \

Location data is the most important, followed by the topic of the event. """

ENRICHMENT_PROMPT = """You are charged with generating context words from the list of key words that \
could be used as additional key words for the user provided event. """

LOCATION_PROMPT = """
You are an expert at geo-locating events based on clues in their descriptions. If the event mentions a school, venue, or well-known organization, infer the city or region from that information. Then, list nearby cities or regions that are reachable within a few hours by car or train. \

Examples: \

This example is for cmd-f in Vancouver, BC, Canada. \
cmd-f is a 24-hour hackathon located in Vancouver, BC, focused on addressing gender inequality in technology. Our main purpose is to create a safe and dedicated space for historically excluded genders to hack together. We’re trying to create access for people who have faced systemic barriers to inclusion on the basis of gender. We encourage participation from women, trans, non-binary, Two-Spirit and gender diverse people. Thus, cmd-f is only open to individuals who identify as a member of an underrepresented gender in technology. We’re aware that gender is not the only inequality in technology. We appreciate allyship and recognize it is important in the community. We invite allies to show their support by not hacking and instead contributing in other forms, such as volunteering or mentoring. Please make sure your participation in this event is aligned with the intentions of the event. We also ask all participants who attend to trust that everyone attending is meant to be here. \
Location(s): ['Vancouver, British Columbia, Canada', 'Burnaby, British Columbia, Canada', 'Richmond, British Columbia, Canada', 'Surrey, British Columbia, Canada', 'Victoria, British Columbia, Canada', 'Abbotsford, British Columbia, Canada', 'Seattle, Washington, USA'] \

This example is for ImmerseGT in Atlanta, Georgia, USA. \
ImmerseGT is a 36-hour long hackathon at Georgia Tech focusing mainly on working and developing XR (Extended Reality) applications and hardware. \
Location(s): ['Atlanta, Georgia, USA', 'Athens, Georgia, USA', 'Columbus, Georgia, USA', 'Chattanooga, Tennessee, USA'] \

This example is for JACHacks in Sainte-Anne-de-Bellevue, Quebec, Canada. \
JACHacks is John Abbott College’s annual hackathon, and this year, we will bring together 200 students for a weekend of innovation and collaboration. Developers and tech enthusiasts of all skill levels will have the chance to build impactful projects, learn new technologies, and connect with industry mentors. Join us for an incredible experience of coding, creativity, and community! Organized by John Abbott College’s CompSci Department. \
Location(s): ['Montreal, Quebec, Canada', 'Sainte-Anne-de-Bellevue, Quebec, Canada', 'Laval, Quebec, Canada', 'Longueuil, Quebec, Canada'] \

This example is for TreeHacks in Stanford, California, USA. \
TreeHacks is Stanford's premier hackathon. The country's brightest engineering students are flown to Stanford's campus to build solutions to the world's largest challenges for 36 hours straight. Join us for our 11th year to dream and build the future!
Tracks: Education, Healthcare, Sustainability, Web3, Autonomy, Edge AI \
Location(s): ['San Francisco Bay Area, California, USA', 'Stanford, California, USA', 'Palo Alto, California, USA', 'San Jose, California, USA', 'San Francisco, California, USA', 'Oakland, California, USA'] \

Instructions: \
- Output a **Python-style list of strings** representing locations relevant to the event. \
- Start with the **metropolitan region** if applicable. \
- Include the specific town or venue location (e.g., university or neighborhood). \
- Then add **nearby cities or regions** reachable within a few hours by car or train. \
- If no location is mentioned directly, **infer the main location from indirect clues**, such as: \
    - University name (e.g., "MIT" → Cambridge, Massachusetts) \
    - Known organizations or campuses \
    - References to landmarks, regional traits, or event names \
- If a city or province or state is directly mentioned (e.g., "Vancouver, BC"), treat that as authoritative and correct. \
- Do not omit inferred locations — use your general knowledge. \

Event Description: \
{event_description}

"""

INDUSTRY_PROMPT = """
You are charged with determining the industry of an event, given its description.

For example, the following event's industry is ["technology", "software"]:  
cmd-f is a 24-hour hackathon located in Vancouver, BC, focused on addressing gender inequality in technology. Our main purpose is to create a safe and dedicated space for historically excluded genders to hack together. We’re trying to create access for people who have faced systemic barriers to inclusion on the basis of gender. We encourage participation from women, trans, non-binary, Two-Spirit and gender diverse people. Thus, cmd-f is only open to individuals who identify as a member of an underrepresented gender in technology.  
We’re aware that gender is not the only inequality in technology. We appreciate allyship and recognize it is important in the community. We invite allies to show their support by not hacking and instead contributing in other forms, such as volunteering or mentoring. Please make sure your participation in this event is aligned with the intentions of the event. We also ask all participants who attend to trust that everyone attending is meant to be here.

For another example, the following event's industry is ["computer graphics", "technology", "software"]:  
Every day we find ourselves more deeply immersed in the technology we create. Where computers and data once existed apart from us, they are now interwoven in our lives, powered by the drive of human expression, creativity, and need. The relationship between humanity and technology transforms our world, pushing the boundaries of what’s possible. As a community of excellence in technical skill and artistry, we at SIGGRAPH can lead this transformation by shaping a future that unites the physical and digital worlds for the better.  
At SIGGRAPH 2025, we stand at the forefront of this progress, embracing it, sharing it, and creating it. We are not just passive participants — we are active co-creators of the future. From the art we bring to life, to the stories we tell across media and unprecedented levels of immersion transforming how we experience the world, SIGGRAPH 2025 is a celebration of our collective drive to connect, comprehend, and express the essence of human experience.  
The human story has always fueled technological breakthroughs, and together, we are writing the next chapter in a legacy that spans over five decades. For 52 years, SIGGRAPH has nurtured the brightest minds and boldest ideas in computer graphics and interactive techniques. This year, we return to Vancouver, whose modern, urban landscape meets an inspiring nature setting, reminding us that technology, at its best, complements and enhances our world.  
We are thrilled to welcome you to SIGGRAPH 2025, where you will discover and embrace how human ingenuity and technological marvels unite to shape our trajectory toward a better future.  
Ginger Alford, SIGGRAPH 2025 Conference Chair  
Play an active role in shaping our collective technological future. Submit your most exciting, unconventional, or experiential innovation to present in front of our esteemed community. Get involved by giving back your time through one of our many volunteer opportunities. Discover how human creativity and next-level technology improve our collective future by joining us for SIGGRAPH 2025 in Vancouver.

For another example, the following event's industry is ['wine', 'food', 'hospitality']: 
VanWineFest is Canada’s premier wine show and widely considered to be the best wine event in North America. 
With ~18,000 admissions and at 46 years of age, it is one of the biggest and oldest wine events in the world. 
Its slogan is “The Wine World is Here”. It has been voted the “#1 Food, Wine & Hospitality Event in Canada” for eight years running by New York’s BizBash. 
Trade Days, which runs February 26-28 in 2025, comprises 12 of the festival’s 43 events.

For another example, the following event's industry is ['Arts', 'Books', 'Literature', 'Theatre', 'Performing Arts']: 
The UBC Players Club and UBC Book Club proudly present the second edition of our End of Year Gala. 
We can't wait to see the magic unfold in our Secret Garden.
A gala for lovers of all things artsy, our End of Year Gala is an evening for indulging in food, drink and frivolity. 
A ticket includes a fully catered dinner, automatic entry into a raffle for several bookish and theatrical delights, and a night full of fun.

Instructions:
- Return a list of industries that best fit the event.
- Include the most **broad and meaningful industry label** possible. (e.g., “technology” is broader than “software”)
- Use only actual **industries or occupational domains**, such as: technology, software, healthcare, finance, engineering, education, business management, etc.
- Do **not** include topics, event types, or values (e.g., “hackathon”, “gender equality”, “sustainability”) unless they are also recognized as industries.

Determine the industries of this event:
{event_description}

"""


QUERY_PROMPT = """You are looking for relevant sponsorships for an event, based on the \
given location data and the industries the event caters to. \
Generate a list of search queries that will gather any relevant sponsorships and/or people. \

For example, a hackathon in Vancouver, BC, Canada about diversity and equity in tech would have queries like the following: 
Tech companies with offices in Vancouver BC. \
Tech firms in Vancouver BC. \
Global tech companies with Vancouver BC offices. \

Only generate {num_queries} queries max. \

Here is the given data: \
Location data: {locations} \

Industry: {industries} \
"""

EXTRACT_PROMPT = """You are looking for relevant sponsorships for an event. \
Based on the given search results, generate a list of companies mentioned in the search results. \

For example, the search result: \
Alongside these next level valuations, other BC-based industry leaders have emerged: AbCellera in the life \
science space, BroadbandTV (BBTV) in online content distribution, Boast.ai in R&D tax credit automation, and \
Vancouver's Dapper Labs, which almost single-handedly lit the fuse on the global NFT market and is now one of \
the most valuable... \

would return ['AbCellera', 'BroadbandTV', 'Boast.ai', Dapper Labs'] \

Here are the search results to extract a list of companies from: \
{companies}
"""