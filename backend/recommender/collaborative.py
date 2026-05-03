import pickle
import os
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "collab_model.pkl")

class CollaborativeRecommender:
    def __init__(self):
        self.model = None
        self.user_encoder = LabelEncoder()
        self.movie_encoder = LabelEncoder()
        self.all_movie_ids = []
        self.rating_matrix = None
        self.rmse = None

    def train(self, ratings_df, movies_df):
        self.all_movie_ids = movies_df["movie_id"].tolist()
        ratings_df = ratings_df.copy()
        ratings_df["user_idx"] = self.user_encoder.fit_transform(ratings_df["user_id"].astype(str))
        ratings_df["movie_idx"] = self.movie_encoder.fit_transform(ratings_df["movie_id"].astype(str))
        n_users = ratings_df["user_idx"].nunique()
        n_movies = ratings_df["movie_idx"].nunique()
        self.rating_matrix = np.zeros((n_users, n_movies))
        for _, row in ratings_df.iterrows():
            self.rating_matrix[int(row["user_idx"]), int(row["movie_idx"])] = row["rating"]
        self.model = TruncatedSVD(n_components=50, random_state=42)
        self.model.fit(self.rating_matrix)
        print("Collaborative model trained.")

    def save(self):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump({
                "model": self.model,
                "user_encoder": self.user_encoder,
                "movie_encoder": self.movie_encoder,
                "all_movie_ids": self.all_movie_ids,
                "rating_matrix": self.rating_matrix,
            }, f)

    def load(self):
        if not os.path.exists(MODEL_PATH):
            print("Warning: Collaborative model not found.")
            return
        with open(MODEL_PATH, "rb") as f:
            data = pickle.load(f)
        self.model = data["model"]
        self.user_encoder = data["user_encoder"]
        self.movie_encoder = data["movie_encoder"]
        self.all_movie_ids = data["all_movie_ids"]
        self.rating_matrix = data["rating_matrix"]
        print("Collaborative model loaded.")

    def recommend(self, user_id, rated_movie_ids, limit=10):
        if self.model is None:
            return []
        rated_set = set(rated_movie_ids)
        candidates = [mid for mid in self.all_movie_ids if mid not in rated_set]
        return candidates[:limit]

    def predict_rating(self, user_id, movie_id):
        return 3.0