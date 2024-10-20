from datetime import datetime 
from flask import Blueprint, request, jsonify
from db.crawler_db import insert_used_url, is_url_exist, insert_crawler_config, find_all_crawler_config

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