import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import Form from './Form';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed
const DynamicForm = ({ actions }) => {
  const { modelid } = useParams();
  const [formFields, setFormFields] = useState({});
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [errors, setErrors] = useState({});
  const [explanation, setExplanation] = useState(null);
  const [queryId, setQueryId] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE_URL}/dynamic-form/${modelid}/`)
      .then(response => {
        setFormFields(response.data.form);
      })
      .catch(error => {
        console.error('There was an error fetching the form schema!', error);
      });
  }, [modelid]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData({
      ...formData,
      [name]: files ? files[0] : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formDataToSend = new FormData();
    for (const key in formData) {
      formDataToSend.append(key, formData[key]);
    }

    axios.post(`${API_BASE_URL}/dynamic-form/${modelid}/`, formDataToSend)
      .then(response => {
        setResult(response.data.result);
        setErrors({});
        setExplanation(null);  // Reset explanation when a new result is fetched
        setQueryId(response.data.query_id);  // Store the query_id 
        actions.handleFormSubmit(response.data.result,response.data.query_id)
        //sendBotMessage()
      })
      .catch(error => {
        if (error.response && error.response.data) {
          setErrors(error.response.data.errors);
        } else {
          console.error('There was an error submitting the form!', error);
        }
      });
  };

  const getExplanation = () => {
    if (!queryId) {
      console.error('Query ID is not available.');
      return;
    }
  };

  return (
    <div>
      <Form
        formFields={formFields}
        handleChange={handleChange}
        handleSubmit={handleSubmit}
        errors={errors}
      />
      {/* {result && <Result result={result}  />} */}
    </div>
  );
};

export default DynamicForm;
