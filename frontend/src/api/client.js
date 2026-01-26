import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  predict: (data) => apiClient.post('/predict/', data),
  getRecords: () => apiClient.get('/records/'),
  getStatistics: () => apiClient.get('/statistics/'),
};

export default apiClient;
