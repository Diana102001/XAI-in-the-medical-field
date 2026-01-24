// src/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

export const fetchAIModels = () => {
    return axios.get(`${API_BASE_URL}/aimodels/`);
};

export const fetchModelVersions = (modelId) => {
    return axios.get(`${API_BASE_URL}/aimodels/${modelId}/modelvs/`);
};

export const fetchDynamicFormFields = (modelVersionId) => {
    return axios.get(`${API_BASE_URL}/DynamicForm/${modelVersionId}/`);
};

export const createQuery = (modelVersionId,data) => {
    return axios.post(`${API_BASE_URL}/DynamicForm/${modelVersionId}/`, data);
};

export const fetchExplanation = (queryId) => {
    return axios.get(`${API_BASE_URL}/query-explanation/${queryId}/`);
};
