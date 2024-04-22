import LoginForm from "./pages/LoginForm/LoginForm";
import Home from './pages/Home/Home';

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <div>
      
      <Router>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/loginstudent" element={<LoginForm />} />
          
        </Routes>
      </Router>
    </div>
  );
}

export default App;
