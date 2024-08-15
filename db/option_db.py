from pymongo import MongoClient
from bson import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
option_db = client['option_db']
loc_collection = option_db['loc']
tag_collection = option_db['tag']

# CRUD operations for loc

def insert_loc(loc):
    return loc_collection.insert_one(loc)

def find_all_loc():
    return list(loc_collection.find())

def find_loc_by_id(loc_id):
    return loc_collection.find_one({'_id': ObjectId(loc_id)})

def update_loc(loc_id, updated_data):
    return loc_collection.update_one({'_id': ObjectId(loc_id)}, {'$set': updated_data})

def delete_loc(loc_id):
    return loc_collection.delete_one({'_id': ObjectId(loc_id)})

def bulk_update_loc(updates):
    for update in updates:
        loc_id = update.pop('_id', None)
        if loc_id:
            update_result = loc_collection.update_one(
                {'_id': ObjectId(loc_id)},
                {'$set': update}
            )
    return 'ok'

# CRUD operations for tag

def insert_tag(tag):
    return tag_collection.insert_one(tag)

def find_all_tag():
    return list(tag_collection.find())

def find_tag_by_id(tag_id):
    return tag_collection.find_one({'_id': ObjectId(tag_id)})

def update_tag(tag_id, updated_data):
    return tag_collection.update_one({'_id': ObjectId(tag_id)}, {'$set': updated_data})

def delete_tag(tag_id):
    return tag_collection.delete_one({'_id': ObjectId(tag_id)})

def bulk_update_tag(updates):
    for update in updates:
        tag_id = update.pop('_id', None)
        if tag_id:
            update_result = tag_collection.update_one(
                {'_id': ObjectId(tag_id)},
                {'$set': update}
            )
    return 'ok'