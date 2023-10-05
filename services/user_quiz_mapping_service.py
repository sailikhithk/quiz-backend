from database import session
from models import UserQuizMapping
from utils import obj_to_dict

class UserQuizMappingService:
    def __init__(self):
        pass

    def get_record(self,user_id,quiz_id):
        record = session.query(UserQuizMapping).filter_by(user_id=user_id).filter_by(quiz_id=quiz_id).first()
        if not record:
            return {}
        return obj_to_dict(record)

    def update_record(self, update_dic, user_id, quiz_id):
        record = session.query(UserQuizMapping).filter_by(user_id=user_id).filter_by(quiz_id=quiz_id).first()
        for column, value in update_dic.items():
            setattr(record, column, value)

        session.commit()
        return record.id
    
    def create_record(self, user_id, quiz_id, is_qualified, max_scored_marks):
        new_result = UserQuizMapping(
            user_id = user_id,
            quiz_id = quiz_id,
            no_of_attempts = 1,
            is_qualified = is_qualified,
            max_scored_marks = max_scored_marks
        )
        session.add(new_result)
        session.commit()
        return  new_result.id  
