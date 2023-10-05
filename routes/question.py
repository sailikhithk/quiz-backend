import logging
import traceback

from flask import Blueprint, request, jsonify
from services.question_service import QuestionService
from flask_jwt_extended import jwt_required, get_jwt_identity

question = Blueprint("question", __name__)
logger = logging.getLogger("question")

question_service_obj = QuestionService()


@question.route("/<int:id>/get_question", methods=["GET"])
def get_question(id):
    try:
        question = question_service_obj.get_question_by_id(id)
        if not question:
            return jsonify({"error": "Question not found"}), 404
        return jsonify(question)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@question.route("/<int:id>/delete_question", methods=["GET"])
def delete_question(id):
    try:
        question = question_service_obj.delete_question(id)
        if not question:
            return jsonify({"error": "Question not found"}), 404
        return jsonify(question)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
