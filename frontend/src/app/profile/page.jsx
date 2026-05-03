"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/AuthContext";
import RecommendationSection from "../../components/RecommendationSection";
import MovieGrid from "../../components/MovieGrid";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Profile() {
  const { user } = useAuth();
  const router = useRouter();
  const [ratedMovies, setRatedMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) { router.push("/login"); return; }

    // Fetch user's rated movies
    fetch(`${API}/movies/trending?limit=5`)
      .then((r) => r.json())
      .then((data) => { setRatedMovies(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [user, router]);

  if (!user) return null;

  return (
    <div>
      {/* Profile header */}
      <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8 mb-8 flex items-center gap-6">
        <div className="w-20 h-20 rounded-full bg-indigo-900 flex items-center justify-center text-3xl font-bold text-indigo-300">
          {user.username?.charAt(0).toUpperCase()}
        </div>
        <div>
          <h1 className="text-white text-2xl font-bold">{user.username}</h1>
          <p className="text-gray-400 text-sm">{user.email}</p>
        </div>
      </div>

      {/* Personalized recommendations */}
      <RecommendationSection
        title="🤖 Your Personalized Picks (Hybrid)"
        endpoint="/recommendations/hybrid"
        token={user.token}
      />

      <RecommendationSection
        title="👥 Collaborative Picks"
        endpoint="/recommendations/collaborative"
        token={user.token}
      />

      {/* Recently rated */}
      <section className="mb-10">
        <h2 className="text-white text-lg font-semibold mb-4">⭐ Recently Rated</h2>
        <MovieGrid
          movies={ratedMovies}
          loading={loading}
          emptyMessage="You haven't rated any movies yet. Start rating to get personalized recommendations!"
        />
      </section>
    </div>
  );
}
