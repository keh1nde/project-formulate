import React, { useState } from 'react';
import './ShowResults.css';

const ShowResults = ({ results }) => {
  const [selectedResult, setSelectedResult] = useState(null);

  const handleResultClick = (index) => {
    setSelectedResult(results[index]);
  };

  return (
    <div className="show-results">
      <div className="history-icon">
        &gt;
      </div>
      <div className="results-container">
        <div className="results-list">
          {results.map((result, index) => (
            <div
              key={index}
              className={`result-item ${selectedResult === result ? 'selected' : ''}`}
              onClick={() => handleResultClick(index)}
            >
              {index + 1}
            </div>
          ))}
        </div>
        <div className="result-display">
          {selectedResult ? (
            <textarea
              readOnly
              value={selectedResult}
              className="result-textbox"
            />
          ) : (
            <div className="placeholder">Click each page to see its output</div>
          )}
        </div>
      </div>
      <footer className="footer">
        <div className="formulate-button" onClick={() => window.location.reload()}>Formulate</div>
        <div className="github-button">
          <a href="https://github.com/your-repo-url" target="_blank" rel="noopener noreferrer">GITHUB</a>
        </div>
      </footer>
    </div>
  );
};

export default ShowResults;