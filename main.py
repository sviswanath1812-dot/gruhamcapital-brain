from fastapi import FastAPI, Depends, Response
from src.utils.MongoDB import get_connected_database, GruhamDB
from src.utils.Models import Consultation, Slot
import json

app = FastAPI()


@app.get("/ping")
async def ping_api():
    return Response("success", 200)


@app.post("/add_consultation")
async def add_consulatation(
    data: Consultation, db: GruhamDB = Depends(get_connected_database)
):
    try:
        db.add_consultation(json.loads(data.model_dump_json()))
        return Response("Consultation Added", 200)
    except Exception as e:
        return Response(f"Consultation failed {e}", 500)


@app.post("/add_slots")
async def add_slots(data: Slot, db: GruhamDB = Depends(get_connected_database)):
    try:
        slot_id = db.add_slots(json.loads(data.model_dump_json()))
        return Response(f"Slot Added with ID {slot_id}", 200)
    except Exception as e:
        return Response(f"Slot addition failed {e}", 500)


@app.post("/increase_availablity")
async def increase_slots(
    slot_id: str, number: int, db: GruhamDB = Depends(get_connected_database)
):
    try:
        db.increase_slots(slot_id, number)
        return Response("Slots increased to the timeframe slot", 200)
    except Exception as e:
        return Response(f"Slots increase failed {e}", 500)


@app.post("/decrease_availablity")
async def increase_slots(
    slot_id: str, number: int, db: GruhamDB = Depends(get_connected_database)
):
    try:
        db.decrease_slots(slot_id, number)
        return Response("Slots increased to the timeframe slot", 200)
    except Exception as e:
        return Response(f"Slots increase failed {e}", 500)


@app.get("/slot_availability/{slot_id}")
async def slot_availability(
    slot_id: str, db: GruhamDB = Depends(get_connected_database)
):
    try:
        slots = db.get_availability(slot_id)
        return Response(f"{slots}", 200)
    except Exception as e:
        return Response(f"Slots availability failed {e}", 500)
