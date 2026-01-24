// import React, { useEffect, useState } from 'react';
// import { useParams } from 'react-router-dom';
// import axios from 'axios';

// const API_BASE_URL = 'http://localhost:8000';

// const ChatDetails = () => {
//   const { id } = useParams(); // Extract the id from the URL
//   const [chat, setChat] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchChatDetails = async () => {
//       try {
//         const response = await axios.get(`${API_BASE_URL}/chats/${id}/`);
//         const chatData = Array.isArray(response.data) ? response.data[0] : response.data; // Handle array response
//         console.log('Chat Data:', chatData);
//         setChat(chatData);
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchChatDetails();
//   }, [id]);

//   if (loading) return <p>Loading...</p>;
//   if (error) return <p>Error: {error}</p>;
//   if (!chat) return <p>No chat found with ID {id}</p>;

//   return (
//     <div>
//       <h2>Chat Details</h2>
//       <p><strong>Sent Message:</strong> {chat.sent_message || "N/A"}</p>
//       <p><strong>Received Message:</strong> {chat.received_message || "N/A"}</p>
//       <p><strong>Created At:</strong> {chat.created_at ? new Date(chat.created_at).toLocaleString() : "N/A"}</p>
//     </div>
//   );
// };

// export default ChatDetails;

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { ChatBot } from 'react-chatbot-kit'; // Adjust this import based on the actual library API
import 'react-chatbot-kit/build/main.css'; // Import default styles if needed

const API_BASE_URL = 'http://localhost:8000';

const ChatDetails = () => {
  const { id } = useParams(); // Extract the id from the URL
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChatDetails = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/chats/${id}/`);
        setChat(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchChatDetails();
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!chat || chat.length === 0) return <p>No chat found with ID {id}</p>;

  // Transform the fetched data to the format required by react-chatbot-kit
  const messages = chat.map(message => ({
    id: message.id,
    type: message.sent_message ? 'user' : 'bot', // Use 'user' for sent_message and 'bot' for received_message
    content: message.sent_message || message.received_message,
    timestamp: new Date(message.created_at).toLocaleTimeString() // Optional: add timestamp if needed
  }));

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <ChatBot
        botName="ChatBot"
        messages={messages}
        // Add additional props if needed
      />
    </div>
  );
};

export default ChatDetails;
