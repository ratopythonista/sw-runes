import os
from pymongo import MongoClient


password = os.environ.get("MONGO_DB_PASS")

class Database():
    def __init__(self) -> None:
        client = MongoClient(f"mongodb+srv://ratopythonista:{password}@ratopythonista.lj1z2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = client.swr
    
    def insert(self, info: dict):
        self.db.runes.insert_one(info)

    def find_among_all(self, slot: int, rune_type: str, sub_type: str):
        return self.db.runes.find(filter={
            "slot": slot,
            "rune_type": rune_type,
            f"sub.{sub_type}": { '$gt': 0 }
        })