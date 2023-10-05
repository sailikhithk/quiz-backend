from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL configuration
DATABASE_URL = "sqlite:///app.db"

# Create an engine instance using the configured DATABASE_URL
# The engine is the starting point for any SQLAlchemy application.
engine = create_engine(DATABASE_URL)

# Create a declarative base instance
# The declarative base class serves as a catalog of classes that can be mapped to a relational database.
Base = declarative_base()

# Create a sessionmaker factory
# The sessionmaker factory is used to create Session objects, which are the source of all ORM operations.
Session = sessionmaker(bind=engine)

# Create a Session instance
# The session object allows you to add, update, delete, and query objects using SQLAlchemy ORM.
session = Session()
