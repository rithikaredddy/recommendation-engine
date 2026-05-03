"""
Content-Based Recommender
Uses TF-IDF on movie genres + title keywords → Cosine Similarity matrix
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "content_model.pkl")

class ContentBasedRecommender:
    def __init__(self):
        self.similarity_matrix = None
        self.movie_ids = None
        self.id_to_idx = {}

    def train(self, movies_df: pd.DataFrame):
        """
        Train the content-based model.
        movies_df must have columns: movie_id, title, genres (list or | separated string)
        """
        movies_df = movies_df.copy()

        # Build a combined text feature: genres + title words
        movies_df["genres"] = movies_df["genres"].apply(
            lambda g: " ".join(g) if isinstance(g, list) else g.replace("|", " ")
        )
        movies_df["features"] = movies_df["genres"] + " " + movies_df["title"]

        # TF-IDF vectorization
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(movies_df["features"])

        # Cosine similarity
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.movie_ids = movies_df["movie_id"].tolist()
        self.id_to_idx = {mid: i for i, mid in enumerate(self.movie_ids)}

        print(f"Content model trained on {len(self.movie_ids)} movies")

    def save(self):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump({
                "similarity_matrix": self.similarity_matrix,
                "movie_ids": self.movie_ids,
                "id_to_idx": self.id_to_idx
            }, f)
        print(f"Content model saved to {MODEL_PATH}")

    def load(self):
        if not os.path.exists(MODEL_PATH):
            print("Warning: Content model not found. Run train_models.py first.")
            return
        with open(MODEL_PATH, "rb") as f:
            data = pickle.load(f)
        self.similarity_matrix = data["similarity_matrix"]
        self.movie_ids = data["movie_ids"]
        self.id_to_idx = data["id_to_idx"]
        print("Content-based model loaded")

    def recommend(self, movie_id: int, limit: int = 10) -> list:
        """Return top-N similar movie IDs for a given movie."""
        if movie_id not in self.id_to_idx:
            return []
        idx = self.id_to_idx[movie_id]
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        # Exclude the movie itself (score = 1.0)
        similar = [self.movie_ids[i] for i, _ in scores[1:limit + 1]]
        return similar

    def get_similarity_score(self, movie_id_1: int, movie_id_2: int) -> float:
        """Get cosine similarity between two movies."""
        if movie_id_1 not in self.id_to_idx or movie_id_2 not in self.id_to_idx:
            return 0.0
        i, j = self.id_to_idx[movie_id_1], self.id_to_idx[movie_id_2]
        return float(self.similarity_matrix[i][j])
