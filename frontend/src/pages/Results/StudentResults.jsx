import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faTimes } from '@fortawesome/free-solid-svg-icons';
import CloseIcon from '@material-ui/icons/Close';
import '../../styles/StudentResult.css';

const StudentResults = () => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const regNo = sessionStorage.getItem('regno');
    const [viewResult, setViewResult] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:5000/published-results-student', {
                    reg_no: regNo
                });
                const sortedResults = response.data.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate));
                setResults(sortedResults);
                setLoading(false);
            } catch (err) {
                setError(err);
                setLoading(false);
            }
        };

        fetchResults();
    }, [regNo]);

    const viewresult = (name) => {
        setViewResult(viewResult === name ? '' : name);
    };

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const filteredResults = results.filter(result => {
        const words = searchTerm.toLowerCase().split(' ');
        return words.every(word => result.result_name.toLowerCase().includes(word));
    });

    return (
        <div className="container">
            {loading && (
                <div>
                    <p>Loading...</p>
                </div>
            )}
            {error && (
                <div>
                    <p>Error loading results: {error.message}</p>
                </div>
            )}
            {!loading && !error && (
                <div>
                    <div className="search-container">
                        <input
                            type="text"
                            placeholder="Search Result"
                            value={searchTerm}
                            onChange={handleSearch}
                            className="search-bar"
                        />
                        {searchTerm && (
                            <div className="close-icon" onClick={() => setSearchTerm('')}>
                                <CloseIcon />
                            </div>
                        )}
                    </div>
                    {filteredResults.map((result, index) => (
                        <div className="result-card" key={index}>
                            <div className="result-header">
                                <div>
                                    <p className="result-name">{result.result_name}</p>
                                    <p className="publish-date">Published On: {result.publishDate}</p>
                                </div>
                                <div>
                                    <button
                                        className={`view-button ${viewResult === result.result_name ? 'close-button' : ''}`}
                                        onClick={() => viewresult(result.result_name)}
                                    >
                                        <FontAwesomeIcon icon={viewResult === result.result_name ? faTimes : faEye} /> {viewResult === result.result_name ? 'Hide' : 'View'}
                                    </button>
                                </div>
                            </div>
                            {viewResult === result.result_name && (
                                <div className="table-container">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th className="center-text">SL</th>
                                                <th>Course</th>
                                                <th className="center-text">Grade</th>
                                                <th className="center-text">Credits</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {result.result.map((course, courseIndex) => (
                                                <tr key={courseIndex}>
                                                    <td className="center-text">{courseIndex + 1}</td>
                                                    <td>{course.courseName}</td>
                                                    <td className="center-text">{course.grade}</td>
                                                    <td className="center-text">{course.credits}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default StudentResults;
