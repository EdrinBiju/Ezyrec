import LoginForm from "./pages/LoginForm/LoginForm";
import LoginForm2 from "./pages/LoginForm/LoginForm2";
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
          <Route path="/loginfaculty" element={<LoginForm2 />} />
          
        </Routes>
      </Router>
    </div>
  );
}

export default App;
