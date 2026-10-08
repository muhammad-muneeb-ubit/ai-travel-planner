from tools.travel_tools import search_hotels
import time
from log import logger


def hotel_agent(state):

    logger.info("Hotel Agent started.")

    agent_start = time.perf_counter()

    tool_start = time.perf_counter()

    minimum_rating = int(
        state["hotel_preference"].split("-")[0]
    )

    hotels = search_hotels.invoke({
        "destination": state["destination"],
        "minimum_rating": minimum_rating
    })
    tool_elapsed = time.perf_counter() - tool_start
    logger.info(f"Search Hotels tool completed in {tool_elapsed:.3f}s")
    
    state["hotel_options"] = hotels

    logger.info(f"Hotel options: {hotels}")

    elapsed = time.perf_counter() - agent_start
    logger.info(f"Hotel Agent completed in {elapsed:.3f}s") 

    return state