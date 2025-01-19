import React from 'react';
import '../styles/Model.css';

const Loading = ({ show }) => {
  if (!show) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <p type='loading'>
        Loading...
        This may take few minutes.
      </p>
    </div>
  );
};

export default Loading;