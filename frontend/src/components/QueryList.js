import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:8000';

const QueryList = () => {
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQueries = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/user-queries/`);
        setQueries(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchQueries();
  }, []);

  const handleClick = (queryId) => {
    navigate(`/chats/${queryId}`);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <ul>
        {queries.map(query => (
          <li key={query.id}>
            <p>
              <button onClick={() => handleClick(query.id)}>
                <strong>Query number:</strong> {query.id}
              </button>
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default QueryList;
