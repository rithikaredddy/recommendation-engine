"""
EDA and Model Training Script
Run this to explore the MovieLens dataset and train all models.

Usage:
    cd ml
    python notebooks/EDA_and_Model.py

Requires: pandas, numpy, matplotlib, seaborn, scikit-learn, scikit-surprise
"""

import os
import sys
import urllib.request
import zipfile
import pandas as pd
import numpy as np

# ─── 1. Download Dataset ────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ML_DIR = os.path.join(DATA_DIR, "ml-100k")

if not os.path.exists(ML_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Downloading MovieLens 100K...")
    zip_path = os.path.join(DATA_DIR, "ml-100k.zip")
    urllib.request.urlretrieve("https://files.grouplens.org/datasets/movielens/ml-100k.zip", zip_path)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(DATA_DIR)
    os.remove(zip_path)
    print("Download complete.")
else:
    print("Dataset already present.")

# ─── 2. Load Data ───────────────────────────────────────────────────────────

GENRE_LIST = [
    "unknown", "Action", "Adventure", "Animation", "Children",
    "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
    "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
    "Sci-Fi", "Thriller", "War", "Western"
]

# Load movies
movie_cols = ["movie_id", "title", "release_date", "video", "imdb_url"] + GENRE_LIST
movies = pd.read_csv(os.path.join(ML_DIR, "u.item"), sep="|", encoding="latin-1",
                     header=None, names=movie_cols)
movies["genres"] = movies[GENRE_LIST].apply(
    lambda r: [GENRE_LIST[i] for i, v in enumerate(r) if v == 1], axis=1
)
movies["year"] = movies["title"].str.extract(r"\((\d{4})\)").astype(float)

# Load ratings
ratings = pd.read_csv(os.path.join(ML_DIR, "u.data"), sep="\t", header=None,
                      names=["user_id", "movie_id", "rating", "timestamp"])

# Load users
user_cols = ["user_id", "age", "gender", "occupation", "zip"]
users = pd.read_csv(os.path.join(ML_DIR, "u.user"), sep="|", header=None, names=user_cols)

print("\n=== Dataset Overview ===")
print(f"Movies:  {len(movies):,}")
print(f"Ratings: {len(ratings):,}")
print(f"Users:   {len(users):,}")
print(f"Rating range: {ratings['rating'].min()} – {ratings['rating'].max()}")
print(f"Rating mean:  {ratings['rating'].mean():.3f}")

# ─── 3. EDA ─────────────────────────────────────────────────────────────────

print("\n=== Rating Distribution ===")
print(ratings["rating"].value_counts().sort_index())

print("\n=== Top 10 Most Rated Movies ===")
top = (ratings.groupby("movie_id")["rating"]
       .agg(["count", "mean"])
       .reset_index()
       .merge(movies[["movie_id", "title"]], on="movie_id")
       .sort_values("count", ascending=False)
       .head(10))
print(top[["title", "count", "mean"]].to_string(index=False))

print("\n=== Genre Distribution ===")
genre_counts = {}
for genres in movies["genres"]:
    for g in genres:
        genre_counts[g] = genre_counts.get(g, 0) + 1
for genre, count in sorted(genre_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  {genre:20s}: {count}")

print("\n=== User Activity Stats ===")
user_activity = ratings.groupby("user_id")["rating"].count()
print(f"  Avg ratings per user: {user_activity.mean():.1f}")
print(f"  Min: {user_activity.min()}, Max: {user_activity.max()}")

# ─── 4. Sparsity ────────────────────────────────────────────────────────────

n_users = ratings["user_id"].nunique()
n_movies = ratings["movie_id"].nunique()
n_ratings = len(ratings)
sparsity = 1 - (n_ratings / (n_users * n_movies))
print(f"\n=== Matrix Sparsity ===")
print(f"  Users: {n_users}, Movies: {n_movies}")
print(f"  Sparsity: {sparsity:.4f} ({sparsity*100:.2f}% empty)")

# ─── 5. Train Content-Based Model ───────────────────────────────────────────

print("\n=== Training Content-Based Model ===")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend", "recommender"))
from content_based import ContentBasedRecommender

content_rec = ContentBasedRecommender()
content_rec.train(movies[["movie_id", "title", "genres"]])
content_rec.save()

toy_story_recs = content_rec.recommend(1, 5)
toy_story_titles = movies[movies["movie_id"].isin(toy_story_recs)]["title"].tolist()
print(f"  Toy Story recommendations: {toy_story_titles}")

# ─── 6. Train Collaborative Model ───────────────────────────────────────────

print("\n=== Training Collaborative Model (SVD) ===")
from collaborative import CollaborativeRecommender

collab_rec = CollaborativeRecommender()
collab_rec.train(ratings, movies[["movie_id"]])
collab_rec.save()
print(f"  SVD RMSE: {collab_rec.rmse:.4f}")

print("\n=== All models trained successfully! ===")
print("Next step: run 'python seed/seed_movies.py' to load data into MongoDB.")
