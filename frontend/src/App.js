import React, { useState } from 'react';
import './App.css';
import PredictionForm from './components/PredictionForm';
import RecordsView from './components/RecordsView';
import StatisticsView from './components/StatisticsView';

function App() {
  const [activeTab, setActiveTab] = useState('predict');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handlePredictionSuccess = () => {
    // Refresh records and statistics after successful prediction
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📚 Student Performance Predictor</h1>
          <p>AI-Powered ML Prediction System</p>
        </div>
      </header>

      <nav className="navigation">
        <button
          className={`nav-btn ${activeTab === 'predict' ? 'active' : ''}`}
          onClick={() => setActiveTab('predict')}
        >
          🔮 Make Prediction
        </button>
        <button
          className={`nav-btn ${activeTab === 'records' ? 'active' : ''}`}
          onClick={() => setActiveTab('records')}
        >
          📋 All Records
        </button>
        <button
          className={`nav-btn ${activeTab === 'statistics' ? 'active' : ''}`}
          onClick={() => setActiveTab('statistics')}
        >
          📊 Statistics
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'predict' && (
          <PredictionForm onSuccess={handlePredictionSuccess} />
        )}
        {activeTab === 'records' && (
          <RecordsView refreshTrigger={refreshTrigger} />
        )}
        {activeTab === 'statistics' && (
          <StatisticsView refreshTrigger={refreshTrigger} />
        )}
      </main>

      <footer className="app-footer">
        <p>Student Performance ML API • Django + React • 2025</p>
      </footer>
    </div>
  );
}

export default App;
