from fastapi import FastAPI
from graphs.graph import travel_graph
import time
from log import logger
import asyncio
import json
from fastapi.responses import StreamingResponse
from mock_data.data import PROGRESS_MESSAGES
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Travel Planner")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return { "   ": "AI Travel Planner API is running" }
    
@app.get("/api/travel-plan")
def travel_plan(user_request: str):

    initial_state = {
        "user_request": {user_request},

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

    return result

@app.get("/api/plan/stream")
async def plan_stream(request: str):

    async def event_generator():

        initial_state = {
            "user_request": request,
            "destination": None,
            "days": None,
            "month": None,
            "budget": None,
            "interests": None,
            "hotel_preference": None,

            "flight_options": [],
            "hotel_options": [],
            "activity_options": [],

            "selected_flight": {},
            "selected_hotel": {},
            "selected_activities": [],

            "total_cost": 0,
            "budget_exceeded": False,
            "replan_attempts": 0,

            "final_plan": {},

            "progress_message": ""
        }

        try:

            yield f"data: {json.dumps({
                'type': 'start',
                'message': 'Starting your travel plan...'
            })}\n\n"

            for update in travel_graph.stream(
                initial_state,
                stream_mode="updates"
            ):

                for node_name, state_update in update.items():

                    message = PROGRESS_MESSAGES.get(
                        node_name,
                        f"Running {node_name}..."
                    )

                    # Special budget message
                    if node_name == "check_budget":

                        if state_update.get("budget_exceeded"):
                            message = "⚠️ Your trip exceeds the budget."
                        else:
                            message = "✓ Trip is within your budget."

                    # Special replan message
                    if node_name == "replan_with_llm":

                        attempt = state_update.get(
                            "replan_attempts",
                            0
                        )

                        message = (
                            f"🔄 Optimizing your trip "
                            f"— attempt {attempt} of 3..."
                        )

                    event = {
                        "type": "progress",
                        "node": node_name,
                        "message": message
                    }

                    yield f"data: {json.dumps(event)}\n\n"

                    await asyncio.sleep(0.05)

                    # Final result
                    if node_name == "create_final_plan":

                        final_plan = state_update.get(
                            "final_plan"
                        )

                        yield f"data: {json.dumps({
                            'type': 'complete',
                            'message': '🎉 Trip planned successfully!',
                            'plan': final_plan
                        })}\n\n"

        except Exception as e:

            yield f"data: {json.dumps({
                'type': 'error',
                'message': str(e)
            })}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )