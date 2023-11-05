import logging
import traceback
import pandas
import io
import openpyxl
import base64


from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema import validate

from services import QuestionService, QuizService
from validation import UPLOAD_QUIZ_SCHEMA

quiz = Blueprint("quiz", __name__)
logger = logging.getLogger("auth")

question_service_obj = QuestionService()
quiz_service_obj = QuizService()


@quiz.route("/<int:user_id>/list", methods=["GET"])
def get_all_quizzes(user_id):
    """
    Endpoint to fetch all quizzes for a specific user.
    Sample input URL: /quiz/1/list

    :param user_id: ID of the user
    :return: JSON object containing quizzes
    """
    try:
        quizzes = quiz_service_obj.get_all_quizzes_by_user_id(user_id)
        return jsonify(quizzes), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@quiz.route("/full_list", methods=["GET"])
def get_full_list():
    try:
        quizzes = quiz_service_obj.get_all_quizzes()
        return jsonify(quizzes), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@quiz.route("/upsert_quiz", methods=["POST"])
def upload_quiz():
    """
    Endpoint to upload or update a quiz.
    Sample input JSON:
    {
        "file": file_object,
        "user_id": 1,
        "quiz_id": 2
    }

    :return: JSON object with response message
    """
    try:
        data = request.get_json()
        if 'base64' in data:
            # file upload approch
            user_id = data.get("user_id", None)
            quiz_id = data.get("quiz_id", None)
            file_data = base64.b64decode(data['base64'])
            file_data_name = f'user_bulk_upload.xlsx'
            
            with open(file_data_name, 'wb') as excel_file:
                excel_file.write(file_data)

            response = quiz_service_obj.upsert_quiz_file(file_data_name, user_id, quiz_id)
        else:
            validate(data, UPLOAD_QUIZ_SCHEMA)
            response = quiz_service_obj.upload_quiz_json(data)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@quiz.route("/<int:quiz_id>/download_quiz", methods=["GET"])
def download_quiz(quiz_id):
    """
    Endpoint to download a quiz in Excel format.
    Sample input URL: /quiz/1/download_quiz

    :param quiz_id: ID of the quiz
    :return: Excel file for download
    """
    try:
        quiz_service_obj.download_quiz(quiz_id)
        return send_file("output.xlsx", as_attachment=True)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@quiz.route("/<int:quiz_id>/questions", methods=["GET"])
def get_quiz(quiz_id):
    """
    Endpoint to fetch questions for a specific quiz.
    Sample input URL: /quiz/1/questions

    :param quiz_id: ID of the quiz
    :return: JSON object containing questions
    """
    try:
        response = quiz_service_obj.get_quiz(quiz_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@quiz.route("/<int:quiz_id>/delete_quiz", methods=["GET"])
def delete_quiz(quiz_id):
    """
    Endpoint to delete a specific quiz.
    Sample input URL: /quiz/1/delete_quiz

    :param quiz_id: ID of the quiz
    :return: JSON object with response message
    """
    try:
        response = quiz_service_obj.delete_quiz(quiz_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@quiz.route("/<int:quiz_id>/deactivate", methods=["Get"])
def deactivate(quiz_id):
    try:
        response = quiz_service_obj.deactivate_quiz(quiz_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@quiz.route("/<int:quiz_id>/activate", methods=["GET"])
def activate(quiz_id):
    try:
        response = quiz_service_obj.activate_quiz(quiz_id)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500