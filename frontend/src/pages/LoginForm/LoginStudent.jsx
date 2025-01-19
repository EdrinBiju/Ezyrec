import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/banner.png';
import '../../styles/Login.css';
import { FaUser, FaLock } from "react-icons/fa";

const LoginStudent = () => {
  const navigate = useNavigate(); // Initialize useHistory
  
  const [regno, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const [isFetching, setIsFetching] = useState(false);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    if (isFetching) return; 
    console.log("login")
    setIsFetching(true);
    e.preventDefault();

    try {
      console.log('request')
      const response = await fetch('http://127.0.0.1:5000/studentlogin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ regno, password }),
      });
      console.log("response")
      if (response.ok) {
        sessionStorage.setItem('regno', regno);
        navigate('/studenthome');
        
        setIsFetching(false); 
      } else {
        // Display error message for wrong credentials
        setError('Invalid student ID or password.');
        
        setIsFetching(false);
      }
    } catch (error) {
      console.error('Error:', error);
      
      setIsFetching(false);
      setError('An unexpected error occurred. Please try again later.');
    }
  };

  return (
    <div className='login-content'>
      <img src={logo} alt='logo' />
      <div className='wrapper'>
        <form onSubmit={handleSubmit}>
          <h1>Students Login</h1>
          <div className="input-box">
            <input 
              type="text" 
              placeholder='Register Number'
              autoComplete="username" 
              value={regno} 
              onChange={handleUsernameChange} 
              required 
            />
            <FaUser className='icon' />
          </div>
          <div className="input-box">
            <input 
              type="password" 
              autoComplete="current-password"
              placeholder='Password' 
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

export default LoginStudent;
