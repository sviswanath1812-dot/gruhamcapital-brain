from pydantic import BaseModel


class Consultation(BaseModel):
    name: str
    mobile: int
    email: str
    purpose: str
    slot_id: str


class Slot(BaseModel):
    name: str
    description: str = ""
    starttime: int
    endtime: int
    total: int
