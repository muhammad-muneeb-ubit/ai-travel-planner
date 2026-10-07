from graphs.state import TravelState
from config.config import llm
import json

def parse_request(state: TravelState) -> TravelState:
    print("Running parse_request node...")
    user_request = state["user_request"]
    response = llm.invoke(
        f"""Extract the following information from the user's request: destination, days, month, budget, interests, hotel_preference. 
            User request: {user_request}. Just return the response in JSON format. If any info not provide from the user then add null for that field. dont add any extra text. The response should be in the following format:
        {{
            "destination": "country or city name",
            "days": number of days,
            "month": "month name",
            "budget": "budget amount",
            "interests": ["interest1", "interest2"],
            "hotel_preference": "2-starts, 3-stars, 4-stars, 5-stars"
            }}
            """
    )
    data = json.loads(response.content[0]['text'])
    
    # print("LLM Response:", response.content[0]['text'])
    state["destination"] = data['destination']
    state["days"] = data['days']
    state["month"] = data['month']
    state["budget"] = data['budget']
    state["interests"] = data['interests']
    state["hotel_preference"] = data['hotel_preference']
    return state

def apply_defaults(state: TravelState) -> TravelState:
    print("Running apply_defaults node...")

    # Default hotel preference
    if not state["hotel_preference"]:
        state["hotel_preference"] = "3-star"

    # Default interests
    if not state["interests"]:
        state["interests"] = [
            "sightseeing",
            "food",
            "culture"
        ]

    return state

def get_budget_amount(budget):

    budget = str(budget)
    budget = budget.replace("$", "")
    budget = budget.replace(",", "")

    return int(float(budget))


def calculate_budget(state: TravelState) -> TravelState:

    print("Running calculate_budget node...")

    flight_cost = (
        state["selected_flight"].get("price", 0)
    )

    hotel_cost = (
        state["selected_hotel"].get("price_per_night", 0)
        * (state["days"] - 1)
    )

    activity_cost = sum(
        activity.get("price", 0)
        for activity in state["selected_activities"]
    )

    total_cost = (
        flight_cost
        + hotel_cost
        + activity_cost
    )

    budget_amount = get_budget_amount(
        state["budget"]
    )

    state["total_cost"] = total_cost

    state["budget_exceeded"] = (
        total_cost > budget_amount
    )

    print("Flight cost:", flight_cost)
    print("Hotel cost:", hotel_cost)
    print("Activity cost:", activity_cost)
    print("Total cost:", total_cost)
    print("Budget:", budget_amount)
    print("Budget exceeded:", state["budget_exceeded"])

    return state
def check_budget(state: TravelState) -> TravelState:
    print("Running check_budget node...")

    if state["total_cost"] <= int(state["budget"][1:]):
        state["budget_exceeded"] = False
    else:
        state["budget_exceeded"] = True

    print("Budget:", state["budget"])
    print("Total cost:", state["total_cost"])
    print("Budget exceeded:", state["budget_exceeded"])

    return state

def create_final_plan(state: TravelState) -> TravelState:
    print("Running create_final_plan node...")

    state["final_plan"] = {
        "destination": state["destination"],
        "days": state["days"],
        "month": state["month"],
        "budget": state["budget"],

        "flight": state["selected_flight"],

        "hotel": state["selected_hotel"],

        "activities": state["selected_activities"],

        "total_cost": state["total_cost"],

        "remaining_budget": (
           int(state["budget"][1:])- state["total_cost"]
        )
    }

    return state

def route_after_budget_check(state: TravelState) -> str:

    if not state["budget_exceeded"]:
        return "final_plan"

    if state["replan_attempts"] >= 3:
        return "final_plan"

    return "replan"


# def extract_selections(state: TravelState) -> TravelState:
    print("Running extract_selections node...")

    # Find the latest AI response
    messages = state["messages"]

    last_ai_message = messages[-1]

    content = last_ai_message.content

    # Gemini may return structured content
    if isinstance(content, list):
        content = content[0]["text"]

    data = json.loads(content)

    flight_id = data["flight_id"]
    hotel_id = data["hotel_id"]
    activity_ids = data["activity_ids"]

    selected_flight = next(
        (
            flight
            for flight in state["flight_options"]
            if flight["id"] == flight_id
        ),
        {}
    )

    selected_hotel = next(
        (
            hotel
            for hotel in state["hotel_options"]
            if hotel["id"] == hotel_id
        ),
        {}
    )

    selected_activities = [
        activity
        for activity in state["activity_options"]
        if activity["id"] in activity_ids
    ]

    state["selected_flight"] = selected_flight
    state["selected_hotel"] = selected_hotel
    state["selected_activities"] = selected_activities

    return state