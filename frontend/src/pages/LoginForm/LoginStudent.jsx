import React, { useState } from 'react';
import logo from '../../assets/banner.png';
import '../../styles/Login.css';
import { FaUser, FaLock } from "react-icons/fa";

const LoginStudent = () => {
  
  const [username, setUsername] = useState('');
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
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Handle successful login, e.g., redirect to student dashboard
        console.log(data.message); // Print success message
      } else {
        const data = await response.json();
        setError(data.message);
      }
    } catch (error) {
      console.error('Error:', error);
      setError('An unexpected error occurred. Please try again later.');
    }
  };

  return (
    // <div className='login-content'>
    //     <img src={logo} alt='logo' />
    //     <div className='wrapper'>
        
    //       <form action="">
          
    //         <h1>Students Login</h1>
    //         <div className="input-box">
    //           <input type="text" placeholder='Username' required />
    //           <FaUser className='icon' />
    //         </div>
    //         <div className="input-box">
    //           <input type="password" placeholder='Password' required />
    //           <FaLock className='icon' />
    //         </div>

    //         <div className="remember-forget">
    //           <label><input type="checkbox" />Remember Me</label>
    //           <a href="reset password">Forget Password?</a>
    //         </div>

    //         <button type="submit" href="/studenthome">Login</button>
            
    //       </form>

    //     </div>
    // </div>
    <div className='login-content'>
    <img src={logo} alt='logo' />
    <div className='wrapper'>
      <form onSubmit={handleSubmit}>
        <h1>Students Login</h1>
        <div className="input-box">
          <input 
            type="text" 
            placeholder='Username' 
            value={username} 
            onChange={handleUsernameChange} 
            required 
          />
          <FaUser className='icon' />
        </div>
        <div className="input-box">
          <input 
            type="password" 
            placeholder='Password' 
            value={password} 
            onChange={handlePasswordChange} 
            required 
          />
          <FaLock className='icon' />
        </div>

        <div className="remember-forget">
          <label><input type="checkbox" />Remember Me</label>
          <a href="reset password">Forget Password?</a>
        </div>

        {error && <p className="error">{error}</p>}

        <button type="submit">Login</button>
      </form>
    </div>
  </div>
    
  )
}

export default LoginStudent;