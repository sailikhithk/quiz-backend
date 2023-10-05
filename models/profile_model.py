# models/profile_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)  # Adding email field
    photo = Column(String)  # Assuming photo is stored as a URL or file path
    first_name = Column(String)  # First name
    last_name = Column(String)  # Last name
    bio = Column(String)  # Short bio or description

    def __repr__(self):
        return f"<Profile {self.username}>"
