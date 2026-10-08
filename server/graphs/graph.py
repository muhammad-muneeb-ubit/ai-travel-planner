from langgraph.graph import StateGraph, START, END
from graphs.state import TravelState
from graphs.nodes import parse_request, apply_defaults, calculate_budget, check_budget,  create_final_plan, route_after_budget_check
from agents.travel_planner import replan_with_llm, travel_planner
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.activity_agent import activity_agent


graph = StateGraph(TravelState)

graph.add_node("parse_request", parse_request)
graph.add_node("apply_defaults", apply_defaults)
graph.add_node("flight_agent",flight_agent)
graph.add_node("hotel_agent",hotel_agent)
graph.add_node("activity_agent",activity_agent)
graph.add_node( "travel_planner", travel_planner )
graph.add_node("calculate_budget", calculate_budget)
graph.add_node("check_budget", check_budget)
graph.add_node("replan_with_llm", replan_with_llm)
graph.add_node("create_final_plan", create_final_plan)
graph.add_node("route_after_budget_check", route_after_budget_check)



graph.add_edge(START, "parse_request")
graph.add_edge("parse_request", "apply_defaults")
graph.add_edge("apply_defaults", "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "activity_agent")
graph.add_edge("activity_agent", "travel_planner")
graph.add_edge("travel_planner", "calculate_budget")

graph.add_edge("calculate_budget", "check_budget")
graph.add_conditional_edges("check_budget", route_after_budget_check, 
                            {
                                "replan": "replan_with_llm",
                                "final_plan": "create_final_plan"
                            })
        
graph.add_edge("replan_with_llm", "calculate_budget")
graph.add_edge("create_final_plan", END)


travel_graph = graph.compile()

