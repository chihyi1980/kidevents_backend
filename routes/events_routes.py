from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db.events_db import insert_event, find_all_events

events_bp = Blueprint('events_bp', __name__)

@events_bp.route('/events', methods=['POST'])
@jwt_required()
def add_event():
    data = request.get_json()
    event = {
        "event_id": data['event_id'],
        "event_name": data['event_name'],
        "event_start_time": data['event_start_time'],
        "event_end_time": data['event_end_time'],
        "event_price": data['event_price'],
        "event_age_start": data['event_age_start'],
        "event_age_end": data['event_age_end'],
        "event_desc": data['event_desc'],
        "event_link": data['event_link'],
        "event_pics": data['event_pics'],
    }
    insert_event(event)
    return jsonify({"msg": "Event added successfully"}), 201

@events_bp.route('/events', methods=['GET'])
def get_events():
    events = find_all_events()
    for event in events:
        event['_id'] = str(event['_id'])  # 将MongoDB对象ID转换为字符串
    return jsonify(events), 200
