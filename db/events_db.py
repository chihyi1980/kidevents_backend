from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
events_db = client['events_db']
events_collection = events_db['events']

def insert_event(event):
    return events_collection.insert_one(event)

def find_all_events():
    return list(events_collection.find())
