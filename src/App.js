import './App.css';
import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import LandingPage from "./components/LandingPage";
import ImportNew from "./components/ImportNew";
import ShowResults from "./components/ShowResults";

function App() {
    return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/import-new" element={< ImportNew />} />
          <Route path="/show-results" element={< ShowResults />} />
        </Routes>
      </div>
    </Router>
    )
}

export default App;
