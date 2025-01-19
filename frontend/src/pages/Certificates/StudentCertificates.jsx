import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "../../styles/Certificates.css";
import { IoAdd } from "react-icons/io5";
import { generateThumbnail } from '../../Utils/thumbnailGenerator';
import { criteriaOptions, activityLevels, approvalDocuments, additionalCriteria } from '../../Constants/FormConstants';
import loadingIcon from '../../assets/loading.gif';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faDownload, faTrash } from '@fortawesome/free-solid-svg-icons';

const StudentCertificates = () => {
  const [showForm, setShowForm] = useState(false);
  const [certificateName, setCertificateName] = useState('');
  const [organization, setOrganization] = useState('');
  const [issueDate, setIssueDate] = useState('');
  const [certificateFile, setCertificateFile] = useState(null);
  const [achievementFile, setAchievementFile] = useState(null);
  const [criteria, setCriteria] = useState('');
  const [subCriteria, setSubCriteria] = useState('');
  const [level, setLevel] = useState('');
  const [approvalDocument, setApprovalDocument] = useState('');
  const [achievement, setAchievement] = useState('');
  const [certificates, setCertificates] = useState([]);
  const regNo = sessionStorage.getItem('regno');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [thumbnailfetching, setFetching] = useState(false);

  useEffect(() => {
    const fetchCertificates = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/studentcertificates', {
          method: 'POST',
          headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ reg_no: regNo }),
        });
        if (!response.ok) {
          throw new Error('Failed to fetch certificates');
        }
        const data = await response.json();
        
        // for (const certificate of data.certificates) {
        //   const pdfUrl = `http://127.0.0.1:5000/view/${certificate.file_path}`;
        //   certificate.thumbnail = await generateThumbnail(pdfUrl);
        // }

        setCertificates(data.certificates);
        setFetching(true)
      } catch (error) {
        console.error('Error:', error);
      }finally {
        setLoading(false);
      }

    };
    if(showForm === false){
      fetchCertificates();
    }
  }, [regNo, showForm]);

  // useEffect(() => {
  //   const fetchThumbnails = async () => {
  //     const updatedCertificates = await Promise.all(certificates.map(async (certificate) => {
  //       const pdfUrl = `http://127.0.0.1:5000/view/${certificate.file_path}`;
  //       const thumbnail = await generateThumbnail(pdfUrl);
  //       return { ...certificate, thumbnail };
  //     }));
  //     setCertificates(updatedCertificates);
  //   };

  //   if (certificates.length > 0 && thumbnailfetching === true) {
  //     fetchThumbnails();
  //     setFetching(false)
  //   }
  // }, [certificates]);

  useEffect(() => {
    const fetchThumbnails = async () => {
      for (const certificate of certificates) {
        const pdfUrl = `http://127.0.0.1:5000/view/${certificate.file_path}`;
        const thumbnail = await generateThumbnail(pdfUrl);

        setCertificates(prevCertificates =>
          prevCertificates.map(cert =>
            cert.file_path === certificate.file_path
              ? { ...cert, thumbnail }
              : cert
          )
        );
      }
    };

    if (certificates.length > 0 && thumbnailfetching === true) {
      fetchThumbnails();
      setFetching(false)
    }
  }, [certificates, thumbnailfetching]);

  useEffect(() => {
    setShowForm(false); // Reset showForm to false when the component mounts
  }, []);

  const handleAddCertificateClick = () => {
    setShowForm(true);
    setCertificateName('');
    setOrganization('');
    setIssueDate('');
    setCertificateFile(null);
    setAchievementFile(null);
    setCriteria('');
    setSubCriteria('');
    setLevel('');
    setApprovalDocument('');
    setAchievement('')
  };

  const handleBackButtonClick = () => {
    setShowForm(false);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('reg_no', regNo);
    formData.append('certificateName', certificateName);
    formData.append('organization', organization);
    formData.append('issueDate', issueDate);
    formData.append('criteria', criteria);
    formData.append('subCriteria', subCriteria);
    formData.append('level', level);
    formData.append('achievement', achievement)
    formData.append('approvalDocument', approvalDocument);
    formData.append('certificateFile', certificateFile);
    formData.append('achievementFile', achievementFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/addcertificates', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      setShowForm(false);
      
    } catch (error) {
      setError('An unexpected error occurred. Please try again later.');
      // Handle error response
    }
  };

  const formatDate = (dateString) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const handleCriteriaChange = (event) => {
    setCriteria(event.target.value);
    setSubCriteria('');
    setLevel('');
    setApprovalDocument('');
    setAchievement('')
  };

  const handleSubCriteriaChange = (event) => {
    setSubCriteria(event.target.value);
    setLevel('');
    setApprovalDocument('');
    setAchievement('')
  };

  const shouldShowLevelField = (criteria, subCriteria) => {
    const levelRequiredCriteria = [
      { criteria: "Sports & Games", subCriteria: ["Sports", "Games"] },
      { criteria: "Cultural Activities", subCriteria: ["Music", "Performing arts", "Literary arts"] },
      { criteria: "Professional Self Initiatives", subCriteria: [
        "Tech Fest, Tech Quiz",
        "Competitions conducted by Professional Societies"
      ] },
      { criteria: "Leadership & Management", subCriteria: [
        "Student Professional Societies (IEEE, IET, ASME, SAE, NASA etc.)",
        "College Association Chapters (Mechanical, Civil, Electrical etc.)",
        "Festival & Technical Events (College approved)",
        "Hobby Clubs",
        "Special Initiatives (Approval from College and University is mandatory)",
        "Elected student representatives"
      ] }
    ];


    return levelRequiredCriteria.some(
      (combination) =>
        combination.criteria === criteria &&
        combination.subCriteria.includes(subCriteria)
    );
  };

  const handleAchievementChange = (event) => {
    setAchievement(event.target.value);
  };

  const shouldShowadditionalField = (criteria, subCriteria) => {
    const additionalRequiredCriteria = [
      { criteria: "National Initiatives", subCriteria: ["NCC", "NSS"] },
      { criteria: "Sports & Games", subCriteria: ["Sports", "Games"] },
      { criteria: "Cultural Activities", subCriteria: ["Music", "Performing arts", "Literary arts"] },
      { criteria: "Professional Self Initiatives", subCriteria: [
        "Paper presentation/publication at IITs/NITs",
        "Paper presentation/publication at KTU or its affiliated institutes",
        "Poster Presentation at IITs/NITs",
        "Poster Presentation at KTU or its affiliated institutes"
      ] }
    ]
    return additionalRequiredCriteria.some(
      (combination) =>
        combination.criteria === criteria &&
        combination.subCriteria.includes(subCriteria)
    );
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setCertificateFile(selectedFile);
    } else {
      alert('Please select a PDF file.');
      // Reset the file input to clear the selection
      e.target.value = null;
    }
  };

  const handleAchievementFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setAchievementFile(selectedFile);
    } else {
      alert('Please select a PDF file.');
      // Reset the file input to clear the selection
      e.target.value = null;
    }
  };

  const deleteCertificate = async (id) => {
    if (window.confirm('Are you sure you want to delete this certificate?')) {
      try {
        await axios.delete(`http://127.0.0.1:5000/certificates/${id}`);
        setCertificates(certificates.filter(certificate => certificate.id !== id));
      } catch (error) {
        console.error('Error deleting certificate:', error);
      }
    }
  };

  return (
    <div className="container">
      <div className="user-content-heading">
        <div className="heading certificate-heading">
          <h2>All Certificates</h2>
        </div>
        <div className="btn">
          <button className="add-new-certificate" onClick={handleAddCertificateClick} disabled={showForm === true}>
            <IoAdd
              style={{
                fontSize: 25,
                paddingRight: 5,
              }}
            />
            Add Certificate
          </button>
        </div>
      </div>
      <hr />
      {showForm ? (
        <div className="user-content-item">
          <div className="formcontainer">
            <form onSubmit={handleFormSubmit} className="certificate-form">
              <div className="form-group">
                <label>Certificate Name:</label>
                <input
                  type="text"
                  value={certificateName}
                  onChange={(e) => setCertificateName(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Issuing Organization:</label>
                <input
                  type="text"
                  value={organization}
                  onChange={(e) => setOrganization(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Date of Issue:</label>
                <input
                  type="date"
                  value={issueDate}
                  onChange={(e) => setIssueDate(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Select Certificate Criteria:</label>
                <select
                  value={criteria}
                  onChange={handleCriteriaChange}
                  required
                >
                  <option value="" disabled>Select Criteria</option>
                  {Object.keys(criteriaOptions).map((key) => (
                    <option key={key} value={key}>{key}</option>
                  ))}
                </select>
              </div>
              {criteria && (
                <div className="form-group">
                  <label>Select Sub-Criteria:</label>
                  <select
                    value={subCriteria}
                    onChange={handleSubCriteriaChange}
                    required
                  >
                    <option value="" disabled>Select Sub-Criteria</option>
                    {criteriaOptions[criteria].map((sub) => (
                      <option key={sub} value={sub}>{sub}</option>
                    ))}
                  </select>
                </div>
              )}
              {criteria && subCriteria && shouldShowLevelField(criteria, subCriteria) && (
                <div className="form-group">
                  <label>Select Level:</label>
                  <select
                    value={level}
                    onChange={(e) => setLevel(e.target.value)}
                    required
                  >
                    <option value="" disabled>Select Level</option>
                    {criteria === "Leadership & Management" ? (
                      subCriteria === "Elected student representatives" ? (
                        <>
                          <option key="Level I" value="Chairman">Chairman</option>
                          <option key="Level II" value="Secretary">Secretary</option>
                          <option key="Level III" value="Other Council Members">Other Council Members</option>
                        </>
                      ) : (
                        <>
                          <option key="Level I" value="Core coordinator">Core coordinator</option>
                          <option key="Level II" value="Sub coordinator">Sub coordinator</option>
                          <option key="Level III" value="Volunteer">Volunteer</option>
                        </>
                      )
                    ) : (
                      Object.entries(activityLevels).map(([key, value]) => (
                        <option key={key} value={value}>{value}</option>
                      ))
                    )}
                  </select>
                </div>
              )}
              {criteria && shouldShowadditionalField(criteria, subCriteria) && (
                <div className="form-group">
                  <label>Achievement:</label>
                  <select
                    value={achievement}
                    onChange={handleAchievementChange}
                  >
                    <option value="" disabled>Select Additional Achievement</option>
                    {additionalCriteria[criteria].map((point, index) => (
                      <option key={index} value={point}>{point}</option>
                    ))}
                  </select>
                </div>
              )}

              {achievement && achievement !=="None Of The Above" && criteria === "National Initiatives" && (
                <div className="form-group">
                <label>Upload Achievement Proof (PDF):</label>
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleAchievementFileChange}
                  required
                />
              </div>
              )}

              <div className="form-group">
                <label>Select Approval Document Type:</label>
                <select
                  value={approvalDocument}
                  onChange={(e) => setApprovalDocument(e.target.value)}
                  required
                >
                  <option value="" disabled>Select Document Type</option>
                  {approvalDocuments
                    .filter((criteriaItem) => criteriaItem.criteria === criteria)
                    .flatMap((criteriaItem) =>
                      criteriaItem.subCriteria
                        .filter((subCriteriaItem) => subCriteriaItem.name.includes(subCriteria))
                        .flatMap((subCriteriaItem) =>
                          Object.entries(subCriteriaItem.approvalDocuments).map(([key, value]) => (
                            <option key={key} value={value}>{value}</option>
                          ))
                        )
                    )}
                </select>
              </div>
              <div className="form-group">
                <label>Upload Document PDF:</label>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  required
                />
              </div>
              {error && <p className="error">{error}</p>}
              <div className="form-buttons">
                <button type="button" className="back-button" onClick={handleBackButtonClick}>Back</button>
                <button type="submit">Submit</button>
              </div>
            </form>
          </div>
        </div>
      ) : (
        <div className="user-content">
          {loading && <p className="loading-text">Loading...</p>}
          {!loading && certificates.length > 0 && (
            <div className="certificates-grid">
              {certificates.map((certificate, index) => (
                <div key={index} className="certificate-item">
                  <a href={`http://127.0.0.1:5000/view/${certificate.file_path}`} target="_blank" rel="noopener noreferrer">
                    <img src={certificate.thumbnail || loadingIcon} alt={certificate.certificate_name} className="certificate-thumbnail" />
                  </a>
                  <div className="certificate-info">
                    <p><span className='certificate-text'>Name : </span>{certificate.certificate_name}</p>
                    <p><span className='certificate-text'>Issued By : </span>{certificate.organization}</p>
                    <p><span className='certificate-text'>Issued On : </span>{formatDate(certificate.issue_date)}</p>
                    <p><span className='certificate-text'>Criteria : </span>{certificate.criteria}</p>
                    <p><span className='certificate-text'>Sub Criteria : </span>{certificate.sub_criteria}</p>
                    {certificate.level && <p><span className='certificate-text'>Level : </span>{certificate.level}</p>}
                    {certificate.achievement && <p><span className='certificate-text'>Achievement : </span>{certificate.achievement}</p>}
                    {certificate.achievement && <p><span className='certificate-text'>Achievement Proof : &ensp;</span>
                      <div className="achievementcertificate-actions">
                        <a href={`http://127.0.0.1:5000/viewAchievement/${certificate.achievement_file_path}`} target="_blank" rel="noopener noreferrer">
                          <button className="action-button"><FontAwesomeIcon icon={faEye}/> View</button>
                        </a>
                        <a href={`http://127.0.0.1:5000/downloadAchievement/${certificate.achievement_file_path}`}>
                          <button className="action-button"><FontAwesomeIcon icon={faDownload} /> Download</button>
                        </a>
                      </div>
                    </p>}
                    {certificate.approval_document && <p>
                      <span className='certificate-text'>Approval Document : </span>{certificate.approval_document}
                    </p>}
                    <p><span className='certificate-text'>Activity Point : </span><strong>{certificate.activity_point}</strong></p>
                    <p>
                      <span className='certificate-text'>Status : </span>
                      <span className={`status ${certificate.status.toLowerCase()}`}>{certificate.status}</span>
                    </p>
                  </div>
                  <div className="certificate-actions">
                    <a href='#foo' onClick={() => deleteCertificate(certificate.id)}>
                      <button type='delete' className="action-button"><FontAwesomeIcon icon={faTrash}/>  Delete</button>
                    </a>
                    <a href={`http://127.0.0.1:5000/view/${certificate.file_path}`} target="_blank" rel="noopener noreferrer">
                      <button className="action-button"><FontAwesomeIcon icon={faEye} /> View</button>
                    </a>
                    <a href={`http://127.0.0.1:5000/download/${certificate.file_path}`}>
                      <button className="action-button"><FontAwesomeIcon icon={faDownload} /> Download</button>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
          {!loading && certificates.length === 0 && (
            <div className='no-found'>
              <p type='no-found'>No certificates found.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default StudentCertificates;
