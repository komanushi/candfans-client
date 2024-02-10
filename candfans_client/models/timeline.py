from pydantic import BaseModel


class TimelineMonth(BaseModel):
    column_name: str
