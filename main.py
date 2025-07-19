from fastapi import FastAPI, Depends, Response
from src.utils.MongoDB import (
    get_connected_slot_database,
    GruhamSlotsDB,
    get_connected_consultations_database,
    GruhamConsultationsDB,
)
from src.utils.Models import Consultation, Slot
from src.utils.Constants import GruhamTimes
import json
from bson.errors import InvalidId

app = FastAPI()


@app.get("/ping")
async def ping_api():
    return Response("success", 200)


# Consultations
@app.post("/add_consultation")
async def add_consulatation(
    data: Consultation,
    db: GruhamConsultationsDB = Depends(get_connected_consultations_database),
):
    try:
        db.add_consultation(json.loads(data.model_dump_json()))
        return Response("Consultation Added", 200)
    except Exception as e:
        return Response(f"Consultation failed {e}", 500)


@app.post("/consultations")
async def get_consultations(
    starttime: int = GruhamTimes.DEFAULT_START.value,
    endtime: int = GruhamTimes.DEFAULT_END.value,
    consultation_id: str = "",
    db: GruhamConsultationsDB = Depends(get_connected_consultations_database),
):
    try:
        return db.get_consultations(starttime, endtime, consultation_id)
    except InvalidId as e:
        return Response(f"Given Consultation ID is Invalid")
    except Exception as e:
        return Response(f"Consultation availability failed {e}", 500)


# Slots
@app.post("/add_slots")
async def add_slots(
    data: Slot, db: GruhamSlotsDB = Depends(get_connected_slot_database)
):
    try:
        slot_id = db.add_slots(json.loads(data.model_dump_json()))
        return Response(f"Slot Added with ID {slot_id}", 200)
    except Exception as e:
        return Response(f"Slot addition failed {e}", 500)


@app.post("/increase_availablity")
async def increase_slots(
    slot_id: str, number: int, db: GruhamSlotsDB = Depends(get_connected_slot_database)
):
    try:
        db.increase_slots(slot_id, number)
        return Response("Slots increased to the timeframe slot", 200)
    except Exception as e:
        return Response(f"Slots increase failed {e}", 500)


@app.post("/decrease_availablity")
async def increase_slots(
    slot_id: str, number: int, db: GruhamSlotsDB = Depends(get_connected_slot_database)
):
    try:
        db.decrease_slots(slot_id, number)
        return Response("Slots increased to the timeframe slot", 200)
    except Exception as e:
        return Response(f"Slots increase failed {e}", 500)


@app.get("/slot_availability/{slot_id}")
async def slot_availability(
    slot_id: str, db: GruhamSlotsDB = Depends(get_connected_slot_database)
):
    try:
        slots = db.get_availability(slot_id)
        return Response(f"{slots}", 200)
    except Exception as e:
        return Response(f"Slots availability failed {e}", 500)


@app.post("/slots")
async def get_slots(
    starttime: int = GruhamTimes.DEFAULT_START.value,
    endtime: int = GruhamTimes.DEFAULT_END.value,
    db: GruhamSlotsDB = Depends(get_connected_slot_database),
):
    try:
        return db.get_all_slots(starttime, endtime)
    except Exception as e:
        return Response(f"Slots availability failed {e}", 500)
