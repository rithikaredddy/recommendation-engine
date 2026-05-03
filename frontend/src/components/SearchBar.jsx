"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const debounceRef = useRef(null);
  const router = useRouter();

  useEffect(() => {
    if (!query.trim()) { setResults([]); setOpen(false); return; }
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API}/movies/search?q=${encodeURIComponent(query)}&limit=6`);
        const data = await res.json();
        setResults(data);
        setOpen(true);
      } catch { setResults([]); }
      setLoading(false);
    }, 350);
    return () => clearTimeout(debounceRef.current);
  }, [query]);

  const handleSelect = (movie) => {
    setQuery("");
    setOpen(false);
    router.push(`/movie/${movie.movie_id}`);
  };

  return (
    <div className="relative w-full max-w-xl mx-auto">
      <div className="flex items-center bg-gray-800 border border-gray-700 rounded-xl px-4 py-2.5 gap-3">
        <span className="text-gray-400 text-lg">🔍</span>
        <input
          type="text"
          placeholder="Search movies..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setOpen(true)}
          onBlur={() => setTimeout(() => setOpen(false), 150)}
          className="bg-transparent text-white placeholder-gray-500 outline-none flex-1 text-sm"
        />
        {loading && <span className="text-gray-500 text-xs">searching...</span>}
      </div>

      {open && results.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-2xl z-50">
          {results.map((movie) => (
            <button
              key={movie.movie_id}
              onMouseDown={() => handleSelect(movie)}
              className="w-full text-left px-4 py-3 hover:bg-gray-700 transition flex items-center justify-between gap-4"
            >
              <span className="text-white text-sm">{movie.title}</span>
              <span className="text-gray-500 text-xs shrink-0">{movie.genres?.[0]}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
