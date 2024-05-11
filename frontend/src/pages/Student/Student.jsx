import React from 'react'
import Home from '../Home/HomeStudent';
import Results from '../Results/Results';
import Certificates from '../Certificates/Certificates';
import StudentProfile from '../Profile/StudentProfile';

const Student = () => {
  return (
    <div>
        <ul className="nav nav-tabs justify-content-center" id="myTab" role="tablist">
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
      </div>
    </div>
  )
}

export default Student
