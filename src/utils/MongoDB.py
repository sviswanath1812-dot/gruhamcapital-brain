from pymongo import MongoClient
from pymongo.cursor import Cursor

from src.utils.Models import Slot
from bson import ObjectId
from src.utils.Constants import (
    DATABASE_NAME,
    CONSULTATION_DB,
    SLOTS_DB,
    MONGO_URL,
)


class GruhamDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URL, tls=True, tlsAllowInvalidCertificates=True)
        self.database = self.client.get_database(DATABASE_NAME)


class GruhamConsultationsDB(GruhamDB):
    def __init__(self):
        super().__init__()
        self.collection = self.database.get_collection(CONSULTATION_DB)

    # Consultations
    def add_consultation(self, consultation_data: dict):
        collection = self.database.get_collection(CONSULTATION_DB)
        added_id = collection.insert_one(consultation_data)
        if added_id:
            return added_id
        return False

    def get_consultations(self, starttime, endtime, consultation_id):
        collection = self.database.get_collection(CONSULTATION_DB)

        query = {"$and": [{"date": {"$gte": starttime}}, {"date": {"$lte": endtime}}]}

        # Add Consultation ID if needed
        if consultation_id:
            query["_id"] = ObjectId(consultation_id)

        records: Cursor = collection.find(query)

        final_records = []
        for record in records:
            record["id"] = str(record["_id"])
            del record["_id"]
            final_records.append(record)
        return final_records


class GruhamSlotsDB(GruhamDB):
    def __init__(self):
        super().__init__()
        self.collection = self.database.get_collection(SLOTS_DB)

    def add_slots(self, slot_data: dict):

        slot_data["availabile"] = slot_data["total"]
        added_id = self.collection.insert_one(slot_data)
        if added_id:
            return True
        return False

    def increase_slots(self, slot_id: str, number: int):
        record: Slot = self.collection.find_one({"_id": ObjectId(slot_id)})
        self.collection.update_one(
            {"_id": ObjectId(slot_id)},
            {
                "$set": {
                    "available": record["available"] + number,
                    "total": record["total"] + number,
                }
            },
        )

    def decrease_slots(self, slot_id: str, number: int):
        record: dict = self.collection.find_one({"_id": ObjectId(slot_id)})
        self.collection.update_one(
            {"_id": ObjectId(slot_id)},
            {
                "$set": {
                    "available": record["available"] - number,
                    "total": record["total"] + number,
                }
            },
        )

    def get_availability(self, slot_id: str):
        record: dict = self.collection.find_one({"_id": ObjectId(slot_id)})
        return record["available"]

    def get_all_slots(self, starttime: int, endtime: int) -> list[dict]:
        records: Cursor = self.collection.find(
            {
                "$and": [
                    {"starttime": {"$gte": starttime}},
                    {"endtime": {"$lte": endtime}},
                ]
            }
        )

        final_records = []
        for record in records:
            record["id"] = str(record["_id"])
            del record["_id"]
            final_records.append(record)
        return final_records


# this global variable is for maintaining singleton
gruham_slots_db = GruhamSlotsDB()
gruham_consultations_db = GruhamConsultationsDB()


def get_connected_consultations_database():
    return gruham_consultations_db


def get_connected_slot_database():
    return gruham_slots_db
