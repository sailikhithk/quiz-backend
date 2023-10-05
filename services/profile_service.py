# services/profile_service.py
from database import session
from models.profile_model import Profile


class ProfileService:
    def __init__(self):
        pass
    
    def get_profile(self, user_id):
        profile = session.query(Profile).filter_by(user_id=user_id).first()
        return profile

    def update_profile(self, user_id, data):
        profile = session.query(Profile).filter_by(user_id=user_id).first()
        for key, value in data.items():
            setattr(profile, key, value)
        session.commit()
        return profile
