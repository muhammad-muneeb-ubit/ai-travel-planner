from fastapi import FastAPI
from graphs.graph import travel_graph
app = FastAPI(title="AI Travel Planner")


@app.get("/")
def root():
    return {
        "   ": "AI Travel Planner API is running"
    }
    
    
    
initial_state = {

    "user_request":
        "I want to visit Istanbul for 5 days in December with a $1000 budget",

    "destination": "",
    "days": 0,
    "month": "",
    "budget": "",

    "hotel_preference": "",
    "interests": [],

    "flight_options": [],
    "hotel_options": [],
    "activity_options": [],

    "selected_flight": {},
    "selected_hotel": {},
    "selected_activities": [],

    "total_cost": 0,
    "budget_exceeded": False,

    "replan_attempts": 0,

    "final_plan": {}
}
result = travel_graph.invoke(initial_state)

print("\nFinal State:")
print(result)