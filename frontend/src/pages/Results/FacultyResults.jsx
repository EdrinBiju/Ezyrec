import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import CloseIcon from '@material-ui/icons/Close';
import '../../styles/FacultyResult.css';
import Loading from '../../Components/Loading';

const FacultyResults = () => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadingModal, setLoadingModal] = useState(false);
    const [error, setError] = useState(null);
    const [viewResult, setViewResult] = useState('');
    const [viewStudent, setViewStudent] = useState('');
    const [viewedData, setViewedData] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/fetch-published-results');
                const sortedResults = response.data.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate));
                setResults(sortedResults);
                setLoading(false);
            } catch (err) {
                setError(err);
                setLoading(false);
            }
        };

        fetchResults();
    }, []);

    const viewResultDetails = async (result) => {
        if (viewResult === result.resultName) {
            setViewResult('');
            setViewedData([]);
        } else {
            setLoadingModal(true);
            try {
                const response = await axios.post('http://127.0.0.1:5000/published-results-allstudents', {
                    token: result.token,
                    date: result.publishDate,
                    resultName: result.resultName
                });
                setViewedData(response.data.map(student => ({ ...student, visible: false })));
                setViewResult(result.resultName);
                setLoadingModal(false);
            } catch (err) {
                setError(err);
                setLoadingModal(false);
            }
        }
    };

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const toggleVisibility = (reg_no) => {
        if (viewStudent === reg_no) {
            setViewStudent('');
        }
        else{
            setViewStudent(reg_no)
        }
        setViewedData(prevState => 
            prevState.map(student => 
                student.reg_no === reg_no ? { ...student, visible: !student.visible } : student
            )
        );
    };

    const filteredResults = results.filter(result => {
        const words = searchTerm.toLowerCase().split(' ');
        return words.every(word => result.resultName.toLowerCase().includes(word));
    });

    return (
        <div className="container">
            {loading && (
                <div className=''>
                    <p>Loading...</p>
                </div>
            )}
            {error && (
                <div className=''>
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
                                    <p className="result-name">{result.resultName}</p>
                                    <p className="publish-date">Published On: {result.publishDate}</p>
                                </div>
                                <div>
                                    <button
                                        className={`view-button ${viewResult === result.resultName ? 'close-button' : ''}`}
                                        onClick={() => viewResultDetails(result)}
                                    >
                                        <FontAwesomeIcon icon={viewResult === result.resultName ? faEyeSlash : faEye} /> {viewResult === result.resultName ? 'Hide' : 'View'}
                                    </button>
                                </div>
                            </div>
                            {viewResult === result.resultName && viewedData.length > 0 && (
                                <div className="student-cards-container">
                                    {viewedData.map((student, studentIndex) => (
                                        <div className="student-card" key={studentIndex}>
                                            <div className="student-card-header">
                                                <div className="student-name">
                                                    <p >Name : {student.name}</p>
                                                </div>
                                                <div className="student-regno">
                                                    <p >Register Number : {student.reg_no}</p>
                                                </div>
                                                <div>
                                                <button
                                                    className={`view-button ${viewStudent === student.reg_no ? 'close-button' : ''}`}
                                                    onClick={() => toggleVisibility(student.reg_no)}
                                                >
                                                    {student.visible ? 'Hide Results' : 'View Results'}
                                                </button>
                                                </div>
                                            </div>
                                            {viewStudent === student.reg_no && student.visible && (
                                                <div className="result-table">
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
                                                            {student.result.map((subject, subIndex) => (
                                                                <tr key={subIndex}>
                                                                    <td className="center-text">{subIndex+1}</td>
                                                                    <td>{subject.courseName}</td>
                                                                    <td className="center-text">{subject.grade}</td>
                                                                    <td className="center-text">{subject.credits}</td>
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
                            {viewResult === result.resultName && viewedData.length === 0 && (
                                <div>
                                    <p className='noresult'>No Student Result Found.</p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
            <Loading show={loadingModal} />
        </div>
    );
};

export default FacultyResults;
