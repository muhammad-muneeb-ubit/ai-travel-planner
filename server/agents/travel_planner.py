# from config.config import llm
# from agents.models import TravelSelection, TravelPlan
# from graphs.state import TravelState

# planner_llm = llm.with_structured_output(TravelPlan)

# def travel_planner(state):

#     print("Running travel_planner node...")

#     prompt = f"""
# You are a travel planner.

# Select the best trip options from the available data.

# Destination:
# {state["destination"]}

# Days:
# {state["days"]}

# Budget:
# {state["budget"]}

# Hotel preference:
# {state["hotel_preference"]}

# Interests:
# {state["interests"]}

# Available flights:
# {state["flight_options"]}

# Available hotels:
# {state["hotel_options"]}

# Available activities:
# {state["activity_options"]}

# Rules:

# 1. Select only IDs from the provided options.
# 2. Do not invent options.
# 3. Prefer cheaper options when appropriate.
# 4. Match the user's hotel preference.
# 5. Select activities matching the user's interests.
# 6. Try to stay within the budget.
# """

#     result = planner_llm.invoke(prompt)

#     print("Planner result:", result)

#     selected_flight = next(
#         (
#             flight
#             for flight in state["flight_options"]
#             if flight["id"] == result.flight_id
#         ),
#         {}
#     )

#     selected_hotel = next(
#         (
#             hotel
#             for hotel in state["hotel_options"]
#             if hotel["id"] == result.hotel_id
#         ),
#         {}
#     )

#     selected_activities = [
#         activity
#         for activity in state["activity_options"]
#         if activity["id"] in result.activity_ids
#     ]

#     state["selected_flight"] = selected_flight
#     state["selected_hotel"] = selected_hotel
#     state["selected_activities"] = selected_activities

#     print("Selected flight:", selected_flight)
#     print("Selected hotel:", selected_hotel)
#     print("Selected activities:", selected_activities)
#     print("Reasoning:", result.reasoning)

#     return state


# def replan_with_llm(state: TravelState) -> TravelState:

#     print("Running replan_with_llm node...")

#     state["replan_attempts"] += 1

#     prompt = f"""
# You are a travel planner responsible for fixing an over-budget trip.

# Destination:
# {state["destination"]}

# Days:
# {state["days"]}

# Month:
# {state["month"]}

# Maximum budget:
# {state["budget"]}

# Current total:
# ${state["total_cost"]}

# Current flight:
# {state["selected_flight"]}

# Current hotel:
# {state["selected_hotel"]}

# Current activities:
# {state["selected_activities"]}

# Available flights:
# {state["flight_options"]}

# Available hotels:
# {state["hotel_options"]}

# Available activities:
# {state["activity_options"]}

# Interests:
# {state["interests"]}

# Rules:

# 1. Stay within the budget if possible.
# 2. Select only IDs from available options.
# 3. Do not invent anything.
# 4. Prefer cheaper flight and hotel options.
# 5. Keep important activities when possible.
# 6. Remove expensive activities before removing all activities.
# 7. Return the cheapest reasonable combination.
# """

#     result = planner_llm.invoke(prompt)

#     print("Replan result:", result)

#     selected_flight = next(
#         (
#             flight
#             for flight in state["flight_options"]
#             if flight["id"] == result.flight_id
#         ),
#         {}
#     )

#     selected_hotel = next(
#         (
#             hotel
#             for hotel in state["hotel_options"]
#             if hotel["id"] == result.hotel_id
#         ),
#         {}
#     )

#     selected_activities = [
#         activity
#         for activity in state["activity_options"]
#         if activity["id"] in result.activity_ids
#     ]

#     state["selected_flight"] = selected_flight
#     state["selected_hotel"] = selected_hotel
#     state["selected_activities"] = selected_activities

#     print("Replan reasoning:", result.reasoning)
#     print("Replan attempt:", state["replan_attempts"])

#     return state



from config.config import llm
from agents.models import TravelSelection, TravelPlan
from graphs.state import TravelState
import time
from log import logger


planner_llm = llm.with_structured_output(TravelPlan)


