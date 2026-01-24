// src/ChatOldChats.js
import React from 'react';
import QueryList from './QueryList';
import ChatbotWrapper from './MyChat/ChatbotWrapper';
import './ChatOldChats.css'; // Import the CSS file for styling
import Layout from './Layout';
const ChatOldChats = () => {
  return (
    <Layout>
    <div className="chat-old-chats-container">
    
      <div className="chatbot-wrapper-container">
        <ChatbotWrapper />
      </div>
    </div>
    </Layout>
  );
};

export default ChatOldChats;
