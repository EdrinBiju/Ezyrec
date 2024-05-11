import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './pages/Home/Home';
import LoginStudent from "./pages/LoginForm/LoginStudent";
import LoginFaculty from "./pages/LoginForm/LoginFaculty";
import StudentHome from "./pages/Student/Student";

function App() {
  return (
    <div>
      
      <Router>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/loginstudent" element={<LoginStudent />} />
          <Route path="/loginfaculty" element={<LoginFaculty />} />
          <Route path="/studenthome" element={<StudentHome />} />
          
        </Routes>
      </Router>
    </div>
  );
}

export default App;
