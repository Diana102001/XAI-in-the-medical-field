import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Layout from './Layout'; // Adjust the import path as necessary
import './AImodelsList.css';

const API_BASE_URL = 'http://localhost:8000';

const AImodelsList = () => {
  const [aimodels, setAiModels] = useState([]);

  useEffect(() => {
    const fetchAIModels = async () => {
      const response = await axios.get(`${API_BASE_URL}/aimodels/`);
      setAiModels(response.data);
    };
    fetchAIModels();
  }, []);

  return (
    <Layout>
      <div className="aimodels-container">
        <h1>Choose usecase</h1>
        <div className="card-list">
          {aimodels.map((aimodel) => (
            <div key={aimodel.id} className="card">
              <h2>{aimodel.name}</h2>
              <Link to={`${'http://localhost:3000'}/usecase/${aimodel.id}`} className="button">Try this case</Link>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
};

export default AImodelsList;
