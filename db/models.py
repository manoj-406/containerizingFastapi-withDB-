"""This module contains database models
"""

from sqlalchemy import  Column, Integer, String,Date
from db.database import Base

class movieshop(Base):
    """This represents the database table Books
    """
    __tablename__ = "movieshop"
    id = Column(Integer, primary_key=True)
    Movie_title = Column(String)
    Director = Column(String)
    Release_date = Column(Date)
