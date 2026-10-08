from tools.travel_tools import search_flights
import time
from log import logger


def flight_agent(state):

    logger.info("Flight Agent started.")

    agent_start = time.perf_counter()

    tool_start = time.perf_counter()

    flights = search_flights.invoke({
        "destination": state["destination"]
    })
    tool_elapsed = time.perf_counter() - tool_start
    logger.info(f"Search Flights tool completed in {tool_elapsed:.3f}s")
    
    state["flight_options"] = flights

    logger.info(f"Flight options: {flights}")

    elapsed = time.perf_counter() - agent_start
    logger.info(f"Flight Agent completed in {elapsed:.3f}s")

    return state