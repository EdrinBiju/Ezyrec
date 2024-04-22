import React from 'react';
import '../../styles/Home.css';
import '../../styles/nicepage.css';

function Home() {
    return (
      <div>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta charSet="utf-8" />
      <meta name="description" content />
      <title>Home</title>
      <link rel="stylesheet" href="nicepage.css" media="screen" />
      <link rel="stylesheet" href="Home.css" media="screen" />
      <link id="u-theme-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,500,500i,700,700i,900,900i|Open+Sans:300,300i,400,400i,500,500i,600,600i,700,700i,800,800i" />
      <link id="u-page-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Merriweather:300,300i,400,400i,700,700i,900,900i" />
      <meta name="theme-color" content="#9b74ea" />
      <meta property="og:title" content="Home" />
      <meta property="og:type" content="website" />
      <meta data-intl-tel-input-cdn-path="intlTelInput/" />
      <section className="u-align-center u-clearfix u-image u-shading u-section-1" src data-image-width={1280} data-image-height={1183} id="carousel_642d">
        <div className="u-clearfix u-sheet u-sheet-1">
          <h1 className="u-align-center u-custom-font u-font-merriweather u-text u-text-default-lg u-text-default-md u-text-default-xl u-title u-text-1"> EZYREC</h1>
          <h5 className="u-custom-font u-font-merriweather u-text u-text-default u-text-2"> an easy solution for students and faculties</h5>
          <div className="u-expanded-width-lg u-expanded-width-md u-expanded-width-sm u-expanded-width-xs u-list u-list-1">
            <div className="u-repeater u-repeater-1">
              <div className="u-align-left u-container-style u-list-item u-repeater-item">
                <div className="u-container-layout u-similar-container u-valign-middle u-container-layout-1">
                  <a href="" className="u-border-none u-btn u-btn-round u-button-style u-hover-palette-3-light-2 u-palette-3-base u-radius-50 u-btn-1">faculty login </a>
                </div>
              </div>
              <div className="u-align-left u-container-style u-list-item u-repeater-item">
                <div className="u-container-layout u-similar-container u-valign-middle u-container-layout-2">
                  <a href="/loginstudent" className="u-border-none u-btn u-btn-round u-button-style u-hover-palette-3-light-2 u-palette-3-base u-radius-50 u-btn-2">student login </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    );
  };
export default Home;