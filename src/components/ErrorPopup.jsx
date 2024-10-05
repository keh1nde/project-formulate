import React from 'react';
import './ErrorPopup.css'; // Assuming you will use external CSS for styling

const ErrorPopup = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="error-popup-overlay">
      <div className="error-popup">
        <div className="error-message"> Error: {message}</div>
        <button className="close-button" onClick={onClose}>X</button>
      </div>
    </div>
  );
};

export default ErrorPopup;