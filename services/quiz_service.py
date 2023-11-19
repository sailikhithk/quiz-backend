from models import Quiz, Question, UserQuizMapping, Role, User
from services import QuestionService
from database import session
from sqlalchemy.orm import aliased
from sqlalchemy import desc, and_
from utils import obj_to_list, obj_to_dict
import json
import pandas as pd
import traceback
import openpyxl

question_service_obj = QuestionService()

class QuizService:
    def __init__(self):
        pass

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

    def get_all_quizzes(self):
        quiz = session.query(Quiz).all()
        response = {
            "status": True,
            "data": obj_to_list(quiz)
        }
        return response

    def get_all_quizzes_by_user_id(self, user_id):
        try:
            QuizAlias = aliased(Quiz)
            UserQuizMappingAlias = aliased(UserQuizMapping)
            result = (
                session.query(
                    Quiz.id,
                    Quiz.title,
                    Quiz.author_id,
                    Quiz.pass_marks,
                    Quiz.next_quiz_to_unlock,
                    Quiz.created_date,
                    Quiz.updated_date,
                    UserQuizMapping.id,
                    UserQuizMapping.user_id,
                    UserQuizMapping.quiz_id,
                    UserQuizMapping.no_of_attempts,
                    UserQuizMapping.is_qualified,
                    UserQuizMapping.max_scored_marks,
                    UserQuizMapping.created_date,
                    UserQuizMapping.updated_date,
                )
                .outerjoin(
                    UserQuizMappingAlias,
                    and_(
                        Quiz.id == UserQuizMappingAlias.quiz_id,
                        UserQuizMappingAlias.user_id == user_id,
                    ),
                )
                .order_by(desc(UserQuizMappingAlias.updated_date))
                .all()
            )

            quiz_results = []
            for row in result:
                quiz_data = {
                    "quiz_id": row[0],
                    "title": row[1],
                    "author_id": row[2],
                    "pass_marks": row[3],
                    "next_quiz_to_unlock": row[4],
                    "created_date_quiz": str(row[5]),  # Convert DateTime to string
                    "updated_date_quiz": str(row[6]),  # Convert DateTime to string
                    "user_quiz_mapping_id": row[7],
                    "user_id": row[8],
                    "user_quiz_id": row[9],
                    "no_of_attempts": row[10],
                    "is_qualified": row[11],
                    "max_scored_marks": row[12],
                    "created_date_mapping": str(row[13]),  # Convert DateTime to string
                    "updated_date_mapping": str(row[14]),  # Convert DateTime to string
                }
                quiz_results.append(quiz_data)

            return quiz_results
        except Exception as e:
            return []

    def get_quiz_by_id(self, quiz_id):
        quiz = session.query(Quiz).filter_by(id=quiz_id).first()
        if not quiz:
            return {"error": "Quiz not found"}
        return quiz

    def create_quiz(self, title, user_id, pass_marks, next_lessons_to_unlock):
        try:
            if not self.is_valid_admin(user_id):
                return {"message": "Invalid user try to check with admin", "status": False}
            
            serialized_next_lessons_to_unlock = json.dumps(next_lessons_to_unlock)
            new_quiz = Quiz(
                title=title,
                author_id=user_id,
                pass_marks=pass_marks,
                next_lessons_to_unlock=serialized_next_lessons_to_unlock,
            )
            session.add(new_quiz)
            session.commit()
            return {"message": "Quiz created", "id": new_quiz.id, "status": True}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": "Quiz not created", "status": False}
    
    def delete_quiz(self, quiz_id):
        try:
            quiz = session.query(Quiz).filter_by(id=quiz_id).first()
            if quiz:
                session.delete(quiz)
                session.commit()
            return {"message": "Quiz Deleted", "status": False}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": "Quiz not Deleted", "status": False}

    def combine_options(self, row):
        return [row["Option 1"], row["Option 2"], row["Option 3"], row["Option 4"]]

    def split_options(self, row):
        return pd.Series(row["options"] + [None] * (4 - len(row["options"])))

    def convert_to_bool(val):
        try:
            str_val = str(val).strip().lower()
            if str_val in ['1', 'true', True, 'True']:
                return True
            elif str_val == ['0', 'false', False, 'False']:
                return False
            else:
                return False
        except:
            return False
   
    def upsert_quiz_file(self, file, user_id, quiz_id):
        try:
            meta_data = pd.read_excel(file, engine='openpyxl', header=0, skiprows=0, nrows=4)
            meta_data_dic = dict(zip(meta_data["preference"], meta_data["value"]))
            meta_data_dic["quiz_name"] = meta_data_dic["Name"]
            existing_quiz = session.query(Quiz).filter_by(title = meta_data_dic["quiz_name"]).first()
            if existing_quiz:
                return {"message": "Quiz with same name exist", "status": False}
            
            meta_data_dic["pass_marks"] = meta_data_dic["Pass Marks"]
            meta_data_dic["next_lessons_to_unlock"] = meta_data_dic["next lessons to unlock"]
            meta_data_dic["next_lessons_to_unlock"] = meta_data_dic["next_lessons_to_unlock"].replace('"', "")
            meta_data_dic.pop("Name", None)
            meta_data_dic.pop("Pass Marks", None)
            meta_data_dic.pop("next lessons to unlock", "2")
            
            questions_df = pd.read_excel(file, header=7)
            column_mapping = {
                "Questions": "questions",
                "Correct Answers": "correct_option",
                "Marks": "marks",
                "Mandatory": "is_mandatory",
            }

            questions_df = questions_df.rename(columns=column_mapping)
            
            print("----------------------------------------")
            print("----------------------------------------")
            print("questions_df", questions_df)
            print("columns", questions_df.columns)
            print("columns", list(questions_df.columns))
            
            
            print("----------------------------------------")
            print("----------------------------------------")

            questions_df['is_mandatory'] = questions_df['is_mandatory'].apply(self.convert_to_bool)
            # questions_df["is_mandatory"] = questions_df["is_mandatory"].map(
            #     lambda x: bool(x)
            # )
            questions_df["options"] = questions_df.apply(self.combine_options, axis=1)
            questions_df["correct_option"] = questions_df["correct_option"].astype(str)
            questions_df["correct_option"] = questions_df["correct_option"].apply(
                lambda x: list(map(int, x.split(",")))
            )
            questions_df.drop(
                ["Option 1", "Option 2", "Option 3", "Option 4"], axis=1, inplace=True
            )
            questions_df["is_mandatory"] = True

            result_list = questions_df.to_dict(orient="records")

            print("result_list:", result_list)

            meta_data_dic["questions"] = result_list
            meta_data_dic["user_id"] = user_id

            if quiz_id:
                meta_data_dic["quiz_id"] = quiz_id
                pass
            else:
                return self.upload_quiz_json(meta_data_dic)
        except Exception as e:
            traceback.print_exc()
            return {"message": "Quiz not created", "status": False}

    def upload_quiz_json(self, data):
        user_id = data["user_id"]
        quiz_name = data["quiz_name"]
        questions = data["questions"]
        pass_marks = data["pass_marks"]
        next_lessons_to_unlock = data["next_lessons_to_unlock"]

        result = self.create_quiz(quiz_name, user_id, pass_marks, next_lessons_to_unlock)
        quiz_id = result.get("id", None)
        for question in questions:
            question_service_obj.create_question(question, quiz_id)
        return {"message": "Quiz uploaded"}

    def update_quiz_json(self, data):
        user_id = data["user_id"]
        quiz_name = data["quiz_name"]
        questions = data["questions"]
        pass_marks = data["pass_marks"]
        next_quiz_to_unlock = data["next_quiz_to_unlock"]
        quiz_id = data["quiz_id"]
        quiz = (
            session.query(Quiz).filter_by(id=quiz_id).first()
        )  # Fixed the filter condition here

        quiz.title = quiz_name
        quiz.pass_marks = pass_marks
        quiz.next_quiz_to_unlock = next_quiz_to_unlock
        quiz.author_id = user_id
        session.commit()

        for question in questions:
            question_service_obj.update_question(question)
        return {"message": "Quiz updated"}  # Fixed the return message here

    def download_quiz(self, quiz_id):
        quiz = session.query(Quiz).filter_by(id=quiz_id).first()
        questions = session.query(Question).filter_by(quiz_id=quiz_id).all()
        questions = obj_to_list(questions)

        quiz_dic = {
            "Name": quiz.title,
            "Total Marks": 100,
            "Pass Marks": quiz.pass_marks,
            "next lessons to unlock": quiz.next_lessons_to_unlock,
        }
        quiz_dic["next lessons to unlock"] = quiz_dic["next lessons to unlock"].replace('"', '')
        df1 = pd.DataFrame(list(quiz_dic.items()), columns=["preference", "value"])
        df2 = pd.DataFrame(questions)
        df2_normalized = pd.json_normalize(df2["content"])
        df2 = pd.concat([df2.drop(columns="content"), df2_normalized], axis=1)
        df2["correct_option"] = df2["correct_option"].apply(
            lambda x: ",".join(map(str, x))
        )
        df2[["Option 1", "Option 2", "Option 3", "Option 4"]] = df2.apply(
            self.split_options, axis=1
        )
        columns_to_drop = ["created_date", "updated_date", "options", "id"]
        df2.drop(columns=columns_to_drop, inplace=True)

        column_mapping = {
            "questions": "Questions",
            "correct_option": "Correct Answers",
            "marks": "Marks",
            "is_mandatory": "Mandatory",
        }
        df2['is_mandatory'] = df2['is_mandatory'].replace({1: 'True', 0: 'False'})
        df2 = df2.rename(columns=column_mapping)
        desired_column_order = [
            "Questions",
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Correct Answers",
            "Marks",
            "Mandatory",
            "quiz_id",
        ]
        df2 = df2[desired_column_order]
        df2 = df2.drop(df2.index[5])
        

        with pd.ExcelWriter("output.xlsx") as writer:
            df1.to_excel(writer, sheet_name="Sheet1", index=False)
            df2.to_excel(
                writer, sheet_name="Sheet1", index=False, startrow=7, startcol=0
            )

    def get_questions_by_quiz_id(self, id):
        questions = session.query(Question).filter_by(quiz_id=id).all()
        return obj_to_list(questions)

    def get_quiz(self, id):
        quiz = self.get_quiz_by_id(id)
        quiz = obj_to_dict(quiz)
        quiz["questions"] = self.get_questions_by_quiz_id(id)
        return quiz

    def deactivate_quiz(self, quiz_id):
        try:
            quiz = self.get_quiz_by_id(quiz_id)
            if quiz:
                quiz.is_active = False
                session.commit()
                return {"message": "Quiz deactivate", "status": True}
            else:
                return {"message": "Quiz not found", "status": False}            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}
        
    def activate_quiz(self, quiz_id):
        try:
            quiz = self.get_quiz_by_id(quiz_id)
            if quiz:
                quiz.is_active = True
                session.commit()
                return {"message": "Quiz activate", "status": True}
            else:
                return {"message": "Quiz not found", "status": False}            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"message": str(e), "status": False}