from flask import Blueprint, jsonify, request
from db.option_db import insert_tag, find_all_tag, find_tag_by_id, update_tag, delete_tag

tag_bp = Blueprint('tag_bp', __name__)

@tag_bp.route('/tag', methods=['POST'])
def create_tag():
    tag_data = request.json
    result = insert_tag(tag_data)
    return jsonify({"message": "Tag created successfully", "id": str(result.inserted_id)}), 201

@tag_bp.route('/tag', methods=['GET'])
def get_all_tags():
    tags = find_all_tag()
    return jsonify([{**tag, "_id": str(tag["_id"])} for tag in tags])

@tag_bp.route('/tag/<tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = find_tag_by_id(tag_id)
    if tag:
        tag['_id'] = str(tag['_id'])
        return jsonify(tag)
    return jsonify({"message": "Tag not found"}), 404

@tag_bp.route('/tag/<tag_id>', methods=['PUT'])
def update_tag_route(tag_id):
    tag_data = request.json
    result = update_tag(tag_id, tag_data)
    if result.modified_count:
        return jsonify({"message": "Tag updated successfully"})
    return jsonify({"message": "Tag not found"}), 404

@tag_bp.route('/tag/<tag_id>', methods=['DELETE'])
def delete_tag_route(tag_id):
    result = delete_tag(tag_id)
    if result.deleted_count:
        return jsonify({"message": "Tag deleted successfully"})
    return jsonify({"message": "Tag not found"}), 404