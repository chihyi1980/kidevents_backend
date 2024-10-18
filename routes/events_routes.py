from datetime import datetime 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db.events_db import insert_event, find_all_events, update_event, find_event_by_id
import pytz
from db.option_db import find_all_loc, find_all_tag

# 定義 UTC 和目標時區
utc = pytz.UTC
target_tz = pytz.timezone('Asia/Taipei')  # UTC+8 時區，以台北為例

events_bp = Blueprint('events_bp', __name__)

@events_bp.route('/events/create', methods=['POST'])
# @jwt_required()
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
    return jsonify([{**event, "_id": str(event["_id"])} for event in sorted_events])

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

@events_bp.route('/events/online_detail/<event_id>', methods=['GET'])
def get_event_detail(event_id):
    event = find_event_by_id(event_id)
    if event:
        temp = {}
        temp['event_link'] = event['event_link']
        temp['event_content'] = event['event_content']
        temp['event_loc_detail'] = event['event_loc_detail']
        temp['_id'] = str(event['_id'])
        return jsonify(temp)
    return jsonify({"message": "Event not found"}), 404

@events_bp.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    event = find_event_by_id(event_id)
    if event:
        event['_id'] = str(event['_id'])
        return jsonify(event)
    return jsonify({"message": "Event not found"}), 404

@events_bp.route('/events/online/<event_id>', methods=['GET'])
def get_event_online(event_id):
    event = find_event_by_id(event_id)

    if event:
        locs = find_all_loc()
        locs_dict = {}
        for loc in locs:
            locs_dict[str(loc['_id'])] = loc['value']
        
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
        try:
            event_start_date = datetime.strptime(event['event_start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            event_start_date = event_start_date.replace(tzinfo=utc).astimezone(target_tz)
            event['event_start_date'] = event_start_date.strftime('%Y-%m-%d')
        except ValueError:
            # 日期格式不符合指定格式，保持原始值
            pass

        # 將 event_end_date 格式化為 yyyy-MM-dd
        try:
            event_end_date = datetime.strptime(event['event_end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            event_end_date = event_end_date.replace(tzinfo=utc).astimezone(target_tz)
            event['event_end_date'] = event_end_date.strftime('%Y-%m-%d')
        except ValueError:
            # 日期格式不符合指定格式，保持原始值
            pass

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
        # del event['created_at']
        del event['updated_at']
        del event['is_enabled']
        del event['is_online']
        del event['event_link']
        del event['event_content']
        del event['event_loc_detail']

        # 將 event_start_date 格式化為 yyyy-MM-dd
        try:
            event_start_date = datetime.strptime(event['event_start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            event_start_date = event_start_date.replace(tzinfo=utc).astimezone(target_tz)
            event['event_start_date'] = event_start_date.strftime('%Y-%m-%d')
        except ValueError:
            # 日期格式不符合指定格式，保持原始值
            pass

        # 將 event_end_date 格式化為 yyyy-MM-dd
        try:
            event_end_date = datetime.strptime(event['event_end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            event_end_date = event_end_date.replace(tzinfo=utc).astimezone(target_tz)
            event['event_end_date'] = event_end_date.strftime('%Y-%m-%d')
        except ValueError:
            # 日期格式不符合指定格式，保持原始值
            pass
        
    # 將事件按 created_at 日期從舊到新排序
    sorted_events = sorted(events, key=lambda x: x.get('created_at', 0), reverse=True)

    # 返回結果，並將 _id 轉換為字符串
    return jsonify([{**loc, "_id": str(loc["_id"])} for loc in sorted_events]) 

#處理由爬蟲自動生成的add event
@events_bp.route('/events/create_crawler', methods=['POST'])
# @jwt_required()
def add_event_crawler():
    data = request.get_json()

    #如果在config 中有指定 loc name，則轉換為 loc id，如果沒有則不選
    if 'event_loc_name' in data:
        #先建立 loc map，將 縣市名稱 轉換為 id
        locs = find_all_loc()
        locs_dict = {}
        for loc in locs:
            locs_dict[loc['value']] = str(loc['_id']) 

        #轉換 loc_name to loc
        data['event_loc'] = locs_dict[data['event_loc_name']]
        del data['event_loc_name']

    tags = find_all_tag()
    tags_dict = {}
    for tag in tags:
        tag['_id'] = str(tag['_id'])
        tags_dict[tag['value']] = tag

    data['event_tag'] = []
    for tag_name in data['event_tag_name']:
        try:
            data['event_tag'].append(tags_dict[tag_name])
        except KeyError:
            continue
    del data['event_tag_name']

       
    utc_now = datetime.now(pytz.utc)
    local_time = utc_now.astimezone(pytz.timezone('Asia/Taipei'))
    data['created_at'] = local_time.isoformat()
    data['updated_at'] = local_time.isoformat()
    data['is_online'] = False
    data['is_enabled'] = True
    insert_event(data)
    return jsonify({"msg": "Event added successfully"}), 201
