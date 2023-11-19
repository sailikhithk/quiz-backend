from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()


# Database URL configuration
# DATABASE_URL = "sqlite:///app.db"

SQL_HOST = os.environ.get("SQL_HOST")
SQL_PORT = os.environ.get("SQL_PORT")
SQL_DB_NAME = os.environ.get("SQL_DB_NAME")
SQL_DB_PASSWORD = os.environ.get("SQL_DB_PASSWORD")
SQL_USER_NAME = os.environ.get("SQL_USER_NAME")

DATABASE_URL = f"postgresql://{SQL_USER_NAME}:{SQL_DB_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()
