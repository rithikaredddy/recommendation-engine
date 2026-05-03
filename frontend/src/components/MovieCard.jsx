import Link from "next/link";

const GENRE_COLORS = {
  Action: "bg-red-900 text-red-300",
  Comedy: "bg-yellow-900 text-yellow-300",
  Drama: "bg-blue-900 text-blue-300",
  Horror: "bg-purple-900 text-purple-300",
  Romance: "bg-pink-900 text-pink-300",
  "Sci-Fi": "bg-cyan-900 text-cyan-300",
  Thriller: "bg-orange-900 text-orange-300",
  Animation: "bg-green-900 text-green-300",
};

const MovieCard = ({ movie }) => {
  const genre = movie.genres?.[0];
  const genreColor = GENRE_COLORS[genre] || "bg-gray-700 text-gray-300";
  const initial = movie.title?.charAt(0).toUpperCase();

  return (
    <Link href={`/movie/${movie.movie_id}`}>
      <div className="bg-gray-800 rounded-xl overflow-hidden hover:scale-105 transition-transform duration-200 cursor-pointer border border-gray-700 hover:border-indigo-500 h-full flex flex-col">
        {/* Poster placeholder */}
        <div className="bg-gradient-to-br from-indigo-900 to-gray-800 h-48 flex items-center justify-center">
          <span className="text-5xl font-bold text-indigo-300 opacity-60">{initial}</span>
        </div>
        <div className="p-4 flex flex-col flex-1 gap-2">
          <h3 className="text-white font-medium text-sm leading-snug line-clamp-2">
            {movie.title}
          </h3>
          <div className="flex items-center justify-between mt-auto pt-2">
            {genre && (
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${genreColor}`}>
                {genre}
              </span>
            )}
            {movie.avg_rating && (
              <span className="text-yellow-400 text-xs font-semibold">
                ⭐ {movie.avg_rating.toFixed(1)}
              </span>
            )}
          </div>
          {movie.year && (
            <p className="text-gray-500 text-xs">{movie.year}</p>
          )}
        </div>
      </div>
    </Link>
  );
};

export default MovieCard;
