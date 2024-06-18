import React from 'react';
import '../styles/Model.css';

const ConfirmLogout = ({ show, onClose, onConfirm }) => {
  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h1>Confirm Logout</h1>
        <p className="logout-message">Are you sure you want to logout?</p>
        <div className="modal-buttons">
          <button onClick={onClose} className="confirm-button">No</button>
          <button onClick={onConfirm} className="cancel-button">Yes</button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmLogout;