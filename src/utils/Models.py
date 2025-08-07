from pydantic import BaseModel
from src.utils.Constants import GruhamTimes


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


class SlotsDTO(BaseModel):
    starttime: int = GruhamTimes.DEFAULT_START.value
    endtime: int = GruhamTimes.DEFAULT_END.value


class ConsultationsDTO(BaseModel):
    starttime: int = GruhamTimes.DEFAULT_START.value
    endtime: int = GruhamTimes.DEFAULT_END.value
    consultation_id: str = ""


class SlotsAvailabilityDTO(BaseModel):
    slot_id: str
    number: int
