from pymongo import MongoClient
from bson import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
crawler_db = client['crawler_db']
used_url_collection = crawler_db['used_url']

def insert_used_url(url):
    return used_url_collection.insert_one(url)

def is_url_exist(url):
    query = {"value": url}
    result = used_url_collection.find_one(query)
    return result is not None
