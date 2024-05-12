import React from 'react'
import "../../styles/Certificates.css";
import { IoAdd } from "react-icons/io5";
import { Link } from "react-router-dom";

const Certificates = () => {

  return (
    <div className="user-content-section">
      <div className="user-content-heading">
        <div className="heading">
          <h2>All Certificates</h2>
        </div>
        <div className="btn">
          <button className="add-new-certificate">
            <Link
              to="/studenthome"
              style={{ textDecoration: "none", color: "white" }}
            >
              <IoAdd
                style={{
                  fontSize: 17,
                  paddingRight: 5,
                }}
              />
              Add Certificate
            </Link>
          </button>
        </div>
      </div>
      <hr />
      <div className="user-content-item"></div>
    </div>
  )
}

export default Certificates