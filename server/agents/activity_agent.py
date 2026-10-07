from tools.travel_tools import search_activities


def activity_agent(state):

    print("Running activity_agent node...")

    activities = search_activities.invoke({
        "destination": state["destination"],
        "interests": state["interests"]
    })

    state["activity_options"] = activities

    print("Activity options:", activities)

    return state