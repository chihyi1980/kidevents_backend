from flask import Blueprint, jsonify, request
from db.option_db import bulk_update_tag, insert_tag, find_all_tag, find_tag_by_id, update_tag, delete_tag

tag_bp = Blueprint('tag_bp', __name__)

@tag_bp.route('/tag/create', methods=['POST'])
def create_tag():
    tag_data = request.json
    tag_data['is_enabled'] = True
    result = insert_tag(tag_data)
    return jsonify({"message": "tag created successfully", "id": str(result.inserted_id)}), 201

@tag_bp.route('/tag/list', methods=['GET'])
def get_all_tags():
    tags = find_all_tag()
    
    # 过滤掉 isEnable != True 的 tags
    tags = filter(lambda x: x.get('is_enabled', 0) == True, tags)
    
    sorted_tags = sorted(tags, key=lambda x: x.get('order', 0))
    return jsonify([{**tag, "_id": str(tag["_id"])} for tag in sorted_tags])

@tag_bp.route('/tag/<tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = find_tag_by_id(tag_id)
    if tag:
        tag['_id'] = str(tag['_id'])
        return jsonify(tag)
    return jsonify({"message": "tag not found"}), 404

@tag_bp.route('/tag/<tag_id>', methods=['PUT'])
def update_tag_route(tag_id):
    tag_data = request.json
    result = update_tag(tag_id, tag_data)
    if result.modified_count:
        return jsonify({"message": "tag updated successfully"})
    return jsonify({"message": "tag not found"}), 404

@tag_bp.route('/tag/<tag_id>', methods=['DELETE'])
def delete_tag_route(tag_id):
    result = delete_tag(tag_id)
    if result.deleted_count:
        return jsonify({"message": "tag deleted successfully"})
    return jsonify({"message": "tag not found"}), 404

@tag_bp.route('/tag/bulk-update', methods=['PUT'])
def bulk_update_tags():
    update_data = request.json
    if not isinstance(update_data, list):
        return jsonify({"message": "Invalid input. Expected a list of tag updates."}), 400

    results = bulk_update_tag(update_data)
    return jsonify({
        "message": "Bulk update completed",
    })

@tag_bp.route('/tag/online_list', methods=['GET'])
def get_online_tags():
    tags = find_all_tag()
    
    # 过滤掉 isEnable != True 的 tags
    tags = filter(lambda x: x.get('is_enabled', 0) == True, tags)
    
    sorted_tags = sorted(tags, key=lambda x: x.get('order', 0))
    
    # Return only the values of the sorted_locs dictionary
    return jsonify([tag['value'] for tag in sorted_tags])