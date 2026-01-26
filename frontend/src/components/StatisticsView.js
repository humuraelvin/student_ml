import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import './StatisticsView.css';

function StatisticsView({ refreshTrigger }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatistics();
  }, [refreshTrigger]);

  const fetchStatistics = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getStatistics();
      setStats(response.data);
    } catch (err) {
      setError('Failed to fetch statistics. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="statistics-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading statistics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="statistics-container">
        <div className="error-message">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="statistics-container">
        <div className="no-data">
          <p>No statistics available yet.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-container">
      <div className="stats-header">
        <h2>📊 Performance Statistics</h2>
        <button onClick={fetchStatistics} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      <div className="stats-grid">
        <StatCard
          icon="📈"
          label="Average Performance"
          value={stats.average_performance?.toFixed(2) || 'N/A'}
          unit=""
        />
        <StatCard
          icon="📊"
          label="Median Performance"
          value={stats.median_performance?.toFixed(2) || 'N/A'}
          unit=""
        />
        <StatCard
          icon="⬆️"
          label="Highest Score"
          value={stats.max_performance?.toFixed(2) || 'N/A'}
          unit=""
        />
        <StatCard
          icon="⬇️"
          label="Lowest Score"
          value={stats.min_performance?.toFixed(2) || 'N/A'}
          unit=""
        />
        <StatCard
          icon="📚"
          label="Total Records"
          value={stats.total_records || '0'}
          unit="predictions"
        />
        <StatCard
          icon="⏱️"
          label="Avg Study Hours"
          value={stats.average_hours_studied?.toFixed(1) || 'N/A'}
          unit="hours"
        />
      </div>

      <div className="insights-section">
        <h3>💡 Key Insights</h3>
        <div className="insights-list">
          {stats.average_performance && (
            <InsightItem
              title="Performance Range"
              description={`Students score between ${stats.min_performance?.toFixed(2)} and ${stats.max_performance?.toFixed(2)}`}
            />
          )}
          {stats.average_hours_studied && (
            <InsightItem
              title="Study Time"
              description={`Average study hours: ${stats.average_hours_studied?.toFixed(1)} hours per week`}
            />
          )}
          <InsightItem
            title="Model Status"
            description="ML model is actively making predictions for student performance"
          />
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, unit }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <div className="stat-value">{value}</div>
        <div className="stat-label">{label}</div>
        {unit && <div className="stat-unit">{unit}</div>}
      </div>
    </div>
  );
}

function InsightItem({ title, description }) {
  return (
    <div className="insight-item">
      <h4>{title}</h4>
      <p>{description}</p>
    </div>
  );
}

export default StatisticsView;