def travel_planner(state: TravelState):

    logger.info("Travel Planner started.")
    node_start = time.perf_counter()

    prompt = f"""
You are a travel planner.

Select the best trip options from the available data.

Destination:
{state["destination"]}

Days:
{state["days"]}

Budget:
{state["budget"]}

Hotel preference:
{state["hotel_preference"]}

Interests:
{state["interests"]}

Available flights:
{state["flight_options"]}

Available hotels:
{state["hotel_options"]}

Available activities:
{state["activity_options"]}

Rules:

1. Select only IDs from the provided options.
2. Do not invent options.
3. Prefer cheaper options when appropriate.
4. Match the user's hotel preference.
5. Select activities matching the user's interests.
6. Try to stay within the budget.
"""

    logger.info("Travel Planner LLM started.")
    llm_start = time.perf_counter()

    result = planner_llm.invoke(prompt)

    llm_elapsed = time.perf_counter() - llm_start
    logger.info(
        f"Travel Planner LLM completed in {llm_elapsed:.3f}s"
    )

    selected_flight = next(
        (
            flight
            for flight in state["flight_options"]
            if flight["id"] == result.flight_id
        ),
        {}
    )

    selected_hotel = next(
        (
            hotel
            for hotel in state["hotel_options"]
            if hotel["id"] == result.hotel_id
        ),
        {}
    )

    selected_activities = [
        activity
        for activity in state["activity_options"]
        if activity["id"] in result.activity_ids
    ]

    state["selected_flight"] = selected_flight
    state["selected_hotel"] = selected_hotel
    state["selected_activities"] = selected_activities

    logger.info(
        f"Planner selected | "
        f"flight={result.flight_id} | "
        f"hotel={result.hotel_id} | "
        f"activities={result.activity_ids}"
    )

    logger.info(f"Planner reasoning: {result.reasoning}")

    elapsed = time.perf_counter() - node_start
    logger.info(
        f"Travel Planner completed in {elapsed:.3f}s"
    )

    return state


def replan_with_llm(state: TravelState) -> TravelState:

    logger.info("Replan started.")
    node_start = time.perf_counter()

    state["replan_attempts"] += 1

    logger.info(
        f"Replan attempt {state['replan_attempts']}"
    )

    prompt = f"""
You are a travel planner responsible for fixing an over-budget trip.

Destination:
{state["destination"]}

Days:
{state["days"]}

Month:
{state["month"]}

Maximum budget:
{state["budget"]}

Current total:
${state["total_cost"]}

Current flight:
{state["selected_flight"]}

Current hotel:
{state["selected_hotel"]}

Current activities:
{state["selected_activities"]}

Available flights:
{state["flight_options"]}

Available hotels:
{state["hotel_options"]}

Available activities:
{state["activity_options"]}

Interests:
{state["interests"]}

Rules:

1. Stay within the budget if possible.
2. Select only IDs from available options.
3. Do not invent anything.
4. Prefer cheaper flight and hotel options.
5. Keep important activities when possible.
6. Remove expensive activities before removing all activities.
7. Return the cheapest reasonable combination.
"""

    logger.info("Replan LLM started.")
    llm_start = time.perf_counter()

    result = planner_llm.invoke(prompt)

    llm_elapsed = time.perf_counter() - llm_start
    logger.info(
        f"Replan LLM completed in {llm_elapsed:.3f}s"
    )

    selected_flight = next(
        (
            flight
            for flight in state["flight_options"]
            if flight["id"] == result.flight_id
        ),
        {}
    )

    selected_hotel = next(
        (
            hotel
            for hotel in state["hotel_options"]
            if hotel["id"] == result.hotel_id
        ),
        {}
    )

    selected_activities = [
        activity
        for activity in state["activity_options"]
        if activity["id"] in result.activity_ids
    ]

    state["selected_flight"] = selected_flight
    state["selected_hotel"] = selected_hotel
    state["selected_activities"] = selected_activities

    logger.info(
        f"Replan selected | "
        f"flight={result.flight_id} | "
        f"hotel={result.hotel_id} | "
        f"activities={result.activity_ids}"
    )

    logger.info(
        f"Replan reasoning: {result.reasoning}"
    )

    elapsed = time.perf_counter() - node_start

    logger.info(
        f"Replan completed in {elapsed:.3f}s"
    )

    return state