import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import Chatbot from 'react-chatbot-kit';
import config from './config';
import ActionProvider from './ActionProvider';
import MessageParser from './MessageParser';
import './chatbotstyle.css';
const ChatbotWrapper = () => {
  const { modelid } = useParams(); // Extract modelid from the URL

  // // Handle suggestion click
  // const handleSuggestionClick = (suggestion) => {
  //   // Clear suggestions after clicking
  //   setSuggestions([]);

  //   // You can handle suggestion logic here if needed
  // };
  
  return (
      <Chatbot
        config={config(modelid)} // Pass modelid to the config function
        messageParser={MessageParser}
        actionProvider={(props) => (
          <ActionProvider {...props} modelid={modelid}/>
        )}></Chatbot>
    
  );
};

export default ChatbotWrapper;
