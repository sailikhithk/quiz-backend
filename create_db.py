from models import *
from database import session
from sqlalchemy import func
import json
import requests
import base64


def create_roles():
    print("Creating Roles")
    roles_data = ["Admin", "Teacher", "Student", "SAI"]
    query_result = (
        session.query(func.count(Role.id)).filter(Role.name.in_(roles_data)).scalar()
    )
    if query_result != len(roles_data):
        for role_name in roles_data:
            role = Role(name=role_name)
            session.add(role)
        session.commit()


def create_dummy_users():
    print("Creating dummy users")
    url = "http://localhost:5000/auth/register"

    users_data = [
        {
            "username": "harnath-a",
            "password": "harnath",
            "email": "harnath-a@gmail.com",
            "institution": "Harnath",
            "role": "Admin",
        },
        {
            "username": "harnath-s",
            "password": "harnath",
            "email": "harnath-s@gmail.com",
            "institution": "Harnath",
            "role": "Student",
        },
        {
            "username": "ramu-a",
            "password": "ramu",
            "email": "ramu-a@gmail.com",
            "institution": "Ramu",
            "role": "Admin",
        },
        {
            "username": "ramu-s",
            "password": "ramu",
            "email": "ramu-s@gmail.com",
            "institution": "Ramu",
            "role": "Student",
        },
        {
            "username": "sai-a",
            "password": "sai",
            "email": "sai-a@gmail.com",
            "institution": "Sai",
            "role": "Admin",
        },
        {
            "username": "sai-s",
            "password": "sai",
            "email": "sai-s@gmail.com",
            "institution": "Sai",
            "role": "Student",
        }
    ]
    
    headers = {
        'Content-Type': 'application/json'
        }
    for i in users_data:
        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)

def create_dummy_quizzes():
    print("Creating dummy quizzes")
    
    url = "http://localhost:5000/quiz/upsert_quiz"

    quiz_data = [
        {"user_id": "1", "file_path": "data/quiz/python basic-1.xlsx"},
        {"user_id": "1", "file_path": "data/quiz/python basic-2.xlsx"},
        {"user_id": "1", "file_path": "data/quiz/python basic-3.xlsx"},
        {"user_id": "1", "file_path": "data/quiz/python basic-4.xlsx"},
        {"user_id": "1", "file_path": "data/quiz/python basic-5.xlsx"}        
    ]
    headers = {
        'Content-Type': 'application/json'
        }
        
    
    for i in quiz_data:
        file_path = i["file_path"]
        
        with open(file_path, 'rb') as excel_file:
            excel_binary_data = excel_file.read()
            base64_data = base64.b64encode(excel_binary_data).decode()
        
        i["base64"] = str(base64_data)
        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)

def create_dummy_lesson():
    print("Creating dummy lesson")
    
    url = "http://localhost:5000/lesson/create"
    lesson_data = [
        {"title": "Python basic-1", "author_id": 1, "file_path": "data/lessons/python_intro.html", "quiz_id": 1},
        {"title": "Python basic-2", "author_id": 1, "file_path": "data/lessons/python_basic.html", "quiz_id": 2},
        {"title": "Python basic-3", "author_id": 1, "file_path": "data/lessons/python_advance.html", "quiz_id": 3},
        {"title": "Python basic-4", "author_id": 1, "file_path": "data/lessons/python_complex.html", "quiz_id": 4},
        {"title": "Python basic-5", "author_id": 1, "file_path": "data/lessons/python_complex.html", "quiz_id": 5},
    ]
    
    headers = {
        'Content-Type': 'application/json'
        }
        
    for i in lesson_data:
        html_content = ""
        file_path = i["file_path"]
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        i.pop("file_path")
        i["data"] = html_content 
        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)

