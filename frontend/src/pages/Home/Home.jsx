import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../../styles/Home.css';
import CloseIcon from '@material-ui/icons/Close';

function HomeStudent() {
  const [notifications, setNotifications] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [pageNumber, setPageNumber] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.post('http://localhost:5000/announcements', {
          pageNumber: pageNumber,
          searchText: searchTerm,
          dataSize: 20
        }, {
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (response.status === 200) {
          setNotifications(response.data.notifications);
        } else {
          console.error('No content found in JSON data.');
        }
      } catch (error) {
        console.error('Error:', error);
      }finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [searchTerm, pageNumber]); // Add searchTerm to the dependency array

  const handleSearch = (event) => {
    setPageNumber(0);
    setSearchTerm(event.target.value);
  };

  const handleNextPage = () => {
    setPageNumber(pageNumber + 1); // Increment page number
  };

  const handlePreviousPage = () => {
    if (pageNumber > 0) {
      setPageNumber(pageNumber - 1);
    }
  };

  const formatDate = (dateString) => {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  return (
    <div className="container">
      <h2 className='heading'>Announcements</h2>
      <div className="search-container"> {/* Added container for search bar */}
        <input
          type="text"
          placeholder="Search notifications"
          value={searchTerm}
          onChange={handleSearch}
          className="search-bar"
        />
        {searchTerm && ( // Render the close icon only if searchTerm is not empty
          <div className="close-icon" onClick={() => [setSearchTerm(''),setPageNumber(0)]}>
            <CloseIcon />
          </div>
        )}
      </div>
      <div className="notifications">
      {loading && <p className="loading-text">Loading...</p>}
        {!loading && notifications.length === 0 ? (
          <p className="no-notifications-message">No Notifications found</p>
        ) : (
        notifications.map((notification, index) => (
          <div className="notification-card" key={index}>
            <h2>{notification.title}</h2>
            <p className="date">{formatDate(notification.date)}</p>
            <div
            className="description"
            dangerouslySetInnerHTML={{ __html: notification.description }}
          />
          </div>
        )))}
      </div>
      <div className="page-buttons">
      <button className="prev-button" onClick={handlePreviousPage} disabled={pageNumber === 0}>Prev</button>
      {/* <button className="next-button" onClick={handleNextPage}>Next</button> */}
      <button className="next-button" onClick={handleNextPage} disabled={notifications.length < 20}>Next</button>
      </div>
    </div>
  );
}


export default HomeStudent;
