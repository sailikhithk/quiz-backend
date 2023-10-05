REGISTER_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "institution": {"type": "string"},
        "role": {"type": "string", "enum": ["Admin", "Teacher", "Student"]},
    },
    "required": ["username", "password", "email", "institution", "role"],
}

UPDATE_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "institution": {"type": "string"},
        "user_id": {"type": "integer"}
    },
    "required": ["user_id"]
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}

RESET_PASSWORD_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "new_password": {"type": "string"}
    },
    "required": ["email", "new_password"]
}

ADMIN_CREATE_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "institution": {"type": "string"},
        "role": {"type": "string", "enum": ["Admin", "Teacher", "Student"]},
    },
    "required": ["username", "password", "email", "institution", "role"],
}


UPLOAD_QUIZ_SCHEMA = {
  "type": "object",
  "properties": {
    "user_id": {"type": "integer"},
    "quiz_name": {
      "type": "string"
    },
    "questions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "question": {
            "type": "string"
          },
          "is_multichoice": {
            "type": "boolean"
          },
          "options": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "correct_option": {
            "type": "array",
            "items": {
              "type": "integer"
            }
          },
          "is_mandatory": {
            "type": "boolean"
          },
          "marks": {
            "type": "integer"
          }
        },
        "required": ["question", "is_multichoice", "options", "correct_option", "is_mandatory", "marks"]
      }
    },
    "pass_marks": {
      "type": "integer"
    },
    "next_quiz_to_unlock": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    }
  },
  "required": ["quiz_name", "questions", "pass_marks", "next_quiz_to_unlock"]
}


SUBMIT_ANSWER_SCHEMA = {
  "type": "object",
  "properties": {
    "user_id": {"type": "integer"},
    "quiz_id": {
      "type": "integer"
    },
    "content": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "question_id": {
            "type": "integer"
          },
          "selected_options": {
            "type": "array",
            "items": {
              "type": "integer"
            }
          }
        },
        "required": ["question_id", "selected_options"]
      }
    }
  },
  "required": ["quiz_id", "content"]
}

CREATE_LESSON_SCHEMA = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "author_id": {"type": "integer"},
    "file_path": {"type": "string"},
    "quiz_id": {"type": "integer"},
  },
  "required": ["title", "author_id", "file_path", "quiz_id"]
}

UPDATE_LESSON_SCHEMA = {
  "type": "object",
  "properties": {
    "lesson_id": {"type": "integer"},
    "title": {"type": "string"},
    "file_path": {"type": "string"},
    "quiz_id": {"type": "integer"},
  },
  "required": ["lesson_id"]
}