from fastapi import APIRouter, Request, Depends, HTTPException, Query
from middleware.auth import verify_token
from models.user import RatingCreate
from datetime import datetime

router = APIRouter()

@router.get("/trending")
async def get_trending(request: Request, limit: int = 20):
    db = request.app.state.db
    movies = await db.movies.find(
        {"num_ratings": {"$gte": 50}},
        {"_id": 0}
    ).sort("avg_rating", -1).limit(limit).to_list(limit)
    return movies

@router.get("/search")
async def search_movies(request: Request, q: str = Query(..., min_length=1), limit: int = 10):
    db = request.app.state.db
    movies = await db.movies.find(
        {"title": {"$regex": q, "$options": "i"}},
        {"_id": 0}
    ).limit(limit).to_list(limit)
    return movies

@router.get("/{movie_id}")
async def get_movie(movie_id: int, request: Request):
    db = request.app.state.db
    movie = await db.movies.find_one({"movie_id": movie_id}, {"_id": 0})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/{movie_id}/rate")
async def rate_movie(
    movie_id: int,
    rating_data: RatingCreate,
    request: Request,
    current_user: dict = Depends(verify_token)
):
    db = request.app.state.db

    # Check movie exists
    movie = await db.movies.find_one({"movie_id": movie_id})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_id = current_user["user_id"]

    # Save or update rating
    await db.ratings.update_one(
        {"user_id": user_id, "movie_id": movie_id},
        {"$set": {
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating_data.rating,
            "timestamp": datetime.utcnow()
        }},
        upsert=True
    )

    # Update user's rated_movies list
    await db.users.update_one(
        {"_id": __import__("bson").ObjectId(user_id)},
        {"$addToSet": {"rated_movies": movie_id}}
    )

    # Recalculate avg_rating for the movie
    pipeline = [
        {"$match": {"movie_id": movie_id}},
        {"$group": {"_id": "$movie_id", "avg": {"$avg": "$rating"}, "count": {"$sum": 1}}}
    ]
    result = await db.ratings.aggregate(pipeline).to_list(1)
    if result:
        await db.movies.update_one(
            {"movie_id": movie_id},
            {"$set": {"avg_rating": round(result[0]["avg"], 2), "num_ratings": result[0]["count"]}}
        )

    return {"message": "Rating saved", "movie_id": movie_id, "rating": rating_data.rating}

@router.get("/{movie_id}/ratings/me")
async def get_my_rating(
    movie_id: int,
    request: Request,
    current_user: dict = Depends(verify_token)
):
    db = request.app.state.db
    rating = await db.ratings.find_one(
        {"user_id": current_user["user_id"], "movie_id": movie_id},
        {"_id": 0}
    )
    return {"rating": rating["rating"] if rating else None}
