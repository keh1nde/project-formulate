import React, { useState } from 'react';
import './ImportNew.css';

const ImportNew = () => {
  const [files, setFiles] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const maxFiles = 20;
  const filesPerPage = 6;

  const handleFileUpload = (event) => {
    const newFiles = Array.from(event.target.files);
    if (newFiles.length + files.length > maxFiles) {
      alert(`Maximum of ${maxFiles} files allowed.`);
    } else {
      setFiles([...files, ...newFiles]);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const newFiles = Array.from(event.dataTransfer.files);
    if (newFiles.length + files.length > maxFiles) {
      alert(`Maximum of ${maxFiles} files allowed.`);
    } else {
      setFiles([...files, ...newFiles]);
    }
  };

  const handlePageChange = (direction) => {
    if (direction === 'next' && (currentPage + 1) * filesPerPage < files.length) {
      setCurrentPage(currentPage + 1);
    } else if (direction === 'prev' && currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleSubmit = () => {
    // Send the files to the backend for processing
    console.log('Submitting files:', files);
  };

  const currentFiles = files.slice(currentPage * filesPerPage, (currentPage + 1) * filesPerPage);

  return (
    <div className="import-new" onDrop={handleDrop} onDragOver={handleDragOver}>
      <div className="close-button">X</div>
      <div className="file-container">
        {currentFiles.map((file, index) => (
          <div key={index} className="file-preview">
            {file.name}
          </div>
        ))}
      </div>

      {files.length > filesPerPage && (
        <div className="pagination">
          <button className="arrow-button" onClick={() => handlePageChange('prev')}>&lt;</button>
          <button className="arrow-button" onClick={() => handlePageChange('next')}>&gt;</button>
        </div>
      )}

      {files.length === 0 && (
        <div className="drag-drop-area">
          Drag and Drop or Select Files
        </div>
      )}

      <input
        type="file"
        multiple
        onChange={handleFileUpload}
        className="file-input"
      />

      <button className="submit-button" onClick={handleSubmit}>Go &rarr;</button>
    </div>
  );
};

export default ImportNew;
