from models import Question
from database import session
from utils import obj_to_list, obj_to_dict


class QuestionService:
    def __init__(self):
        pass

    def get_all_questions(self):
        return self.question_repository.get_all_questions()

    def get_question_by_id(self, question_id):
        question = session.query(Question).filter_by(id=question_id).first()
        if not question:
            return {"error": "Question not found"}
        return obj_to_dict(question)

    def create_question(self, content, quiz_id):
        new_question = Question(content=content, quiz_id=quiz_id)
        session.add(new_question)
        session.commit()
        return {"message": "Question created"}

    def update_question(self, content):
        question_id = content['id']
        content.pop('id', None)
        question = session.query(Question).filter_by(id=question_id).first()
        if question:
            question.content = content
            session.commit()
        return question

    def delete_question(self, question_id):
        question = session.query(Question).filter_by(id=question_id).first()
        if question:
            session.delete(question)
            session.commit()
        return {"message": "Question Deleted"}