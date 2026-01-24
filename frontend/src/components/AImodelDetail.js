import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

const AImodelDetail = () => {
  const { id } = useParams();
  const [aimodel, setAiModel] = useState(null);

  useEffect(() => {
    const fetchAIModel = async () => {
      const response = await axios.get(`${API_BASE_URL}/aimodels/${id}/`);
      setAiModel(response.data);
    };
    fetchAIModel();
  }, [id]);

  if (!aimodel) return <div>Loading...</div>;

  return (
    <div>
      <h1>{aimodel.name}</h1>
      <p>{aimodel.description}</p>
      {/* Add more details as needed */}
    </div>
  );
};

export default AImodelDetail;
