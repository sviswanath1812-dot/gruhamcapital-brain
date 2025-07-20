from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()


class GrishamTimes(Enum):
    DEFAULT_START: int = 0
    DEFAULT_END: int = 100000000000000


SLOTS_DB = os.getenv("SLOTS_DB")
CONSULTATION_DB = os.getenv("CONSULTATION_DB")
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("MONGO_DATABASE")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")