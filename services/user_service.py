import traceback
import os
from flask_jwt_extended import create_access_token

from models import User, Role, Quiz, Result
from utils import encrypt, decrypt, obj_to_list, obj_to_dict
from database import session
from sqlalchemy import desc
from email_utils import send_email
from dotenv import load_dotenv
load_dotenv()

UI_SERVER_URL = os.environ.get("UI_SERVER_URL")
EMAIL_USERNAME = os.environ.get("GOOGLE_EMAIL_USERNAME")

class UserService:
    def __init__(self):
        pass

    def get_user_by_id(self, user_id):
        return session.query(User).filter_by(id=user_id).first()

    def get_user_by_username(self, username):
        return session.query(User).filter_by(username = username).first()

    def get_user_by_email(self, email):
        return session.query(User).filter_by(email = email).first()

    def create_user(self, username, password, email, institution, role_id):
        try:
            hashed_password = encrypt(password)
            new_user = User(
                username=username,
                password_hash=hashed_password,
                email=email,
                institution=institution,
                role_id=role_id,
            )
            session.add(new_user)
            session.commit()
            return new_user
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}
    
    
    def update_user(self, user_id, update_data):
        user = session.query(User).get(user_id)
        if user:
            for key, value in update_data.items():
                if key == "password":
                    value = encrypt(value)
                    key = "hashed_password"
                setattr(user, key, value)  
            session.commit()
        user_dic = obj_to_dict(user)
        return user_dic
    
    def deactivate_user(self, user_id):
        try:
            user = self.get_user_by_id(user_id)
            if user:
                user.is_active = False
                session.commit()
                return {"message": "User deactivate", "status": True}
            else:
                return {"message": "User not found", "status": False}            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}
        
    def activate_user(self, user_id):
        try:
            user = self.get_user_by_id(user_id)
            if user:
                user.is_active = True
                session.commit()
                return {"message": "User activate", "status": True}
            else:
                return {"message": "User not found", "status": False}            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}
    
    def register_user(self, data):
        try:
            username = data["username"]
            password = data["password"]
            email = data["email"]
            institution = data["institution"]
            role_name = data["role"]

            role = session.query(Role).filter_by(name=role_name).first()
            if role is None:
                return {"error": f"Role '{role_name}' not found."}
            role_id = role.id
            
            existing_user = self.get_user_by_email(email)
            if existing_user:
                return {"message": "User with same email exist", "status": False}
            
            
            user = self.create_user(username, password, email, institution, role_id)
            if user:
                email_values = {
                    "user_name": user.username,
                    "institution_name": user.institution,
                    "password": password,
                    "login_url": UI_SERVER_URL    
                }
                send_email("register.html",email, "Registered", email_values)
                return {"message": "User created plese re-login from login page", "status": True}
            else:
                return {"message": "User not created", "status": False}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}

    def login_user(self, data):
        try:
            user_name = data["username"]
            password = data["password"]
            user = self.get_user_by_username(user_name)
            if not user:
                return {"message": "Invalid username or password", "status": False}

            if not user.is_active:
                return {"message": "username deactivated pls contact Admin", "status": False}

            hashpwd = user.password_hash
            db_password = decrypt(hashpwd)

            if db_password == password:
                user_data = {
                    "user_name": user.username,
                    "email": user.email,
                    "institution": user.institution,
                    "role_id": user.role_id,
                    "user_id": user.id,
                }
                access_token = create_access_token(identity=user_data)
                return {"data": user_data, "message": "Login success", "access_token": access_token , "status": True}
            else:
                return {"message": "Invalid username or password", "status": False}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}

    def reset_password(self, data):
        try:
            password = data["new_password"]
            email = data["email"]

            hashed_password = encrypt(password)
            user = self.get_user_by_email(email)
            if not user:
                return {"message": "Invalid email", "status": False}    
            user.password_hash = hashed_password
            session.commit()
            return {"message": "Password updated, relogin again", "status": True}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}

    def is_valid_admin(self, user_id):
        try:
            admin_role = session.query(Role).filter_by(name="Admin").first()
            if admin_role:
                admin_id = admin_role.id
            else:
                return False
            user = session.query(User).filter_by(id=user_id).filter_by(role_id=admin_id)
            if user:
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return False
        
    def user_list(self):
        users = session.query(User).all()
        return obj_to_list(users)
    
    def admin_statistics_calculation(self):
        try:
            pass_percentage_vs_quiz = []
            avg_attemps_vs_quiz = []
            students_qulified_vs_quiz = []

            quiz_list = session.query(Quiz).all()
            for quiz in quiz_list:
                temp_dict = {}
                quiz_id = quiz.id
                temp_dict["name"] = quiz.title
                passed_results = session.query(Result).filter_by(quiz_id = quiz_id).filter_by(is_qualified = True).count()
                if passed_results is None:
                    passed_results = 0
                
                failed_results = session.query(Result).filter_by(quiz_id = quiz_id).filter_by(is_qualified = False).count()
                if failed_results is None:
                    failed_results = 0

                try:
                    percentage = (passed_results / (passed_results + failed_results)) * 100    
                except:
                    percentage = 0

                temp_dict["value"] = percentage
                pass_percentage_vs_quiz.append(temp_dict)

                temp_dict = {}
                temp_dict["name"] = quiz.title
                qualified_count = session.query(Result).filter_by(is_qualified=True).filter_by(quiz_id = quiz_id).count()
                unique_user_count = session.query(Result.user_id).filter_by(is_qualified=True).filter_by(quiz_id = quiz_id).distinct().count()
                try:
                    avg_attemps = qualified_count/unique_user_count
                except:
                    avg_attemps = 0
                temp_dict["value"] = avg_attemps
                avg_attemps_vs_quiz.append(temp_dict)


                temp_dict = {}
                temp_dict["name"] = quiz.title
                temp_dict["value"] = unique_user_count
                students_qulified_vs_quiz.append(temp_dict)
                
            return pass_percentage_vs_quiz, avg_attemps_vs_quiz, students_qulified_vs_quiz
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return [],[],[]
    
    def admin_statistics(self):
        try:
            response = {
                "cards": [],
                "graphs": []
            }
            total_no_of_quiz = session.query(Quiz).count()
            active_quiz = session.query(Quiz).filter_by(is_active = True).count()
            if active_quiz is None:
                active_quiz = 0
            in_active_quiz = session.query(Quiz).filter_by(is_active = False).count()
            if in_active_quiz is None:
                in_active_quiz = 0
            
            total_no_of_user = session.query(User).count()
            active_user = session.query(User).filter_by(is_active = True).count()
            if active_user is None:
                active_user = 0
            in_active_user = session.query(User).filter_by(is_active = False).count()
            if in_active_user is None:
                in_active_user = 0
            
            card_1 = {
                "name": "Number of Quiz",
                "value": total_no_of_quiz,
                "sub_values": {
                    "active": active_quiz,
                    "in_active_quiz": in_active_quiz,
                }
            }
            card_2 = {
                "name": "Number of Users",
                "value": total_no_of_user,
                "sub_values": {
                    "active": active_user,
                    "in_active_quiz": in_active_user,
                }
            }
            
            response["cards"] = [card_1, card_2] 
            
            # MOCK DATA
            # graph_1 = {
            #     "name": "Pass percentage Vs Quiz",
            #     "data": [
            #         { "name": 'Quiz 1', "value": 100 },
            #         { "name": 'Quiz 2', "value": 15 },
            #         { "name": 'Quiz 3', "value": 80 },
            #         { "name": 'Quiz 4', "value": 20 },
            #         { "name": 'Quiz 5', "value": 65 },
            #     ] 
            # }
            # graph_2 = {
            #     "name": "Avg no.of attemps Vs Quiz",
            #     "data": [
            #         { "name": 'Quiz 1', "value": 1 },
            #         { "name": 'Quiz 2', "value": 2 },
            #         { "name": 'Quiz 3', "value": 1 },
            #         { "name": 'Quiz 4', "value": 4 },
            #         { "name": 'Quiz 5', "value": 3 },
            #     ] 
            # }

            # graph_3 = {
            #     "name": "No.of students Qulified Vs Quiz",
            #     "data": [
            #         { "name": 'Quiz 1', "value": 10 },
            #         { "name": 'Quiz 2', "value": 3 },
            #         { "name": 'Quiz 3', "value": 7 },
            #         { "name": 'Quiz 4', "value": 4 },
            #         { "name": 'Quiz 5', "value": 3 },
            #     ] 
            # }

            graph_1_data, graph_2_data, graph_3_data = self.admin_statistics_calculation()
            
            graph_1 = {
                "name": "Pass percentage Vs Quiz",
                "data": graph_1_data
            }
            graph_2 = {
                "name": "Avg no.of attemps Vs Quiz",
                "data": graph_2_data
            }

            graph_3 = {
                "name": "No.of students Qulified Vs Quiz",
                "data":  graph_3_data
            }

            response["graphs"] = [graph_1, graph_2, graph_3]
            return {"status": True, "data": response}

        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return False

    def user_statistics_calculation(self, user_id):
        try:
            percentage_of_marks_scored_vs_quiz_user_graph = []
            attemps_to_qualify_vs_quiz = []
            
            quiz_list = session.query(Quiz).all()
            for quiz in quiz_list:
                temp_dict = {}
                quiz_id = quiz.id
                total_marks = quiz.total_marks
                temp_dict["name"] = quiz.title
                max_result = session.query(Result).filter_by(quiz_id=quiz_id).filter_by(user_id=user_id).order_by(desc(Result.score)).first()
                if max_result is None:
                    temp_dict["value"] = 0 
                else:
                    max_scored_marks = max_result.score
                    try:
                        percentage = (max_scored_marks / total_marks) * 100
                    except:
                        percentage = 0

                    temp_dict["value"] = percentage
                percentage_of_marks_scored_vs_quiz_user_graph.append(temp_dict)

                temp_dict = {}
                temp_dict["name"] = quiz.title
                
                attempts_count = session.query(Result).filter_by(quiz_id=quiz_id).filter_by(user_id=user_id).count()
                if max_result is attempts_count:
                    temp_dict["value"] = 0 
                else:
                    temp_dict["value"] = attempts_count
                attemps_to_qualify_vs_quiz.append(temp_dict)

            return percentage_of_marks_scored_vs_quiz_user_graph, attemps_to_qualify_vs_quiz
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return [],[]

    

    def user_statistics(self, user_id):
        try:
            response = {
                "cards": [],
                "graphs": []
            }
            total_no_of_quiz = session.query(Quiz).count()
            active_quiz = session.query(Quiz).filter_by(is_active = True).count()
            if active_quiz is None:
                active_quiz = 0
            
            in_active_quiz = session.query(Quiz).filter_by(is_active = False).count()
            if in_active_quiz is None:
                in_active_quiz = 0
            
            total_no_of_user = session.query(User).count()
            active_user = session.query(User).filter_by(is_active = True).count()
            if active_user is None:
                active_user = 0
            in_active_user = session.query(User).filter_by(is_active = False).count()
            if in_active_user is None:
                in_active_user = 0
            
            card_1 = {
                "name": "Number of Quiz",
                "value": total_no_of_quiz,
                "sub_values": {
                    "active": active_quiz,
                    "in_active_quiz": in_active_quiz,
                }
            }
            card_2 = {
                "name": "Number of Users",
                "value": total_no_of_user,
                "sub_values": {
                    "active": active_user,
                    "in_active_quiz": in_active_user,
                }
            }
            
            response["cards"] = [card_1, card_2] 
            
            # MOCK DATA
            # graph_1 = {
            #     "name": "Percentage of marks scored Vs Quiz",
            #     "data": [
            #         { "name": 'Quiz 1', "value": 100 },
            #         { "name": 'Quiz 2', "value": 15 },
            #         { "name": 'Quiz 3', "value": 80 },
            #         { "name": 'Quiz 4', "value": 70 },
            #         { "name": 'Quiz 5', "value": 65 },
            #     ] 
            # }
            # graph_2 = {
            #     "name": "No.of attemps to qualify Vs Quiz",
            #     "data": [
            #         { "name": 'Quiz 1', "value": 1 },
            #         { "name": 'Quiz 2', "value": 2 },
            #         { "name": 'Quiz 3', "value": 1 },
            #         { "name": 'Quiz 4', "value": 4 },
            #         { "name": 'Quiz 5', "value": 3 },
            #     ] 
            # }
            
            
            graph_1_data, graph_2_data = self.user_statistics_calculation(user_id)

            
            
            graph_1 = {
                "name": "Percentage of marks scored Vs Quiz",
                "data": graph_1_data
            }
            graph_2 = {
                "name": "No.of attemps to qualify Vs Quiz",
                "data": graph_2_data
            }
            
            response["graphs"] = [graph_1, graph_2]
            return {"status": True, "data": response}

        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return False