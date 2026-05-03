import MovieCard from "./MovieCard";

const MovieGrid = ({ movies, loading, emptyMessage = "No movies found." }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {Array.from({ length: 10 }).map((_, i) => (
          <div key={i} className="bg-gray-800 rounded-xl h-64 animate-pulse" />
        ))}
      </div>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <p className="text-gray-500 text-center py-12">{emptyMessage}</p>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {movies.map((movie) => (
        <MovieCard key={movie.movie_id} movie={movie} />
      ))}
    </div>
  );
};

export default MovieGrid;
