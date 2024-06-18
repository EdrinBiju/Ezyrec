import React from 'react';
import '../../styles/ProjectHome.css';
import '../../assets/library.png'; 

function Home() {
  return (
      <div className="home-container">
          <section className="home-section">
                  <h1 className="home-title u-font-merriweather">EZYREC</h1>
                  <h5 className="home-subtitle u-font-merriweather">AN EASY SOLUTION FOR STUDENTS AND FACULTIES</h5>
                  <div className="button-container">
                    <div className='button-box'>
                        <a href="/loginfaculty" className="login-route-button u-font-merriweather">FACULTY LOGIN</a>
                    </div>
                    <div className='button-box'>
                        <a href="/loginstudent" className="login-route-button u-font-merriweather">STUDENT LOGIN</a>
                    </div> 
                  </div>
          </section>
      </div>
  );
}

export default Home;