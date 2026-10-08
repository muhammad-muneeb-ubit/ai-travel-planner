from tools.travel_tools import search_activities
import time
from log import logger

def activity_agent(state):

    logger.info("Activity Agent started.")

    agent_start = time.perf_counter()

    tool_start = time.perf_counter()
    
    activities = search_activities.invoke({
        "destination": state["destination"],
        "interests": state["interests"]
    })
    tool_elapsed = time.perf_counter() - tool_start
    logger.info(f"Search Activities tool completed in {tool_elapsed:.3f}s")
    
    state["activity_options"] = activities

    logger.info(f"Activity options: {activities}")

    elapsed = time.perf_counter() - agent_start
    logger.info(f"Activity Agent completed in {elapsed:.3f}s")

    return state