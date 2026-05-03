"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "../../../context/AuthContext";
import StarRating from "../../../components/StarRating";
import RecommendationSection from "../../../components/RecommendationSection";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function MovieDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const router = useRouter();

  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [myRating, setMyRating] = useState(null);
  const [ratingLoading, setRatingLoading] = useState(false);
  const [ratedMsg, setRatedMsg] = useState("");

  useEffect(() => {
    fetch(`${API}/movies/${id}`)
      .then((r) => r.json())
      .then((data) => { setMovie(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    if (!user) return;
    fetch(`${API}/movies/${id}/ratings/me`, {
      headers: { Authorization: `Bearer ${user.token}` },
    })
      .then((r) => r.json())
      .then((data) => setMyRating(data.rating));
  }, [id, user]);

  const handleRate = async (stars) => {
    if (!user) { router.push("/login"); return; }
    setRatingLoading(true);
    try {
      await fetch(`${API}/movies/${id}/rate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify({ rating: stars }),
      });
      setMyRating(stars);
      setRatedMsg("Rating saved!");
      setTimeout(() => setRatedMsg(""), 2000);
    } catch { }
    setRatingLoading(false);
  };

  if (loading) return (
    <div className="animate-pulse">
      <div className="h-48 bg-gray-800 rounded-xl mb-6" />
      <div className="h-6 bg-gray-800 rounded w-1/2 mb-4" />
      <div className="h-4 bg-gray-800 rounded w-1/3" />
    </div>
  );

  if (!movie) return (
    <p className="text-gray-500 text-center py-20">Movie not found.</p>
  );

  return (
    <div>
      {/* Movie hero */}
      <div className="bg-gray-800 rounded-2xl p-8 mb-8 flex gap-8 items-start border border-gray-700">
        {/* Poster placeholder */}
        <div className="bg-gradient-to-br from-indigo-900 to-gray-700 rounded-xl w-32 h-44 flex-shrink-0 flex items-center justify-center">
          <span className="text-4xl font-bold text-indigo-300 opacity-70">
            {movie.title?.charAt(0)}
          </span>
        </div>

        <div className="flex-1 min-w-0">
          <h1 className="text-white text-2xl font-bold mb-2">{movie.title}</h1>

          <div className="flex flex-wrap gap-2 mb-4">
            {movie.genres?.map((g) => (
              <span key={g} className="bg-indigo-900 text-indigo-300 text-xs px-3 py-1 rounded-full">
                {g}
              </span>
            ))}
            {movie.year && (
              <span className="bg-gray-700 text-gray-300 text-xs px-3 py-1 rounded-full">
                {movie.year}
              </span>
            )}
          </div>

          {movie.avg_rating && (
            <p className="text-yellow-400 font-semibold mb-4">
              ⭐ {movie.avg_rating.toFixed(1)} / 5
              <span className="text-gray-500 font-normal text-sm ml-2">
                ({movie.num_ratings} ratings)
              </span>
            </p>
          )}

          {/* Star rating */}
          <div className="mt-4">
            <p className="text-gray-400 text-sm mb-2">
              {user ? "Rate this movie:" : "Login to rate this movie"}
            </p>
            {user && (
              <>
                <StarRating currentRating={myRating} onRate={handleRate} loading={ratingLoading} />
                {ratedMsg && <p className="text-green-400 text-sm mt-2">{ratedMsg}</p>}
              </>
            )}
          </div>
        </div>
      </div>

      {/* Content-based recommendations */}
      <RecommendationSection
        title="🎯 Similar Movies (Content-Based)"
        endpoint={`/recommendations/content/${id}`}
      />

      {/* Collaborative recs for logged-in users */}
      {user && (
        <RecommendationSection
          title="👥 Users Like You Also Watched"
          endpoint="/recommendations/collaborative"
          token={user.token}
        />
      )}
    </div>
  );
}
