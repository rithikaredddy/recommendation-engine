"use client";
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import SearchBar from "../components/SearchBar";
import MovieGrid from "../components/MovieGrid";
import RecommendationSection from "../components/RecommendationSection";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const { user } = useAuth();
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/movies/trending?limit=20`)
      .then((r) => r.json())
      .then((data) => { setTrending(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div>
      {/* Hero */}
      <div className="text-center mb-12 py-8">
        <h1 className="text-4xl font-bold text-white mb-3">
          Find Your Next Favourite Movie 🎬
        </h1>
        <p className="text-gray-400 mb-8 text-lg">
          Powered by Content-Based & Collaborative Filtering
        </p>
        <SearchBar />
      </div>

      {/* Personalized recs for logged-in users */}
      {user && (
        <RecommendationSection
          title="🤖 Recommended For You"
          endpoint="/recommendations/hybrid"
          token={user.token}
        />
      )}

      {/* Trending */}
      <section>
        <h2 className="text-white text-lg font-semibold mb-4">🔥 Trending Movies</h2>
        <MovieGrid movies={trending} loading={loading} />
      </section>
    </div>
  );
}
