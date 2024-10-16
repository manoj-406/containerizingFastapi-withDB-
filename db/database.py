"""This module will have database connection and necessary 
methods
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# loads the values from .env file and skips them if there already
# and enviromental variable
load_dotenv()


# get the database uri
DATABASE_URL=os.getenv('DATABASE_URL')

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """This method gets database connection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
