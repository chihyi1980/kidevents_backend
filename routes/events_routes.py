from datetime import datetime 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db.events_db import insert_event, find_all_events
import pytz


events_bp = Blueprint('events_bp', __name__)

@events_bp.route('/events/create', methods=['POST'])
@jwt_required()
def add_event():
    data = request.get_json()
       
    utc_now = datetime.now(pytz.utc)
    local_time = utc_now.astimezone(pytz.timezone('Asia/Taipei'))
    data['created_at'] = local_time.isoformat()
    data['updated_at'] = local_time.isoformat()
    insert_event(data)
    return jsonify({"msg": "Event added successfully"}), 201

@events_bp.route('/events/list', methods=['GET'])
def get_events():
    events = find_all_events()
    sorted_events = sorted(events, key=lambda x: x.get('created_at', 0))
    return jsonify([{**loc, "_id": str(loc["_id"])} for loc in sorted_events])        

