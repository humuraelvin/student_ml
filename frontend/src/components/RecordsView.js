import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import './RecordsView.css';

function RecordsView({ refreshTrigger }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecords();
  }, [refreshTrigger]);

  const fetchRecords = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getRecords();
      setRecords(response.data);
    } catch (err) {
      setError('Failed to fetch records. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="records-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading records...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="records-container">
      <div className="records-header">
        <h2>📋 Student Performance Records</h2>
        <button onClick={fetchRecords} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {records.length === 0 ? (
        <div className="no-records">
          <p>No records found. Make some predictions first!</p>
        </div>
      ) : (
        <div className="records-table-container">
          <table className="records-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Hours Studied</th>
                <th>Previous Scores</th>
                <th>Sleep Hours</th>
                <th>Sample Papers</th>
                <th>Extracurricular</th>
                <th>Performance Index</th>
              </tr>
            </thead>
            <tbody>
              {records.map((record, index) => (
                <tr key={record.id || index} className="record-row">
                  <td className="id-cell">{record.id}</td>
                  <td>{record.hours_studied}</td>
                  <td>{record.previous_scores}%</td>
                  <td>{record.sleep_hours}</td>
                  <td>{record.sample_papers}</td>
                  <td>
                    <span className={`badge ${record.extracurricular ? 'yes' : 'no'}`}>
                      {record.extracurricular ? 'Yes' : 'No'}
                    </span>
                  </td>
                  <td className="performance-cell">
                    <span className="score-badge">{record.performance_index?.toFixed(2) || 'N/A'}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="records-footer">
        <p>Total Records: <strong>{records.length}</strong></p>
      </div>
    </div>
  );
}

export default RecordsView;
