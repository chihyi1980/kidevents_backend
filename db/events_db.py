from pymongo import MongoClient
from bson import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
events_db = client['events_db']
events_collection = events_db['events']

def insert_event(event):
    return events_collection.insert_one(event)

def find_all_events():
    return list(events_collection.find())

def update_event(event_id, updated_data):
    return events_collection.update_one({'_id': ObjectId(event_id)}, {'$set': updated_data})

def find_event_by_id(event_id):
    return events_collection.find_one({'_id': ObjectId(event_id)})