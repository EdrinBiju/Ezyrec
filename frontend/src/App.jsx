import LoginForm from "./pages/LoginForm/LoginForm";
import Home from './pages/Home/Home';
// import Logout from './pages/LogoutConfirm';

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import HomePage from "./pages/HomePage";
// import Academic from "./pages/Academic";

function App() {
  return (
    <div>
      
      <Router>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/loginstudent" element={<LoginForm />} />
          {/* <Route path="/HomePage" element={<HomePage />} />
          <Route path="/Academic" element={<Academic />} />
          <Route path="/loginstudent" element={<Logout />} />
           */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
