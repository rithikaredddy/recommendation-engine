"""
Hybrid Recommender
Blends Content-Based and Collaborative Filtering scores.
Default weight: 40% content + 60% collaborative
"""

from recommender.content_based import ContentBasedRecommender
from recommender.collaborative import CollaborativeRecommender

class HybridRecommender:
    def __init__(
        self,
        content_rec: ContentBasedRecommender,
        collab_rec: CollaborativeRecommender,
        content_weight: float = 0.4,
        collab_weight: float = 0.6
    ):
        self.content_rec = content_rec
        self.collab_rec = collab_rec
        self.content_weight = content_weight
        self.collab_weight = collab_weight

    def recommend(
        self,
        user_id: str,
        seed_movie_id: int,
        rated_ids: list,
        limit: int = 10
    ) -> list:
        """
        Hybrid recommendation:
        1. Get content-based candidates from seed movie
        2. Score each with collaborative predicted rating
        3. Blend scores and return top-N
        """
        rated_set = set(rated_ids)

        # Content candidates (wider pool)
        content_candidates = self.content_rec.recommend(seed_movie_id, limit=limit * 3)
        content_candidates = [mid for mid in content_candidates if mid not in rated_set]

        if not content_candidates:
            # Fallback to pure collaborative
            return self.collab_rec.recommend(user_id, rated_ids, limit)

        # Score each candidate
        scored = []
        for mid in content_candidates:
            content_score = self.content_rec.get_similarity_score(seed_movie_id, mid)
            collab_score = self.collab_rec.predict_rating(user_id, mid) / 5.0  # normalize to 0-1
            hybrid_score = (self.content_weight * content_score) + (self.collab_weight * collab_score)
            scored.append((mid, hybrid_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [mid for mid, _ in scored[:limit]]
