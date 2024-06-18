import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import logo from '../../assets/banner.png';
import '../../styles/Login.css';
import { FaUser, FaLock } from "react-icons/fa";

const LoginFaculty = () => {
  const navigate = useNavigate(); // Initialize useNavigate

  const [facultyid, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/facultylogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ facultyid, password }),
      });

      if (response.ok) {
        sessionStorage.setItem('facultyid',facultyid);
        navigate('/facultyhome');
      } else {
        // Display error message for wrong credentials
        setError('Invalid faculty ID or password.');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('An unexpected error occurred. Please try again later.');
    }
  };

  return (
    <div className='login-content'>
      <img src={logo} alt='logo' />
      <div className='wrapper'>
        <form onSubmit={handleSubmit}>
          <h1>Faculty Login</h1>
          <div className="input-box">
            <input 
              type="text" 
              placeholder='Faculty Id' 
              autoComplete="username" 
              value={facultyid} 
              onChange={handleUsernameChange} 
              required 
            />
            <FaUser className='icon' />
          </div>
          <div className="input-box">
            <input 
              type="password" 
              placeholder='Password' 
              autoComplete="current-password"
              value={password} 
              onChange={handlePasswordChange} 
              required 
            />
            <FaLock className='icon' />
          </div>

          {/* <div className="remember-forget">
            <label><input type="checkbox" />Remember Me</label>
            <a href="reset password">Forget Password?</a>
          </div> */}

          {error && <p className="error">{error}</p>}

          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default LoginFaculty;
