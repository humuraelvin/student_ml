import React, { useState } from 'react';
import { api } from '../api/client';
import './PredictionForm.css';

function PredictionForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    hours_studied: 5,
    previous_scores: 75,
    extracurricular: false,
    sleep_hours: 7,
    sample_papers: 2,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : parseInt(value) || value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // CLIENT-SIDE VALIDATION: Check if hours_studied + sleep_hours > 24
    if (formData.hours_studied + formData.sleep_hours > 24) {
      setError(`❌ Physics check failed: Study (${formData.hours_studied}h) + Sleep (${formData.sleep_hours}h) = ${formData.hours_studied + formData.sleep_hours}h exceeds 24 hours in a day. A day only has 24 hours!`);
      setLoading(false);
      return;
    }

    try {
      const response = await api.predict(formData);
      setResult(response.data);
      onSuccess();
    } catch (err) {
      setError(
        err.response?.data?.error ||
        'Failed to make prediction. Please ensure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-container">
      <div className="form-section">
        <h2>📝 Enter Student Information</h2>
        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-group">
            <label htmlFor="hours_studied">Hours Studied (per week)</label>
            <input
              type="range"
              id="hours_studied"
              name="hours_studied"
              min="0"
              max="24"
              value={formData.hours_studied}
              onChange={handleChange}
              className="slider"
            />
            <span className="value-display">{formData.hours_studied} hours</span>
          </div>

          <div className="form-group">
            <label htmlFor="previous_scores">Previous Scores</label>
            <input
              type="range"
              id="previous_scores"
              name="previous_scores"
              min="0"
              max="100"
              value={formData.previous_scores}
              onChange={handleChange}
              className="slider"
            />
            <span className="value-display">{formData.previous_scores}%</span>
          </div>

          <div className="form-group">
            <label htmlFor="sleep_hours">Sleep Hours (per night)</label>
            <input
              type="range"
              id="sleep_hours"
              name="sleep_hours"
              min="0"
              max="12"
              value={formData.sleep_hours}
              onChange={handleChange}
              className="slider"
            />
            <span className="value-display">{formData.sleep_hours} hours</span>
          </div>

          <div className="form-group">
            <label htmlFor="sample_papers">Sample Papers Solved</label>
            <input
              type="range"
              id="sample_papers"
              name="sample_papers"
              min="0"
              max="10"
              value={formData.sample_papers}
              onChange={handleChange}
              className="slider"
            />
            <span className="value-display">{formData.sample_papers} papers</span>
          </div>

          <div className="form-group checkbox">
            <input
              type="checkbox"
              id="extracurricular"
              name="extracurricular"
              checked={formData.extracurricular}
              onChange={handleChange}
            />
            <label htmlFor="extracurricular">Participates in Extracurricular Activities</label>
          </div>

          <div className="constraint-warning" style={{ color: formData.hours_studied + formData.sleep_hours > 24 ? '#ff6b6b' : '#ffc107', fontWeight: 'bold', marginBottom: '15px' }}>
            ⏰ Study Hours + Sleep Hours = {formData.hours_studied + formData.sleep_hours}/24 hours
            {formData.hours_studied + formData.sleep_hours > 24 && ' ❌ EXCEEDS 24 HOURS!'}
          </div>

          <button type="submit" disabled={loading || (formData.hours_studied + formData.sleep_hours > 24)} className="submit-btn">
            {loading ? '🔄 Predicting...' : '🚀 Make Prediction'}
          </button>
        </form>
      </div>

      {result && (
        <div className="result-section success">
          <h2>✅ Prediction Result</h2>
          <div className="result-box">
            <div className="prediction-score">
              <div className="score-value">{result.predicted_performance_index}</div>
              <div className="score-label">Performance Index</div>
            </div>
            <div className="result-details">
              <h3>Input Features Used:</h3>
              <ul>
                <li><strong>Hours Studied:</strong> {result.input_features.hours_studied} hours</li>
                <li><strong>Previous Scores:</strong> {result.input_features.previous_scores}%</li>
                <li><strong>Sleep Hours:</strong> {result.input_features.sleep_hours} hours</li>
                <li><strong>Sample Papers:</strong> {result.input_features.sample_papers}</li>
                <li><strong>Extracurricular:</strong> {result.input_features.extracurricular ? 'Yes' : 'No'}</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="result-section error">
          <h2>❌ Error</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;
