# from typing import TypedDict


# class TravelState(TypedDict):

#     user_request: str

#     destination: str
#     days: int
#     month: str
#     budget: str

#     hotel_preference: str
#     interests: list

#     flight_options: list
#     hotel_options: list
#     activity_options: list

#     selected_flight: dict
#     selected_hotel: dict
#     selected_activities: list

#     total_cost: float
#     budget_exceeded: bool

#     replan_attempts: int

#     messages: list

#     final_plan: dict

from typing import TypedDict


class TravelState(TypedDict):

    user_request: str

    destination: str
    days: int
    month: str
    budget: str

    hotel_preference: str
    interests: list[str]

    flight_options: list
    hotel_options: list
    activity_options: list

    selected_flight: dict
    selected_hotel: dict
    selected_activities: list

    total_cost: float
    budget_exceeded: bool

    replan_attempts: int

    final_plan: dict