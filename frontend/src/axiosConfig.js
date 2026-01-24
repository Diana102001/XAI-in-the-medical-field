// src/axiosConfig.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000/', // Replace with your Django API base URL
  withCredentials: true, // Include if you are using cookies for authentication
});

export default instance;
