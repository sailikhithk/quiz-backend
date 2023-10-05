import logging
import traceback

from flask import Blueprint, request, jsonify
from jsonschema import validate
from services import LessonService

from validation import UPDATE_LESSON_SCHEMA, CREATE_LESSON_SCHEMA
lesson = Blueprint("lesson", __name__)
logger = logging.getLogger("lesson")

lesson_service_obj = LessonService()

@lesson.route("/create", methods=["POST"])
def create():
    try:
        data = request.get_json()
        validate(data, CREATE_LESSON_SCHEMA)    
        response = lesson_service_obj.create_lesson(data)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@lesson.route("/update", methods=["POST"])
def update():
    try:
        data = request.get_json()
        validate(data, UPDATE_LESSON_SCHEMA)    
        response = lesson_service_obj.update_lesson(data)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@lesson.route("/<int:lesson_id>/get", methods=["GET"])
def get(lesson_id):
    try:
        response = lesson_service_obj.get_lesson(lesson_id)
        return jsonify(response)
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@lesson.route("/full_list", methods=["GET"])
def full_list():
    try:
        response = lesson_service_obj.full_list()
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@lesson.route("/<int:user_id>/list", methods=["GET"])
def list(user_id):
    try:
        response = lesson_service_obj.list_lesson(user_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@lesson.route("/<int:lesson_id>/delete", methods=["DELETE"])
def delete(lesson_id):
    try:
        response = lesson_service_obj.delete_lesson(lesson_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@lesson.route("/<int:lesson_id>/deactivate", methods=["POST"])
def deactivate(lesson_id):
    try:
        response = lesson_service_obj.deactivate(lesson_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@lesson.route("/<int:lesson_id>/activate", methods=["POST"])
def activate(lesson_id):
    try:
        response = lesson_service_obj.activate(lesson_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500