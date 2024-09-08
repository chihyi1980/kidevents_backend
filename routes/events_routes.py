from datetime import datetime 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db.events_db import insert_event, find_all_events, update_event, find_event_by_id
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
    data['is_online'] = False
    data['is_enabled'] = True
    insert_event(data)
    return jsonify({"msg": "Event added successfully"}), 201

@events_bp.route('/events/list', methods=['GET'])
def get_events():
    # 过滤掉 is_enabled != True 的 events
    events = [event for event in find_all_events() if event.get('is_enabled') == True]

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



@events_bp.route('/events/<event_id>', methods=['PUT'])
def update_event_route(event_id):
    event_data = request.json

    # 删除不可修改的 `_id` 字段
    if '_id' in event_data:
        del event_data['_id']

    #更新 last updated 時間
    utc_now = datetime.now(pytz.utc)
    local_time = utc_now.astimezone(pytz.timezone('Asia/Taipei'))
    event_data['updated_at'] = local_time.isoformat()

    result = update_event(event_id, event_data)
    if result.modified_count:
        return jsonify({"message": "Event updated successfully"})
    return jsonify({"message": "Event not found"}), 404

@events_bp.route('/event/<event_id>', methods=['GET'])
def get_event(event_id):
    event = find_event_by_id(event_id)
    if event:
        event['_id'] = str(event['_id'])
        return jsonify(event)
    return jsonify({"message": "Event not found"}), 404

@events_bp.route('/events/online_list', methods=['GET'])
def get_online_events():
    # 过滤掉 is_enabled != True 的 events
    events = [event for event in find_all_events() if (event.get('is_enabled') == True and event.get('is_online') == True)]

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