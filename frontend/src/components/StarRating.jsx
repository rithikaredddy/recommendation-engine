"use client";
import { useState } from "react";

const StarRating = ({ currentRating, onRate, loading }) => {
  const [hovered, setHovered] = useState(0);

  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          onClick={() => !loading && onRate(star)}
          onMouseEnter={() => setHovered(star)}
          onMouseLeave={() => setHovered(0)}
          disabled={loading}
          className="text-2xl transition-transform hover:scale-110 disabled:cursor-not-allowed"
        >
          <span className={
            star <= (hovered || currentRating)
              ? "text-yellow-400"
              : "text-gray-600"
          }>★</span>
        </button>
      ))}
      {currentRating && (
        <span className="text-gray-400 text-sm ml-2">Your rating: {currentRating}/5</span>
      )}
    </div>
  );
};

export default StarRating;
