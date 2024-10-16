"""This module has model of API
"""

from datetime import date
from pydantic import BaseModel, Field

class Movierequest(BaseModel):
    """This represents movierequests
    """
    Movie_title: str = Field(
        ...,
        description="movie title",
        example="RRR"
    )
    Director: str = Field(
        ...,
        description="Director name",
        example="SS.Rajamouli"
    )
    Release_date: date = Field(
        ...,
        description="Release date"
    )

class Movieresponse(BaseModel):
    """This represents Movieresponse
    """
    id: int = Field(..., description="id", example="movie_1")
    Movie_title: str = Field(..., description="movie title", example="RRR")
    Director: str = Field(..., description="Director name", example="SS.Rajamouli")
    Release_date: date = Field(..., description="Release date")
