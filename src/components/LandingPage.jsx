import React, { useState } from 'react';
import './LandingPage.css';
import ErrorPopup from "./ErrorPopup";
import ShowResults from "./ShowResults";

const LandingPage = () => {
  const [showHistory, setShowHistory] = useState(false);
  const [hasHistory, setHasHistory] = useState(false); // Simulating history presence
  const [error, setError] = useState('');
  const [results, setResults] = useState(["Result 1", "Result 2", "Result 3"]); // Placeholder Results

  // Functions to handle button clicks
  const handleCreateNew = () => {
    // Navigate to the 'import-new' component or page
    console.log('Navigating to Create New...');
  };

  const handleOpenExisting = () => {
    // Navigate to the 'import-existing' component or page
    console.log('Navigating to Open Existing...');
  };

  const handleHistoryClick = () => {
    if (hasHistory) {
      setShowHistory(!showHistory);
    } else {
      alert('Hello there');
    }

    const closeError = () => {
      setError('');
    };

    return (
        <div className="landing-page">
          <div className="history-icon" onClick={handleHistoryClick}>
            &gt;
          </div>
          { showHistory && (
              <ShowResults results={results} />
          )}

          <div className="module-container">
            <div className="module create-new" onClick={handleCreateNew}>
              <div className="img-placeholder">IMG</div>
              <div className="module-label">Create New:</div>
            </div>
            <div className="module open-existing" onClick={handleOpenExisting}>
              <div className="img-placeholder">IMG</div>
              <div className="module-label">Open Existing:</div>
            </div>
          </div>

          <footer className="footer">
            <div className="formulate-button" onClick={() => window.location.reload()}>Formulate</div>
            <div className="github-button">
              <a href="https://github.com/keh1nde" target="_blank" rel="noopener noreferrer">GITHUB</a>
            </div>
          </footer>

          <ErrorPopup message={error} onClose={closeError}/>
        </div>
    );
  };
};
export default LandingPage;

