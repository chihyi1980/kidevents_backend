from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
user_db = client['user_db']
user_collection = user_db['user']

def insert_user(user):
    return user_collection.insert_one(user)

def find_user_by_name(user_name):
    return user_collection.find_one({"user_name": user_name})