def create_dummy_results():
    print("Creating dummy results")
    
    url = "http://localhost:5000/result/submit_answer"
    result_data = [
        {"user_id": 2, "quiz_id": 1, "content":[{"question_id":1,"selected_options":[3]},{"question_id":2,"selected_options":[3]},{"question_id":3,"selected_options":[2]},{"question_id":4,"selected_options":[2]},{"question_id":5,"selected_options":[2]},{"question_id":6,"selected_options":[3]},{"question_id":7,"selected_options":[4]},{"question_id":8,"selected_options":[2]},{"question_id":9,"selected_options":[3]},{"question_id":10,"selected_options":[1]},{"question_id":11,"selected_options":[4]},{"question_id":12,"selected_options":[1]},{"question_id":13,"selected_options":[1]},{"question_id":14,"selected_options":[4]},{"question_id":15,"selected_options":[3]},{"question_id":16,"selected_options":[1]},{"question_id":17,"selected_options":[1]},{"question_id":18,"selected_options":[4]},{"question_id":19,"selected_options":[4]},{"question_id":20,"selected_options":[2]},{"question_id":21,"selected_options":[2]},{"question_id":22,"selected_options":[1]},{"question_id":23,"selected_options":[2]},{"question_id":24,"selected_options":[4]},{"question_id":25,"selected_options":[1]}]},
        {"user_id": 2, "quiz_id": 1, "content":[{"question_id":1,"selected_options":[2]},{"question_id":2,"selected_options":[4]},{"question_id":3,"selected_options":[4]},{"question_id":4,"selected_options":[1]},{"question_id":5,"selected_options":[1]},{"question_id":6,"selected_options":[2]},{"question_id":7,"selected_options":[2]},{"question_id":8,"selected_options":[1]},{"question_id":9,"selected_options":[2]},{"question_id":10,"selected_options":[4]},{"question_id":11,"selected_options":[4]},{"question_id":12,"selected_options":[1]},{"question_id":13,"selected_options":[1]},{"question_id":14,"selected_options":[4]},{"question_id":15,"selected_options":[3]},{"question_id":16,"selected_options":[1]},{"question_id":17,"selected_options":[1]},{"question_id":18,"selected_options":[4]},{"question_id":19,"selected_options":[4]},{"question_id":20,"selected_options":[2]},{"question_id":21,"selected_options":[2]},{"question_id":22,"selected_options":[1]},{"question_id":23,"selected_options":[2]},{"question_id":24,"selected_options":[4]},{"question_id":25,"selected_options":[1]}]},
        {"user_id": 4, "quiz_id": 1, "content":[{"question_id":1,"selected_options":[3]},{"question_id":2,"selected_options":[3]},{"question_id":3,"selected_options":[2]},{"question_id":4,"selected_options":[2]},{"question_id":5,"selected_options":[2]},{"question_id":6,"selected_options":[3]},{"question_id":7,"selected_options":[4]},{"question_id":8,"selected_options":[2]},{"question_id":9,"selected_options":[3]},{"question_id":10,"selected_options":[1]},{"question_id":11,"selected_options":[4]},{"question_id":12,"selected_options":[1]},{"question_id":13,"selected_options":[1]},{"question_id":14,"selected_options":[4]},{"question_id":15,"selected_options":[3]},{"question_id":16,"selected_options":[1]},{"question_id":17,"selected_options":[1]},{"question_id":18,"selected_options":[4]},{"question_id":19,"selected_options":[4]},{"question_id":20,"selected_options":[2]},{"question_id":21,"selected_options":[2]},{"question_id":22,"selected_options":[1]},{"question_id":23,"selected_options":[2]},{"question_id":24,"selected_options":[4]},{"question_id":25,"selected_options":[1]}]},
        {"user_id": 4, "quiz_id": 1, "content":[{"question_id":1,"selected_options":[2]},{"question_id":2,"selected_options":[4]},{"question_id":3,"selected_options":[4]},{"question_id":4,"selected_options":[1]},{"question_id":5,"selected_options":[1]},{"question_id":6,"selected_options":[2]},{"question_id":7,"selected_options":[2]},{"question_id":8,"selected_options":[1]},{"question_id":9,"selected_options":[2]},{"question_id":10,"selected_options":[4]},{"question_id":11,"selected_options":[4]},{"question_id":12,"selected_options":[1]},{"question_id":13,"selected_options":[1]},{"question_id":14,"selected_options":[4]},{"question_id":15,"selected_options":[3]},{"question_id":16,"selected_options":[1]},{"question_id":17,"selected_options":[1]},{"question_id":18,"selected_options":[4]},{"question_id":19,"selected_options":[4]},{"question_id":20,"selected_options":[2]},{"question_id":21,"selected_options":[2]},{"question_id":22,"selected_options":[1]},{"question_id":23,"selected_options":[2]},{"question_id":24,"selected_options":[4]},{"question_id":25,"selected_options":[1]}]},
        {"user_id": 6, "quiz_id": 1, "content":[{"question_id":1,"selected_options":[3]},{"question_id":2,"selected_options":[3]},{"question_id":3,"selected_options":[2]},{"question_id":4,"selected_options":[2]},{"question_id":5,"selected_options":[2]},{"question_id":6,"selected_options":[3]},{"question_id":7,"selected_options":[4]},{"question_id":8,"selected_options":[2]},{"question_id":9,"selected_options":[3]},{"question_id":10,"selected_options":[1]},{"question_id":11,"selected_options":[4]},{"question_id":12,"selected_options":[1]},{"question_id":13,"selected_options":[1]},{"question_id":14,"selected_options":[4]},{"question_id":15,"selected_options":[3]},{"question_id":16,"selected_options":[1]},{"question_id":17,"selected_options":[1]},{"question_id":18,"selected_options":[4]},{"question_id":19,"selected_options":[4]},{"question_id":20,"selected_options":[2]},{"question_id":21,"selected_options":[2]},{"question_id":22,"selected_options":[1]},{"question_id":23,"selected_options":[2]},{"question_id":24,"selected_options":[4]},{"question_id":25,"selected_options":[1]}]},
        {"user_id": 6, "quiz_id": 1, "content":[{"question_id":1,"selected_options":[2]},{"question_id":2,"selected_options":[4]},{"question_id":3,"selected_options":[4]},{"question_id":4,"selected_options":[1]},{"question_id":5,"selected_options":[1]},{"question_id":6,"selected_options":[2]},{"question_id":7,"selected_options":[2]},{"question_id":8,"selected_options":[1]},{"question_id":9,"selected_options":[2]},{"question_id":10,"selected_options":[4]},{"question_id":11,"selected_options":[4]},{"question_id":12,"selected_options":[1]},{"question_id":13,"selected_options":[1]},{"question_id":14,"selected_options":[4]},{"question_id":15,"selected_options":[3]},{"question_id":16,"selected_options":[1]},{"question_id":17,"selected_options":[1]},{"question_id":18,"selected_options":[4]},{"question_id":19,"selected_options":[4]},{"question_id":20,"selected_options":[2]},{"question_id":21,"selected_options":[2]},{"question_id":22,"selected_options":[1]},{"question_id":23,"selected_options":[2]},{"question_id":24,"selected_options":[4]},{"question_id":25,"selected_options":[1]}]}
    ]
    
    headers = {
    'Content-Type': 'application/json'
    }

    for i in result_data:
        response = requests.request("POST", url, headers=headers, data=json.dumps(i))
        print(response.text)