import logging
import traceback

from flask import Blueprint, request, jsonify
from jsonschema import validate
from services import UserService
from validation import REGISTER_SCHEMA, LOGIN_SCHEMA, RESET_PASSWORD_SCHEMA, ADMIN_CREATE_USER_SCHEMA, UPDATE_USER_SCHEMA
user = Blueprint("user", __name__)
logger = logging.getLogger("user")
# logger.info('Login page accessed')

user_service_obj = UserService()


@user.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        validate(data, LOGIN_SCHEMA)    
        response = user_service_obj.login_user(data)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@user.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        validate(data, REGISTER_SCHEMA)    
        response = user_service_obj.register_user(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user.route("/create_user", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        validate(data, ADMIN_CREATE_USER_SCHEMA)
        user_id = data["user_id"]
        if user_service_obj.is_valid_admin(user_id):
            response = user_service_obj.register_user(data)
            return jsonify(response)
        else:
            return jsonify({"errror": "Invalid Admin"}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user.route("/update_user", methods=["POST"])
def update_user():
    try:
        data = request.get_json()
        validate(data, UPDATE_USER_SCHEMA)
        user_id = data["user_id"]
        data.pop("user_id", None)
        response = user_service_obj.update_user(user_id, data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user.route("/reset_password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        validate(data, RESET_PASSWORD_SCHEMA)
        response = user_service_obj.reset_password(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user.route("/<int:user_id>/deactivate", methods=["GET"])
def deactivate(user_id):
    try:
        response = user_service_obj.deactivate_user(user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user.route("/<int:user_id>/activate", methods=["GET"])
def activate(user_id):
    try:
        response = user_service_obj.activate_user(user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@user.route("/user_list", methods=["GET"])
def user_list():
    try:
        response = user_service_obj.user_list()
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

@user.route("/<int:user_id>/statistics", methods=["GET"])
def user_statistics(user_id):
    try:
        response = user_service_obj.user_statistics(user_id)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@user.route("/admin_statistics", methods=["GET"])
def admin_statistics():
    try:
        response = user_service_obj.admin_statistics()
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500