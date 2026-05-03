from pydantic import BaseModel
from typing import Optional, List

class Movie(BaseModel):
    movie_id: int
    title: str
    genres: List[str]
    year: Optional[int] = None
    avg_rating: Optional[float] = None
    num_ratings: Optional[int] = None
    description: Optional[str] = None

class MovieDetail(Movie):
    similar_movies: Optional[List[dict]] = []
