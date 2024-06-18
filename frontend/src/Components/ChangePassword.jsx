import React from 'react';
import '../styles/Model.css';

const ChangePassword = ({ show, new_password, confirm_password, onClose, onConfirm, newPasswordchange, confirmPasswordchange }) => {

  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h1>Change Password</h1>
        <p className="logout-message">Enter The New Password Below</p>
        <input
            className='logout-message inputs'
            placeholder=' New Password'
            type="password"
            value={new_password}
            onChange={newPasswordchange}
        />
        <input
            className='logout-message inputs'
            placeholder=' Confirm Password'
            type="password"
            value={confirm_password}
            onChange={confirmPasswordchange}
        />
        <div className="modal-buttons">
          <button onClick={onClose} className="cancel-button">Cancel</button>
          <button 
            onClick={onConfirm} 
            className="confirm-button"
            disabled={!new_password || new_password.toString().length < 6 || !confirm_password ||confirm_password.toString().length < 6 }
          >Submit</button>
        </div>
      </div>
    </div>
  );
};

export default ChangePassword;