import axios from 'axios';

// Always connect to backend on port 8000 (regardless of where frontend is running)
const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

export const api = {
  predict: (data) => apiClient.post('/predict/', data),
  getRecords: () => apiClient.get('/records/'),
  getStatistics: () => apiClient.get('/statistics/'),
};

export default apiClient;
