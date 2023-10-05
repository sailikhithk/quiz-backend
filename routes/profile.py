from flask import Blueprint, request, jsonify
from services.profile_service import ProfileService

profile = Blueprint("profile", __name__)
profile_service = ProfileService()


def profile_to_dict(profile):
    return {c.name: getattr(profile, c.name) for c in profile.__table__.columns}


@profile.route("/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    profile_obj = profile_service.get_profile(user_id)
    if profile_obj:
        return jsonify(profile_to_dict(profile_obj)), 200
    else:
        return jsonify({"error": "Profile not found"}), 404


@profile.route("/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.json
    updated_profile = profile_service.update_profile(user_id, data)
    if updated_profile:
        return jsonify(profile_to_dict(updated_profile)), 200
    else:
        return jsonify({"error": "Failed to update profile"}), 400
