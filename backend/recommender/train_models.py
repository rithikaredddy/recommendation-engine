"""
Train and save all recommendation models.
Run this once after seeding the database.

Usage:
    python recommender/train_models.py

Downloads MovieLens 100K if not already present.
"""

import os
import zipfile
import urllib.request
import pandas as pd
from content_based import ContentBasedRecommender
from collaborative import CollaborativeRecommender

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "data")
ML_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"

GENRE_LIST = [
    "unknown", "Action", "Adventure", "Animation", "Children",
    "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
    "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
    "Sci-Fi", "Thriller", "War", "Western"
]

def download_movielens():
    zip_path = os.path.join(DATA_DIR, "ml-100k.zip")
    ml_dir = os.path.join(DATA_DIR, "ml-100k")
    if os.path.exists(ml_dir):
        print("MovieLens 100K already downloaded.")
        return ml_dir
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Downloading MovieLens 100K dataset...")
    urllib.request.urlretrieve(ML_URL, zip_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(DATA_DIR)
    os.remove(zip_path)
    print("Download complete.")
    return ml_dir

def load_movies(ml_dir: str) -> pd.DataFrame:
    movies_path = os.path.join(ml_dir, "u.item")
    cols = ["movie_id", "title", "release_date", "video_release", "imdb_url"] + GENRE_LIST
    df = pd.read_csv(movies_path, sep="|", encoding="latin-1", header=None, names=cols)

    # Build genres list
    df["genres"] = df[GENRE_LIST].apply(
        lambda row: [GENRE_LIST[i] for i, v in enumerate(row) if v == 1], axis=1
    )
    # Extract year from title
    df["year"] = df["title"].str.extract(r"\((\d{4})\)").astype(float)
    return df[["movie_id", "title", "genres", "year"]]

def load_ratings(ml_dir: str) -> pd.DataFrame:
    ratings_path = os.path.join(ml_dir, "u.data")
    df = pd.read_csv(ratings_path, sep="\t", header=None,
                     names=["user_id", "movie_id", "rating", "timestamp"])
    return df[["user_id", "movie_id", "rating"]]

if __name__ == "__main__":
    ml_dir = download_movielens()

    print("\n--- Loading data ---")
    movies_df = load_movies(ml_dir)
    ratings_df = load_ratings(ml_dir)
    print(f"Movies: {len(movies_df)}, Ratings: {len(ratings_df)}")

    print("\n--- Training Content-Based Model ---")
    content_rec = ContentBasedRecommender()
    content_rec.train(movies_df)
    content_rec.save()

    print("\n--- Training Collaborative Model ---")
    collab_rec = CollaborativeRecommender()
    collab_rec.train(ratings_df, movies_df)
    collab_rec.save()

    print("\n--- All models trained and saved! ---")
    print("Sample content-based recs for movie 1 (Toy Story):", content_rec.recommend(1, 5))
