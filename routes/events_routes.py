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
    data['is_online'] = 0
    insert_event(data)
    return jsonify({"msg": "Event added successfully"}), 201

@events_bp.route('/events/list', methods=['GET'])
def get_events():
    events = find_all_events()

    # 遍歷每個事件，提取 events_tag 中的 _id 並存入 events_tag_ids
    for event in events:
        # 假設 events_tag 是一個列表，提取其中的每個 _id
        if 'event_tag' in event:
            event_tag_ids = [tag.get('_id') for tag in event['event_tag'] if '_id' in tag]
            event['event_tag_ids'] = event_tag_ids

    # 將事件按 created_at 日期從新到舊排序
    sorted_events = sorted(events, key=lambda x: x.get('created_at', 0), reverse=True)

    # 返回結果，並將 _id 轉換為字符串
    return jsonify([{**loc, "_id": str(loc["_id"])} for loc in sorted_events])


