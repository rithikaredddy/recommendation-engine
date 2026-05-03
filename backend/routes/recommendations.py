from fastapi import APIRouter, Request, Depends, HTTPException
from middleware.auth import verify_token

router = APIRouter()

def get_recommenders(request: Request):
    return {
        "content": request.app.state.content_rec if hasattr(request.app.state, "content_rec") else None,
        "collab": request.app.state.collab_rec if hasattr(request.app.state, "collab_rec") else None,
        "hybrid": request.app.state.hybrid_rec if hasattr(request.app.state, "hybrid_rec") else None,
    }

@router.get("/content/{movie_id}")
async def content_based(movie_id: int, request: Request, limit: int = 10):
    """Get movies similar to the given movie using content-based filtering."""
    from recommender.content_based import ContentBasedRecommender
    rec = ContentBasedRecommender()
    rec.load()
    similar_ids = rec.recommend(movie_id, limit)

    db = request.app.state.db
    movies = await db.movies.find(
        {"movie_id": {"$in": similar_ids}},
        {"_id": 0}
    ).to_list(limit)

    # Preserve order
    id_to_movie = {m["movie_id"]: m for m in movies}
    return [id_to_movie[mid] for mid in similar_ids if mid in id_to_movie]

@router.get("/collaborative")
async def collaborative(
    request: Request,
    current_user: dict = Depends(verify_token),
    limit: int = 10
):
    """Get personalized recommendations based on user rating history (SVD)."""
    from recommender.collaborative import CollaborativeRecommender
    db = request.app.state.db

    # Get user's already-rated movies
    user_ratings = await db.ratings.find(
        {"user_id": current_user["user_id"]},
        {"movie_id": 1}
    ).to_list(1000)

    rated_ids = [r["movie_id"] for r in user_ratings]
    if not rated_ids:
        # Cold start: return trending
        movies = await db.movies.find(
            {"num_ratings": {"$gte": 50}},
            {"_id": 0}
        ).sort("avg_rating", -1).limit(limit).to_list(limit)
        return {"method": "trending (cold start)", "movies": movies}

    rec = CollaborativeRecommender()
    rec.load()
    recommended_ids = rec.recommend(current_user["user_id"], rated_ids, limit)

    movies = await db.movies.find(
        {"movie_id": {"$in": recommended_ids}},
        {"_id": 0}
    ).to_list(limit)

    return {"method": "collaborative", "movies": movies}

@router.get("/hybrid")
async def hybrid(
    request: Request,
    current_user: dict = Depends(verify_token),
    limit: int = 10
):
    """Hybrid recommendation — blend of content-based and collaborative."""
    from recommender.hybrid import HybridRecommender
    from recommender.content_based import ContentBasedRecommender
    from recommender.collaborative import CollaborativeRecommender

    db = request.app.state.db

    user_ratings = await db.ratings.find(
        {"user_id": current_user["user_id"]},
        {"movie_id": 1, "rating": 1}
    ).to_list(1000)

    if not user_ratings:
        movies = await db.movies.find(
            {"num_ratings": {"$gte": 50}},
            {"_id": 0}
        ).sort("avg_rating", -1).limit(limit).to_list(limit)
        return {"method": "trending (cold start)", "movies": movies}

    rated_ids = [r["movie_id"] for r in user_ratings]
    # Use highest-rated movie as content seed
    top_rated = max(user_ratings, key=lambda x: x["rating"])

    content_rec = ContentBasedRecommender()
    content_rec.load()
    collab_rec = CollaborativeRecommender()
    collab_rec.load()
    hybrid_rec = HybridRecommender(content_rec, collab_rec)

    recommended_ids = hybrid_rec.recommend(
        user_id=current_user["user_id"],
        seed_movie_id=top_rated["movie_id"],
        rated_ids=rated_ids,
        limit=limit
    )

    movies = await db.movies.find(
        {"movie_id": {"$in": recommended_ids}},
        {"_id": 0}
    ).to_list(limit)

    return {"method": "hybrid", "movies": movies}
