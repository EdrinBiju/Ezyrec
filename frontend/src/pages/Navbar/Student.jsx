// import React, { useState } from 'react'
// import Home from '../Home/Home';
// import Results from '../Results/Results';
// import Certificates from '../Certificates/Certificates';
// import StudentProfile from '../Profile/StudentProfile';
// import '../../styles/Student.css';
// import { useNavigate } from 'react-router-dom';
// import Modal from './Modal';

// const Student = () => {
//   const navigate = useNavigate();
//   const [showModal, setShowModal] = useState(false);

//   const handleLogout = () => {
//     setShowModal(true);
//   };

//   const handleCloseModal = () => {
//     setShowModal(false);
//   };

//   const handleConfirmLogout = () => {
//     setShowModal(false);
//     navigate('/home');
//   };
//   return (
//     <div className='studentsite'>
//       <ul className="nav nav-pills nav-justified justify-content-center fs-3" id="pills-tab" role="tablist">
//         <li className="nav-item" role="presentation">
//           <button className="nav-link active" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" >Home</button>
//         </li>
//         <li className="nav-item" role="presentation">
//           <button className="nav-link" id="pills-result-tab" data-bs-toggle="pill" data-bs-target="#pills-result" type="button" role="tab" aria-controls="pills-result" >Results</button>
//         </li>
//         <li className="nav-item" role="presentation">
//           <button className="nav-link" id="pills-certificates-tab" data-bs-toggle="pill" data-bs-target="#pills-certificates" type="button" role="tab" aria-controls="pills-certificates" >Certificates</button>
//         </li>
//         <li className="nav-item" role="presentation">
//           <button className="nav-link" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" >Profile</button>
//         </li>
//         <li className='logout-container'>
//           <button className="logout-button" onClick={handleLogout}>Logout</button>
//         </li>
//       </ul>
//       <Modal show={showModal} onClose={handleCloseModal} onConfirm={handleConfirmLogout} />
//       <div className="tab-content" id="myTabContent">
//         <div className="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home" tabIndex={0}>
//           <Home/>
//         </div>
//         <div className="tab-pane fade" id="pills-result" role="tabpanel" aria-labelledby="pills-result" tabIndex={0}>
//           <Results/>
//         </div>
//         <div className="tab-pane fade" id="pills-certificates" role="tabpanel" aria-labelledby="pills-certificates" tabIndex={0}>
//           <Certificates/>
//         </div>
//         <div className="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile" tabIndex={0}>
//           <StudentProfile/>
//         </div>
//       </div>
//     </div>

//   )
// }

// export default Student

import React, { useState } from 'react';
import Home from '../Home/Home';
import Results from '../Results/StudentResults';
import StudentCertificates from '../Certificates/StudentCertificates';
import StudentProfile from '../Profile/StudentProfile';
import '../../styles/Student.css';
import { useNavigate } from 'react-router-dom';
import ConfirmLogout from '../../Components/ConfirmLogout';
import '@fortawesome/fontawesome-free/css/all.min.css';

const Student = () => {
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [activeTab, setActiveTab] = useState('home');
  const reg_no = sessionStorage.getItem('regno');

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
      { reg_no ? (
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
              <button className="logout-button" onClick={handleLogout}><i className="fas fa-external-link-alt"></i> Logout</button>
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
              {activeTab === 'certificates' && <StudentCertificates />}
            </div>
            <div className={`tab-pane fade ${activeTab === 'profile' ? 'show active' : ''}`} id="pills-profile" role="tabpanel" aria-labelledby="pills-profile">
              {activeTab === 'profile' && <StudentProfile />}
            </div>
          </div>
        </div>
      ):(
        <div className='please-login'>
          <a href="/loginstudent">Please Login</a>
        </div>
      )}
    </div>
  );
};

export default Student;

