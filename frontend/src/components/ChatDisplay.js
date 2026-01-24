import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:8000';

const ChatDisplay = () => {
  const { queryId } = useParams();
  const [chatData, setChatData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChatData = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/chats/${queryId}`);
        setChatData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchChatData();
  }, [queryId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      {chatData.map((chat) => (
        <div key={chat.id}>
          <p><strong>Sent:</strong> {chat.sent_message}</p>
          <p><strong>Received:</strong> {chat.received_message}</p>
          <p><em>Timestamp: {new Date(chat.created_at).toLocaleString()}</em></p>
          <hr />
        </div>
      ))}
    </div>
  );
};

export default ChatDisplay;
