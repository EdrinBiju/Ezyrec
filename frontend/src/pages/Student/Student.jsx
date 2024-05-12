import React from 'react'
import Home from '../Home/HomeStudent';
import Results from '../Results/Results';
import Certificates from '../Certificates/Certificates';
import StudentProfile from '../Profile/StudentProfile';
import '../../styles/Student.css';

const Student = () => {
  return (
    <div className='studentsite'>
        {/* <ul className="nav nav-tabs justify-content-center fs-4" id="myTab" role="tablist">
        <li className="nav-item" role="presentation">
          <button className="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#home-tab-pane" type="button" role="tab" aria-controls="home-tab-pane" aria-selected="true">Home</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="result-tab" data-bs-toggle="tab" data-bs-target="#result-tab-pane" type="button" role="tab" aria-controls="result-tab-pane" aria-selected="false">Results</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="certificates-tab" data-bs-toggle="tab" data-bs-target="#certificates-tab-pane" type="button" role="tab" aria-controls="certificates-tab-pane" aria-selected="false">Certificates</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile-tab-pane" type="button" role="tab" aria-controls="profile-tab-pane" aria-selected="false">Profile</button>
        </li>
      </ul>
      <div className="tab-content" id="myTabContent">
        <div className="tab-pane fade show active" id="home-tab-pane" role="tabpanel" aria-labelledby="home-tab" tabIndex={0}>
          <Home/>
        </div>
        <div className="tab-pane fade" id="result-tab-pane" role="tabpanel" aria-labelledby="result-tab" tabIndex={0}>
          <Results/>
        </div>
        <div className="tab-pane fade" id="certificates-tab-pane" role="tabpanel" aria-labelledby="certificates-tab" tabIndex={0}>
          <Certificates/>
        </div>
        <div className="tab-pane fade" id="profile-tab-pane" role="tabpanel" aria-labelledby="profile-tab" tabIndex={0}>
          <StudentProfile/>
        </div>
      </div> */}
      <ul className="nav nav-pills justify-content-center fs-4" id="pills-tab" role="tablist">
        <li className="nav-item" role="presentation">
          <button className="nav-link active" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">Home</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="pills-result-tab" data-bs-toggle="pill" data-bs-target="#pills-result" type="button" role="tab" aria-controls="pills-result" aria-selected="false">Results</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="pills-certificates-tab" data-bs-toggle="pill" data-bs-target="#pills-certificates" type="button" role="tab" aria-controls="pills-certificates" aria-selected="false">Certificates</button>
        </li>
        <li className="nav-item" role="presentation">
          <button className="nav-link" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" aria-selected="false">Profile</button>
        </li>
      </ul>
      <div className="tab-content" id="myTabContent">
        <div className="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home" tabIndex={0}>
          <Home/>
        </div>
        <div className="tab-pane fade" id="pills-result" role="tabpanel" aria-labelledby="pills-result" tabIndex={0}>
          <Results/>
        </div>
        <div className="tab-pane fade" id="pills-certificates" role="tabpanel" aria-labelledby="pills-certificates" tabIndex={0}>
          <Certificates/>
        </div>
        <div className="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile" tabIndex={0}>
          <StudentProfile/>
        </div>
      </div>
    </div>
  )
}

export default Student
