"""
Seed MovieLens 100K movies and ratings into MongoDB.
Run after training models.

Usage:
    python seed/seed_movies.py
"""

import asyncio
import os
import urllib.request
import zipfile
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "data")
ML_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"

GENRE_LIST = [
    "unknown", "Action", "Adventure", "Animation", "Children",
    "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
    "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
    "Sci-Fi", "Thriller", "War", "Western"
]

def download_data():
    ml_dir = os.path.join(DATA_DIR, "ml-100k")
    if os.path.exists(ml_dir):
        return ml_dir
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Downloading MovieLens 100K...")
    zip_path = os.path.join(DATA_DIR, "ml-100k.zip")
    urllib.request.urlretrieve(ML_URL, zip_path)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(DATA_DIR)
    os.remove(zip_path)
    return ml_dir

async def seed():
    ml_dir = download_data()

    # Load movies
    cols = ["movie_id", "title", "release_date", "video", "imdb"] + GENRE_LIST
    movies_df = pd.read_csv(
        os.path.join(ml_dir, "u.item"), sep="|", encoding="latin-1",
        header=None, names=cols
    )
    movies_df["genres"] = movies_df[GENRE_LIST].apply(
        lambda r: [GENRE_LIST[i] for i, v in enumerate(r) if v == 1], axis=1
    )
    movies_df["year"] = movies_df["title"].str.extract(r"\((\d{4})\)").astype(float)

    # Load ratings to compute avg and count
    ratings_df = pd.read_csv(
        os.path.join(ml_dir, "u.data"), sep="\t", header=None,
        names=["user_id", "movie_id", "rating", "timestamp"]
    )
    agg = ratings_df.groupby("movie_id")["rating"].agg(["mean", "count"]).reset_index()
    agg.columns = ["movie_id", "avg_rating", "num_ratings"]
    agg["avg_rating"] = agg["avg_rating"].round(2)

    movies_df = movies_df.merge(agg, on="movie_id", how="left")

    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["recommendation_engine"]

    # Clear and insert movies
    await db.movies.delete_many({})
    docs = movies_df[["movie_id", "title", "genres", "year", "avg_rating", "num_ratings"]].to_dict("records")
    # Convert NaN to None
    for doc in docs:
        for k, v in doc.items():
            if pd.isna(v) if not isinstance(v, list) else False:
                doc[k] = None
    await db.movies.insert_many(docs)
    print(f"Seeded {len(docs)} movies")

    # Create indexes
    await db.movies.create_index("movie_id", unique=True)
    await db.movies.create_index([("title", "text")])
    await db.movies.create_index("avg_rating")
    await db.ratings.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
    await db.users.create_index("email", unique=True)
    print("Indexes created")

    client.close()
    print("Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed())
