import React, { useState, useEffect } from 'react';
import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000';

const useFeedbackQuestions = (queryId) => {
  const [questions, setQuestions] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFeedback = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/feedback/${queryId}/`);
        setQuestions(response.data.questions || []);
      } catch (err) {
        console.error("There was an error fetching the feedback!", err);
        setError(err);
      }
    };

    fetchFeedback();
  }, [queryId]);

  return { questions, error };
};

export default useFeedbackQuestions;
