from flask import Blueprint, jsonify, request
from db.option_db import bulk_update_loc, insert_loc, find_all_loc, find_loc_by_id, update_loc, delete_loc

loc_bp = Blueprint('loc_bp', __name__)

@loc_bp.route('/loc/create', methods=['POST'])
def create_loc():
    loc_data = request.json
    loc_data['isEnable'] = 1
    result = insert_loc(loc_data)
    return jsonify({"message": "Location created successfully", "id": str(result.inserted_id)}), 201

@loc_bp.route('/loc/list', methods=['GET'])
def get_all_locs():
    locs = find_all_loc()
    sorted_locs = sorted(locs, key=lambda x: x.get('order', 0))
    return jsonify([{**loc, "_id": str(loc["_id"])} for loc in sorted_locs])

@loc_bp.route('/loc/<loc_id>', methods=['GET'])
def get_loc(loc_id):
    loc = find_loc_by_id(loc_id)
    if loc:
        loc['_id'] = str(loc['_id'])
        return jsonify(loc)
    return jsonify({"message": "Location not found"}), 404

@loc_bp.route('/loc/<loc_id>', methods=['PUT'])
def update_loc_route(loc_id):
    loc_data = request.json
    result = update_loc(loc_id, loc_data)
    if result.modified_count:
        return jsonify({"message": "Location updated successfully"})
    return jsonify({"message": "Location not found"}), 404

@loc_bp.route('/loc/<loc_id>', methods=['DELETE'])
def delete_loc_route(loc_id):
    result = delete_loc(loc_id)
    if result.deleted_count:
        return jsonify({"message": "Location deleted successfully"})
    return jsonify({"message": "Location not found"}), 404

@loc_bp.route('/loc/bulk-update', methods=['PUT'])
def bulk_update_locs():
    update_data = request.json
    if not isinstance(update_data, list):
        return jsonify({"message": "Invalid input. Expected a list of location updates."}), 400

    results = bulk_update_loc(update_data)
    return jsonify({
        "message": "Bulk update completed",
    })