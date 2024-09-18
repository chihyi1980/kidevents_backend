from datetime import datetime 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db.events_db import insert_event, find_all_events, update_event, find_event_by_id
import pytz
from db.option_db import find_all_loc


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
    # 过滤掉 is_enabled != True && is_online != True 的 events
    events = [event for event in find_all_events() if (event.get('is_enabled') == True and event.get('is_online') == True)]

    locs = find_all_loc()
    locs_dict = {}
    for loc in locs:
        locs_dict[str(loc['_id'])] = loc['value']

    # 遍歷每個事件，提取 events_tag 中的 _id 並存入 events_tag_ids
    for event in events:
        # 假設 events_tag 是一個列表，提取其中的每個 _id
        if 'event_tag' in event:
            event_tag_names = [tag.get('value') for tag in event['event_tag'] if '_id' in tag]
            event['event_tag_names'] = event_tag_names
            del event['event_tag']
        if 'event_loc' in event:
            event['event_loc_name'] = locs_dict[event['event_loc']]
            del event['event_loc']
        del event['created_at']
        del event['updated_at']
        del event['is_enabled']
        del event['is_online']

        # 將 event_start_date 格式化為 yyyy-MM-dd
        event_start_date = datetime.strptime(event['event_start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        event['event_start_date'] = event_start_date.strftime('%Y-%m-%d')

        # 將 event_end_date 格式化為 yyyy-MM-dd
        event_end_date = datetime.strptime(event['event_end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        event['event_end_date'] = event_end_date.strftime('%Y-%m-%d')
        
    # 將事件按 event_start_date 日期從舊到新排序
    sorted_events = sorted(events, key=lambda x: x.get('event_start_date', 0), reverse=False)

    # 返回結果，並將 _id 轉換為字符串
    return jsonify([{**loc, "_id": str(loc["_id"])} for loc in sorted_events]) 