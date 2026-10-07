from pydantic import BaseModel, Field


class TravelSelection(BaseModel):
    flight_id: str
    hotel_id: str
    activity_ids: list[str]
    reasoning: str
    
class TravelReplan(BaseModel):
    flight_id: str
    hotel_id: str
    activity_ids: list[str]
    reasoning: str
    
class TravelPlan(BaseModel):

    flight_id: str = Field(
        description="Selected flight ID"
    )

    hotel_id: str = Field(
        description="Selected hotel ID"
    )

    activity_ids: list[str] = Field(
        description="Selected activity IDs"
    )

    reasoning: str = Field(
        description="Brief explanation"
    )
