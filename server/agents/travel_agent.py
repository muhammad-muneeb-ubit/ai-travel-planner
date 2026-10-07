from langchain_core.messages import SystemMessage, HumanMessage
from config.config import llm
from tools.travel_tools import (
    search_flights,
    search_hotels,
    search_activities
)


travel_tools = [
    search_flights,
    search_hotels,
    search_activities
]

travel_llm = llm.bind_tools(travel_tools)


SYSTEM_PROMPT = """
You are a travel research agent.

Use the available tools to search for:

- flights
- hotels
- activities

Use the tools when information is needed.

Do not invent travel data.

Once you have obtained the required information, stop calling tools.
"""


def travel_agent(state):

    print("Running travel_agent node...")

    messages = state["messages"]

    # First call
    if not messages:

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),

            HumanMessage(
                content=f"""
Plan research for this trip.

Destination: {state["destination"]}
Days: {state["days"]}
Month: {state["month"]}
Budget: {state["budget"]}
Hotel preference: {state["hotel_preference"]}
Interests: {state["interests"]}
"""
            )
        ]

    response = travel_llm.invoke(messages)

    print("Travel agent result:", response)

    return {
        "messages": [response]
    }