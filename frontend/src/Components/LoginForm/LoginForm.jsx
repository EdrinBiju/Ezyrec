import React from 'react';
import logo from './1503647889cover.webp'
import './LoginForm.css';
import { FaUser, FaLock } from "react-icons/fa";

const LoginForm = () => {
  return (
    <div className="login-content">
        <img src={logo} alt='logo' />
    <div className='wrapper'>
      
        <form action="">
        
          <h1>Students Login</h1>
          <div className="input-box">
            <input type="text" placeholder='Username' required />
            <FaUser className='icon' />
          </div>
          <div className="input-box">
            <input type="password" placeholder='Password' required />
            <FaLock className='icon' />
          </div>

          <div className="remember-forget">
            <label><input type="checkbox" />Remember Me</label>
            <a href="reset password">Forget Password?</a>
          </div>

          <button type="submit">Login</button>

          {/* <div className="register-link">
            <p>Don't have an Account? <a href="#">Register</a></p>
          </div> */}
        </form>

      </div>
    </div>
    
  )
}

export default LoginForm;