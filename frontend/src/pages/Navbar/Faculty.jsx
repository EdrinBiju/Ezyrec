import React, { useState } from 'react';
import Home from '../Home/Home';
import Results from '../Results/FacultyResults';
import FacultyCertificates from '../Certificates/FacultyCertificates';
import FacultyProfile from '../Profile/FacultyProfile';
import '../../styles/Student.css';
import { useNavigate } from 'react-router-dom';
import ConfirmLogout from '../../Components/ConfirmLogout';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDoorOpen } from '@fortawesome/free-solid-svg-icons';
// import { faSignOutAlt,faPowerOff,faArrowRightFromBracket,faDoorOpen,faRunning } from '@fortawesome/free-solid-svg-icons';

const Faculty = () => {
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [activeTab, setActiveTab] = useState('home');
  const facultyId = sessionStorage.getItem('facultyid');

  const handleLogout = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleConfirmLogout = () => {
    setShowModal(false);
    sessionStorage.clear();
    navigate('/home');
  };

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div>
      { facultyId ? (
        <div className='studentsite'>
          <ul className="nav nav-pills nav-justified justify-content-center fs-3" id="pills-tab" role="tablist">
            <li className="nav-item" role="presentation">
              <button className={`nav-link ${activeTab === 'home' ? 'active' : ''}`} onClick={() => handleTabClick('home')}>Home</button>
            </li>
            <li className="nav-item" role="presentation">
              <button className={`nav-link ${activeTab === 'results' ? 'active' : ''}`} onClick={() => handleTabClick('results')}>Results</button>
            </li>
            <li className="nav-item" role="presentation">
              <button className={`nav-link ${activeTab === 'certificates' ? 'active' : ''}`} onClick={() => handleTabClick('certificates')}>Certificates</button>
            </li>
            <li className="nav-item" role="presentation">
              <button className={`nav-link ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => handleTabClick('profile')}>Profile</button>
            </li>
            <li className='logout-container'>
              <button className="logout-button" onClick={handleLogout}><FontAwesomeIcon icon={faDoorOpen}/> Logout</button>
            </li>
          </ul>
          <ConfirmLogout show={showModal} onClose={handleCloseModal} onConfirm={handleConfirmLogout} />
          <div className="tab-content" id="myTabContent">
            <div className={`tab-pane fade ${activeTab === 'home' ? 'show active' : ''}`} id="pills-home" role="tabpanel" aria-labelledby="pills-home">
              {activeTab === 'home' && <Home />}
            </div>
            <div className={`tab-pane fade ${activeTab === 'results' ? 'show active' : ''}`} id="pills-result" role="tabpanel" aria-labelledby="pills-result">
              {activeTab === 'results' && <Results />}
            </div>
            <div className={`tab-pane fade ${activeTab === 'certificates' ? 'show active' : ''}`} id="pills-certificates" role="tabpanel" aria-labelledby="pills-certificates">
              {activeTab === 'certificates' && <FacultyCertificates />}
            </div>
            <div className={`tab-pane fade ${activeTab === 'profile' ? 'show active' : ''}`} id="pills-profile" role="tabpanel" aria-labelledby="pills-profile">
              {activeTab === 'profile' && <FacultyProfile />}
            </div>
          </div>
        </div>
      ):(
        <div className='please-login'>
          <a href="/loginfaculty">Please Login</a>
        </div>
      )}
    </div>
  );
};

export default Faculty;

