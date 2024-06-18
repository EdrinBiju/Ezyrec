import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../../styles/Profile.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import VerifyEmail from '../../Components/VerifyEmail';
import ChangePassword from '../../Components/ChangePassword';

const FacultyProfile = () => {
  const [faculty, setFaculty] = useState(null);
  const facultyId = sessionStorage.getItem('facultyid');
  const fileInputRef = useRef(null);
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [email, setEmail] = useState("");
  const [isEditingPassword, setIsEditingPassword] = useState(false);
  const [password, setPassword] = useState("");
  const [showEmailModal, setshowEmailModal] = useState(false);
  const [showPasswordModal, setshowPasswordModal] = useState(false);
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");


  useEffect(() => {
    const fetchFacultyProfile = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/faculty/${facultyId}`);
        setFaculty(response.data);
        setEmail(response.data.email || "");
      } catch (error) {
        console.error('Error fetching faculty profile:', error);
      }
    };

    fetchFacultyProfile();
  }, [facultyId]);

  if (!faculty) {
    return <p>Loading...</p>;
  }

//   const formatDate = (dateString) => {
//     const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
//     return new Date(dateString).toLocaleDateString('en-US', options);
//   };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('faculty_id', facultyId);
      formData.append('profilePic', file);

      try {
        const response = await axios.post('http://127.0.0.1:5000/addfacultyprofile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        alert(response.data.message);
        const updatedProfile = await axios.get(`http://127.0.0.1:5000/faculty/${facultyId}`);
        setFaculty(updatedProfile.data);
      } catch (error) {
        alert('File upload failed');
      }
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleEmailEditClick = () => {
    setEmail(faculty.email);
    setIsEditingPassword(false);
    setIsEditingEmail(true);
  };

  const handleEmailCancel = () => {
    setOtp('')
    setIsEditingEmail(false);
    setshowEmailModal(false); // Close modal if open
  };

  const handleRequestOtp = async () => {
    if(email === faculty.email){
        setIsEditingEmail(false);
        setshowEmailModal(false);
        setOtp('')
        return null;
    }
    try {
      const response = await axios.post('http://localhost:5000/request-otp-faculty', {
        faculty_id: facultyId,
        new_email: email,
      });
      if (response.status === 200) {
        setshowEmailModal(true); // Show OTP input modal
      }
    } catch (error) {
      alert("Error sending OTP");
    }
  };

  const handleVerifyOtp = async () => {
    try {
      const response = await axios.post('http://localhost:5000/update-email-faculty', {
        faculty_id: facultyId,
        new_email: email,
        otp: otp,
      });
      if (response.status === 200) {
        alert('Email updated successfully');
        faculty.email = email; // Update local faculty email
        setIsEditingEmail(false);
        setshowEmailModal(false);
        setOtp('')
      }
    } catch (error) {
      alert('Error verifying OTP');
      setIsEditingEmail(false);
      setshowEmailModal(false);
      setOtp('')
    }
  };

  const handleOtpChange = (e) => {
    setOtp(e.target.value);
  };

  const handlePasswordEditClick = () => {
    setPassword('');
    setConfirmPassword('');
    setNewPassword('');
    setIsEditingEmail(false);
    setIsEditingPassword(true);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handlePasswordCancel = () => {
    setIsEditingPassword(false);
    setshowPasswordModal(false);
  };

  const handleNewPasswordChange = (e) => {
    setNewPassword(e.target.value);
  };

  const handleConfirmPasswordChange = (e) => {
    setConfirmPassword(e.target.value);
  };

  const handlePasswordSave = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/verify-password-faculty', {
        faculty_id: facultyId,
        current_password: password,
      });
      if (response.status === 200) {
        setshowPasswordModal(true);
        setIsEditingPassword(false);
      }
    } catch (error) {
      alert('Failed to verify current password');
      setIsEditingPassword(false);
    }
  };
  
  const handleNewPasswordSave = async (e) => {
    try {
      if (newPassword !== confirmPassword) {
        alert('Passwords do not match');
        return;
      }

      if (newPassword === confirmPassword === password) {
        alert('The new password is same as old password');
        return;
      }

      const response = await axios.post('http://127.0.0.1:5000/change-password-faculty', {
        faculty_id: facultyId,
        new_password: newPassword,
      });
      if (response.status === 200) {
        alert('Password changed successfully');
        setshowPasswordModal(false);
        handlePasswordCancel();
      }
    } catch (error) {
      alert('Failed to change password');
      setshowPasswordModal(false);
    }
  };

  return (
    <div className="container">
      <div className="profile-container">
        <div className="profile-pic-box">
          {faculty.profilePath ? (
            <img src={`http://127.0.0.1:5000/profile/${faculty.profilePath}`} alt="Profile" className="profile-pic" />
          ) : (
            <div className="upload-btn-box">
              <button className="upload-btn" onClick={handleUploadClick}>
                <i className="fas fa-upload"></i>
                <span>Upload</span>
              </button>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                ref={fileInputRef}
                style={{ display: 'none' }}
              />
            </div>
          )}
        </div>
        <div className="update-btn-box">
          {faculty.profilePath ? (
            <div>
              <button className="update-btn" onClick={handleUploadClick}>
                <i className="fas fa-sync-alt"></i> Update Profile
              </button>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                ref={fileInputRef}
                style={{ display: 'none' }}
              />
            </div>
          ):(
            <p>Please Upload Profile Picture</p>
          )}
        </div>
        <div className="field-name">
          <p><strong>Faculty Id</strong></p>
        </div>
        <div className="field-value">
          <p>{faculty.faculty_id}</p>
        </div>
        <div className="field-name">
          <p><strong>Name</strong></p>
        </div>
        <div className="field-value">
          <p>{faculty.name}</p>
        </div>
        <div className="field-name">
          <p><strong>Department</strong></p>
        </div>
        <div className="field-value">
          <p>{faculty.department}</p>
        </div>
        <div className="field-name">
          <p><strong>Email</strong></p>
        </div>
        <div className="field-value">
          <p>
            {!isEditingEmail && (
              faculty.email ? (
                <>
                  {faculty.email}
                  <button className="edit-btn" onClick={handleEmailEditClick}>
                    <i className="fas fa-edit"></i>
                  </button>
                </>
              ) : (
                <button className="edit-btn" onClick={handleEmailEditClick}>
                  <i className="fas fa-edit"></i> Add Email
                </button>
              )
            )}
            {isEditingEmail && (
              <>
                <input
                  type="email"
                  value={email}
                  placeholder='Email'
                  onChange={handleEmailChange}
                />
                <button className="action-btn cancel" onClick={handleEmailCancel}>
                  <i className="fas fa-times"></i>
                </button>
                <button className="action-btn confirm" onClick={handleRequestOtp}>
                  <i className="fas fa-check"></i>
                </button>
              </>
            )}
          </p>
        </div>
        <div className="field-name">
          <p><strong>Password</strong></p>
        </div>
        <div className="field-value">
          <p>
              {!isEditingPassword && (
                <button className="edit-btn" onClick={handlePasswordEditClick}>
                    <i className="fas fa-edit"></i> Change Password
                </button>
              )}
              {isEditingPassword && (
                <>
                  <input
                      className='change'
                      type="password"
                      value={password}
                      placeholder='Current Password'
                      onChange={handlePasswordChange}
                  />
                  <button className="action-btn cancel" onClick={handlePasswordCancel}>
                    <i className="fas fa-times"></i>
                  </button>
                  <button className="action-btn confirm" onClick={handlePasswordSave}>
                    <i className="fas fa-check"></i>
                  </button>
                </>
              )}
          </p>
        </div>
      </div>

      <VerifyEmail 
        show={showEmailModal} 
        otp={otp} 
        onClose={handleEmailCancel} 
        onConfirm={handleVerifyOtp} 
        otpchange={handleOtpChange}
      />

      <ChangePassword 
        show={showPasswordModal} 
        new_password={newPassword}
        confirm_password={confirmPassword}
        onClose={handlePasswordCancel} 
        onConfirm={handleNewPasswordSave} 
        newPasswordchange={handleNewPasswordChange}
        confirmPasswordchange={handleConfirmPasswordChange}
      />
    </div>
  );
};

export default FacultyProfile;
