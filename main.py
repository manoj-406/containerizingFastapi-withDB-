"""This module contains main files
"""
from datetime import date
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.model import Movierequest, Movieresponse
from db.database import get_db,Base,engine
from db.models import movieshop

#Create Database tables
Base.metadata.create_all(bind=engine)
app = FastAPI()

#gets movie response here
@app.get("/movie", response_model=list[Movieresponse])
def get_movies(db: Session = Depends(get_db)):
    """This Function Gets all the Movieresponses
    """
    
    return db.query(movieshop).all()

@app.post("/movie", response_model=Movieresponse)
def requested_movie(request: Movierequest,db: Session = Depends(get_db)):
    """This Function Returns Movierequest
    """

    db_movie = movieshop(**request.model_dump()) 
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movie/{movie_id}")
def delete_movie(movie_id: int,db: Session = Depends(get_db)):
    """This method deletes the movie
    """
    db_movie = db.query(movieshop).filter(movieshop.id == movie_id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return{"message": "Movie Deleted Sucessfully"}
