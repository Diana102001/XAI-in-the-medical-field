import React, { useState } from 'react';
import axios from 'axios';

const ActionProvider = ({ createChatBotMessage, setState, children, modelid }) => {
  const [queryId, setQueryId] = useState(null);
  const [isAwaitingAnswer, setIsAwaitingAnswer] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [feedbackAnswers, setFeedbackAnswers] = useState({});
  const [textFeedback, setTextFeedback] = useState('');
  const [feedbackQuestions, setQuestions] = useState([]);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleForm = () => {
    const botMessage = createChatBotMessage(
      "Please fill out the following form:",
      {
        widget: "form",
        withAvatar: true,
        loading: true,
        widgetProps: { modelid }, // Pass modelid as a prop here
      }
    );
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const handleFormSubmit = (result, queryId) => {
    setQueryId(queryId);

    const botMessage = createChatBotMessage(`The result of your submission is: ${result}`);
    const suggestion = "Explain";
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
      queryId,
      suggestion,
    }));
  };

  const fetchExplanations = () => {
    setState((state) => {
      const queryId = state.queryId;

      if (queryId) {
        const botMessage = createChatBotMessage(
          `The available explanations are:`,
          {
            widget: "explanation",
            withAvatar: true,
            delay: 500,
            widgetParams: { modelid, queryId }
          });
        return {
          ...state,
          messages: [...state.messages, botMessage],
        };
      } else {
        const botMessage = createChatBotMessage(`No query_id found in the state.`);
        return {
          ...state,
          messages: [...state.messages, botMessage],
        };
      }
    });
  };

  const feedback = () => {
    setState((state) => {
      const queryId = state.queryId;

      if (queryId) {
        const botMessage = createChatBotMessage(
          `The available explanations are:`,
          {
            widget: "feedback",
            withAvatar: true,
            delay: 500,
            widgetParams: { queryId }
          });
        return {
          ...state,
          messages: [...state.messages, botMessage],
        };
      } else {
        const botMessage = createChatBotMessage(`No query_id found in the state.`);
        return {
          ...state,
          messages: [...state.messages, botMessage],
        };
      }
    });
  };

  const getFeedbackQuestions = () => {
    if (feedbackQuestions.length === 0) {
      const API_BASE_URL = 'http://localhost:8000';
    
      axios.get(`${API_BASE_URL}/feedback/${queryId}/`)
        .then(response => {
          const questions = response.data.questions;
    
          if (!Array.isArray(questions) || questions.length === 0) {
            setState((state) => ({
              ...state,
              messages: [...state.messages, "No questions found or invalid data format"],
            }));
            return;
          }
          setQuestions(questions);
          askQuestion(questions[currentQuestionIndex]);
    
        })
        .catch(error => {
          setState((state) => ({
            ...state,
            messages: [...state.messages, "Error getting questions"],
          }));
        });
    }
  };

  const askQuestion = (question) => {
    const botMessage = createChatBotMessage(question);
    setState((state) => ({
      ...state,
      messages: [...state.messages, botMessage],
    }));
    setIsAwaitingAnswer(true);
  };

  const handleUserInput = (input) => {
    if (!isAwaitingAnswer) {
      return;
    }
    
    if (currentQuestionIndex >= feedbackQuestions.length) {
      handleTextFeedback(input);
    } else {
      const parsedInput = parseInt(input, 10);
  
      if (isNaN(parsedInput) || parsedInput < 0 || parsedInput > 5) {
        const errorMessage = createChatBotMessage("Please enter a valid value between 0 and 5.");
        setState((state) => ({
          ...state,
          messages: [...state.messages, errorMessage],
        }));
      } else {
        const currentQuestion = feedbackQuestions[currentQuestionIndex];
        setFeedbackAnswers(prevAnswers => ({
          ...prevAnswers,
          [currentQuestion]: parsedInput,
        }));
  
        if (currentQuestionIndex + 1 < feedbackQuestions.length) {
          setCurrentQuestionIndex(currentQuestionIndex + 1);
          askQuestion(feedbackQuestions[currentQuestionIndex + 1]);
        } else {
          setCurrentQuestionIndex(currentQuestionIndex + 1);
          askQuestion("Any notes you want to add :)");
        }
      }
    }
  };

  const handleTextFeedback = (input) => {
    if (input.trim() === "") {
      const errorMessage = createChatBotMessage("Please enter some feedback before submitting.");
      setState((state) => ({
        ...state,
        messages: [...state.messages, errorMessage],
      }));
      return;
    }
    
    setTextFeedback(input.trim()); // Ensure no empty or whitespace-only feedback is set
    setIsAwaitingAnswer(false);

    if (!isSubmitted) {
      submitFeedback(input.trim()); // Pass the feedback to submit
    } else {
      console.log("Feedback already submitted. Ignoring further submissions.");
    }
  };

  const submitFeedback = (finalTextFeedback) => {
    if (!isSubmitted) {
      const data = {
        star_ratings: feedbackAnswers,
        text_feedback: finalTextFeedback, // Use the finalTextFeedback passed from handleTextFeedback
      };
      const API_BASE_URL = 'http://localhost:8000';
    
      axios.post(`${API_BASE_URL}/feedback/${queryId}/`, data)
        .then(response => {
          console.log('Feedback submitted successfully:', response.data);
          setIsSubmitted(true);
          const completionMessage = createChatBotMessage("Thank you for completing the feedback!");
          setState((state) => ({
            ...state,
            messages: [...state.messages, completionMessage],
          }));
        })
        .catch(error => {
          console.log(error);
        });
    }
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleForm,
            handleFormSubmit,
            fetchExplanations,
            feedback,
            getFeedbackQuestions,
            handleUserInput,
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;
