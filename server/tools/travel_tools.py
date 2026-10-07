from langchain_core.tools import tool

from mock_data.data import (
    FLIGHTS,
    HOTELS,
    ACTIVITIES
)


@tool
def search_flights(destination: str) -> list[dict]:
    """
    Search available flights for a destination.
    """

    return [
        flight
        for flight in FLIGHTS
        if flight["to"].lower() == destination.lower()
    ]


@tool
def search_hotels(
    destination: str,
    minimum_rating: int = 3
) -> list[dict]:
    """
    Search available hotels for a destination.
    """

    return [
        hotel
        for hotel in HOTELS
        if hotel["rating"] >= minimum_rating
    ]


@tool
def search_activities(
    destination: str,
    interests: list[str]
):
    """
    Search activities matching the user's interests.
    """
    return [
        activity
        for activity in ACTIVITIES
        if activity["destination"].lower() == destination.lower()
        and activity["category"] in interests
    ]