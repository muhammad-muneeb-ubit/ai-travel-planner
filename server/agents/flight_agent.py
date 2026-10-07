from tools.travel_tools import search_flights


def flight_agent(state):

    print("Running flight_agent node...")

    flights = search_flights.invoke({
        "destination": state["destination"]
    })

    state["flight_options"] = flights

    print("Flight options:", flights)

    return state