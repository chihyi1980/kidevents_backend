from datetime import datetime 
from flask import Blueprint, request, jsonify
from db.crawler_db import insert_used_url, is_url_exist, insert_crawler_config, find_all_crawler_config, update_crawler_config

crawler_bp = Blueprint('crawler_bp', __name__)

#建立新爬取過URL紀錄
@crawler_bp.route('/crawler/used_url/create', methods=['POST'])
def add_used_url():
    data = request.get_json()
    insert_used_url(data)
    return jsonify({"msg": "Used URL added successfully"}), 201

#先判斷這個event是否已經爬過
@crawler_bp.route('/crawler/used_url/check', methods=['POST'])
def check_used_url():
    data = request.get_json()
    url = data['value']
    result = is_url_exist(url)
    if result == True:
        return jsonify({'value': True}), 201
    else:
        return jsonify({'value': False}), 201
    
#新增 crawler config
@crawler_bp.route('/crawler/config/create', methods=['POST'])
def add_config():
    data = request.get_json()
    insert_crawler_config(data)
    return jsonify({"msg": "crawler config added successfully"}), 201

#取得 crawler config 列表
@crawler_bp.route('/crawler/config/list', methods=['GET'])
def get_config():
    configs = find_all_crawler_config()
    
    # 返回結果，並將 _id 轉換為字符串
    return jsonify([{**con, "_id": str(con["_id"])} for con in configs])

# 取得 crawler config ，並且依照取得的順序，將其hour與 min 分別設置為從00:30分開始，每一個時間間隔5分鐘
@crawler_bp.route('/crawler/config/resetRunTime', methods=['GET'])
def reset_run_time():
    configs = find_all_crawler_config()
    
    # 初始化時間
    current_hour = 0
    current_minute = 30
    
    for con in configs:
        
        # 更新時間
        current_minute += 5
        if current_minute >= 60:
            current_minute = 0
            current_hour += 1
        
        data = {}
        data['hour'] = current_hour
        data['minute'] = current_minute

        # 打印設置的時間
        update_crawler_config(str(con['_id']), data)
    
    return 'OK'
