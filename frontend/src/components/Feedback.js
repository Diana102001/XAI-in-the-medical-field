import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:8000';

const FeedbackForm = ({queryId}) => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [starRatings, setStarRatings] = useState({});
  const [textFeedback, setTextFeedback] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    // Fetch questions once at the start
    axios.get(`${API_BASE_URL}/feedback/${queryId}/`)
      .then(response => {
        const data = response.data;
        setQuestions(data.questions || []);
      })
      .catch(error => {
        console.error("There was an error fetching the questions!", error);
      });
  }, [queryId]);

  const handleStarChange = (value) => {
    setStarRatings(prevRatings => ({
      ...prevRatings,
      [currentQuestionIndex]: value
    }));
  };

  const handleNextQuestion = () => {
    setCurrentQuestionIndex(currentQuestionIndex + 1);
  };

  const handleSubmit = () => {
    const data = {
      star_ratings: starRatings,
      text_feedback: textFeedback
    };
    console.log(data)

    axios.post(`${API_BASE_URL}/feedback/${queryId}/`, data)
      .then(response => {
        setIsSubmitted(true);
      })
      .catch(error => {
        console.error("There was an error submitting the feedback!", error);
      });
  };

  if (isSubmitted) {
    return <p>Thank you for your feedback!</p>;
  }

  return (
    <div>
      <h1>Submit Your Feedback</h1>
      {questions.length > 0 && currentQuestionIndex < questions.length ? (
        <div>
          <label>{questions[currentQuestionIndex]}</label>
          <input 
            type="number" 
            min="0" 
            max="5" 
            value={starRatings[currentQuestionIndex] || 0} 
            onChange={(e) => handleStarChange(e.target.value)} 
          />
          <button onClick={handleNextQuestion}>
            Next
          </button>
        </div>
      ) : (
        <p>Loading questions...</p>
      )}
      {currentQuestionIndex === questions.length && (
        <div>
          <label>Text Feedback</label>
          <textarea
            value={textFeedback}
            onChange={(e) => setTextFeedback(e.target.value)}
          />
          <button onClick={handleSubmit}>Submit</button>
        </div>
      )}
    </div>
  );
};

export default FeedbackForm;
