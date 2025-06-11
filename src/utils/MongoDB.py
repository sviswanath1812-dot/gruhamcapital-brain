from pymongo import MongoClient
from dotenv import load_dotenv
import os
from src.utils.Models import Slot
from bson import ObjectId

load_dotenv()

SLOTS = os.getenv("SLOTS_DB")


class GruhamDB:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URL"))
        self.database = self.client.get_database(os.getenv("MONGO_DATABASE"))

    def add_consultation(self, consultation_data: dict):
        collection = self.database.get_collection("consultations")
        added_id = collection.insert_one(consultation_data)
        if added_id:
            return added_id
        return False

    def add_slots(self, slot_data: dict):
        collection = self.database.get_collection(SLOTS)
        slot_data["availabile"] = slot_data["total"]
        added_id = collection.insert_one(slot_data)
        if added_id:
            return added_id
        return False

    def increase_slots(self, slot_id: str, number: int):
        collection = self.database.get_collection(SLOTS)
        record: Slot = collection.find_one({"_id": ObjectId(slot_id)})
        collection.update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": {"available": record["available"] + number}},
        )

    def decrease_slots(self, slot_id: str, number: int):
        collection = self.database.get_collection(SLOTS)
        record: dict = collection.find_one({"_id": ObjectId(slot_id)})
        collection.update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": {"available": record["available"] - number}},
        )

    def get_availability(self, slot_id: str):
        collection = self.database.get_collection(SLOTS)
        record: dict = collection.find_one({"_id": ObjectId(slot_id)})
        return record["available"]


# this global variable is for maintaining singleton
gruham_db = GruhamDB()


def get_connected_database():
    return gruham_db
