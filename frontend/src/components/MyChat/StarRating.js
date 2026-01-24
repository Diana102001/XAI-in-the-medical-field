import React, { useState } from 'react';
import axios from 'axios';
import './StarRating.css';

const API_BASE_URL = 'http://localhost:8000';
const StarRating = ({ explanationId}) => {
  const [rating, setRating] = useState(0);
  const [error, setError] = useState(null);

  const handleRating = async (newRating) => {
    try {
      const url = `${API_BASE_URL}/explanation/${explanationId}/rate/`; // assuming 'modelid' is actually the explanation id
      await axios.put(url, {rating: newRating });
      setRating(newRating);
    } catch (error) {
      console.error('Error submitting rating:', error);
      setError('There was an error submitting your rating.');
    }
  };
  

  return (
    <div>
      {[1, 2, 3, 4, 5].map((star) => (
        <span
          key={star}
          className={`star ${star <= rating ? 'selected' : ''}`}
          onClick={() => handleRating(star)}
        >
          ★
        </span>
      ))}
      {error && <p>{error}</p>}
    </div>
  );
};

export default StarRating;
