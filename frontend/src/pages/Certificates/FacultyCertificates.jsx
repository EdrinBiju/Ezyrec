import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "../../styles/Certificates.css";
import { generateThumbnail } from '../../Utils/thumbnailGenerator';
import loadingIcon from '../../assets/loading.gif';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faCheck, faEye } from '@fortawesome/free-solid-svg-icons';
import CloseIcon from '@material-ui/icons/Close';

const FacultyCertificates = () => {
  const [certificates, setCertificates] = useState([]);
  const regNo = sessionStorage.getItem('regno');
  const [loading, setLoading] = useState(true);
  const [thumbnailfetching, setFetching] = useState(false);
  const [status, setStatus] = useState('Pending');
  const [category, setCategory] = useState('All Students');
  const [searchText, setSearchText] = useState('');
  const [change, setChange] = useState(false);


  useEffect(() => {
    const fetchCertificates = async () => {
      const formData = new FormData();
      formData.append('status', status);
      formData.append('category', category);
      formData.append('searchText', searchText);
      try {
        const response = await fetch('http://127.0.0.1:5000/certificates', {
          method: 'POST',
          body: formData,
        });
        if (!response.ok) {
          throw new Error('Failed to fetch certificates');
        }
        const data = await response.json();

        setCertificates(data.certificates);
        setFetching(true)

      } catch (error) {
        console.error('Error:', error);
      }finally {
        setLoading(false);
      }

    };
    
    fetchCertificates();
  }, [regNo, change, status, category, searchText]);

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

  const allStatus = ["Pending","Accepted","Rejected","All"]

  const allCategories = ["All Students","Search By Name","Search By Register Number"]

  const formatDate = (dateString) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const rejectCertificate = async (id) => {
    if (window.confirm('Are you sure you want to reject this certificate?')) {
      try {
        await axios.post(`http://127.0.0.1:5000/reject/${id}`);
        setChange(!change)
      } catch (error) {
        alert('Error rejecting certificate');
      }
    }
  };

  const acceptCertificate = async (id) => {
    if (window.confirm('Are you sure you want to accept this certificate?')) {
      try {
        await axios.post(`http://127.0.0.1:5000/accept/${id}`);
        setChange(!change)
      } catch (error) {
        alert('Error accepting certificate');
      }
    }
  };

  const handleStatusChange = (event) => {
    setStatus(event.target.value);
  };

  const handleCategoryChange = (event) => {
    setCategory(event.target.value);
  };

  const handleSearchTextChange = (event) => {
    setSearchText(event.target.value);
  };

  const updateStatus = async (id,status) => {
    if (window.confirm('Are you sure you want to change the certificate status?')) {
      try {
        if(status === 'Rejected')
          {await axios.post(`http://127.0.0.1:5000/accept/${id}`);}
        else if(status === 'Accepted')
          {await axios.post(`http://127.0.0.1:5000/reject/${id}`);}
        setChange(!change)
      } catch (error) {
        alert('Error changing certificate status');
      }
    }
  };

  return (
    <div className="container">
      <div className='filters'>
        <h1 className='header'>Filters</h1>
        <div className='filter-menus'>
          <select className='menu-item'
            value={status}
            onChange={handleStatusChange}
            required
          >
            {allStatus.map((statusOption) => (
              <option key={statusOption} value={statusOption}>{statusOption}</option>
            ))}
          </select>

          <select className='menu-item'
            value={category}
            onChange={handleCategoryChange}
            required
          >
            {allCategories.map((categoryOption) => (
              <option key={categoryOption} value={categoryOption}>{categoryOption}</option>
            ))}
          </select>
        </div>
      </div>
      {category !== 'All Students' && (
        <div className="search-container"> {/* Added container for search bar */}
          <input
            type="text"
            placeholder={category}
            value={searchText}
            onChange={handleSearchTextChange}
            className="search-bar"
          />
          {searchText && ( // Render the close icon only if searchTerm is not empty
            <div className="close-icon" onClick={() => [setSearchText('')]}>
              <CloseIcon />
            </div>
          )}
        </div>
      )}
      {category === 'All Students' && (<hr/>)}
      {certificates && (
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
                    <p><span className='certificate-text'>Student : </span>{certificate.student}</p>
                    <p><span className='certificate-text'>Register No : </span>{certificate.reg_no}</p>
                    <p><span className='certificate-text'>Certificate Name : </span>{certificate.certificate_name}</p>
                    <p><span className='certificate-text'>Issued By : </span>{certificate.organization}</p>
                    <p><span className='certificate-text'>Issued On : </span>{formatDate(certificate.issue_date)}</p>
                    <p><span className='certificate-text'>Criteria : </span>{certificate.criteria}</p>
                    <p><span className='certificate-text'>Sub Criteria : </span>{certificate.sub_criteria}</p>
                    {certificate.level && <p><span className='certificate-text'>Level : </span>{certificate.level}</p>}
                    {certificate.achievement && <p><span className='certificate-text'>Achievement : </span>{certificate.achievement}</p>}
                    {certificate.achievement && <p><span className='certificate-text'>Achievement Proof : &ensp;</span>
                      <div className="view-div">
                        <a href={`http://127.0.0.1:5000/viewAchievement/${certificate.achievement_file_path}`} target="_blank" rel="noopener noreferrer">
                          <button className="action-button"><FontAwesomeIcon icon={faEye}/> View</button>
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
                  {certificate.status === 'Pending' ? (
                    <div className="certificate-actions">
                      <a href={`http://127.0.0.1:5000/view/${certificate.file_path}`} target="_blank" rel="noopener noreferrer">
                        <button className="action-button"><FontAwesomeIcon icon={faEye} /> View</button>
                      </a>
                      <a href="#foo" onClick={() => rejectCertificate(certificate.id)}>
                        <button type='reject' className="action-button"><FontAwesomeIcon icon={faTimes} /> Reject</button>
                      </a>
                      <a href="#foo" onClick={() => acceptCertificate(certificate.id)}>
                        <button type='accept' className="action-button"><FontAwesomeIcon icon={faCheck} /> Accept</button>
                      </a>
                    </div>
                  ) : (
                    <div className="certificate-actions">
                      <a href={`http://127.0.0.1:5000/view/${certificate.file_path}`} target="_blank" rel="noopener noreferrer">
                        <button className="action-button"><FontAwesomeIcon icon={faEye} /> View</button>
                      </a>
                      <a href="#foo" onClick={() => updateStatus(certificate.id,certificate.status)}>
                        <button className="action-button"><i className="fas fa-sync-alt"></i> Status</button>
                      </a>
                    </div>
                  )}
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

export default FacultyCertificates;
