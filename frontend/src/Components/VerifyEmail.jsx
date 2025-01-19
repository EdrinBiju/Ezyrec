import React from 'react';
import '../styles/Model.css';

const VerifyEmail = ({ show, otp, onClose, onConfirm, otpchange}) => {

  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h1>Verify Email</h1>
        <p className="logout-message">An OTP is send to your email.</p>
        <input
            className='logout-message inputs'
            placeholder='Enter OTP'
            type="otp"
            value={otp}
            onChange={otpchange}
            required
        />
        <div className="modal-buttons">
          <button onClick={onClose} className="cancel-button">Cancel</button>
          <button onClick={onConfirm} className="confirm-button" disabled={!otp || otp.toString().length !== 6 }>Submit</button>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmail;