from tools.travel_tools import search_hotels


def hotel_agent(state):

    print("Running hotel_agent node...")

    minimum_rating = int(
        state["hotel_preference"].split("-")[0]
    )

    hotels = search_hotels.invoke({
        "destination": state["destination"],
        "minimum_rating": minimum_rating
    })

    state["hotel_options"] = hotels

    print("Hotel options:", hotels)

    return state