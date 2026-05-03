"use client";
import { useEffect, useState } from "react";
import MovieGrid from "./MovieGrid";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const RecommendationSection = ({ title, endpoint, token }) => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    fetch(`${API}${endpoint}`, { headers })
      .then((r) => r.json())
      .then((data) => {
        // Handle both array response and { movies: [] } shape
        setMovies(Array.isArray(data) ? data : data.movies || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [endpoint, token]);

  return (
    <section className="mb-10">
      <h2 className="text-white text-lg font-semibold mb-4">{title}</h2>
      <MovieGrid movies={movies} loading={loading} emptyMessage="No recommendations yet." />
    </section>
  );
};

export default RecommendationSection;
