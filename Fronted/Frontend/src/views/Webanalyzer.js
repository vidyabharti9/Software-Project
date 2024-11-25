import React, { useState, useEffect, useContext } from 'react';
import './Webanalyzer.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../components/authContext'; // Import AuthContext

const DynamicForm = () => {
  const [url, setUrl] = useState('');
  const [firstOption, setFirstOption] = useState('');
  const [secondOptions, setSecondOptions] = useState([]);
  const [secondOption, setSecondOption] = useState('');
  const { isLoggedIn } = useContext(AuthContext); // Use context for authentication
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      navigate('/login');
    }
  }, [isLoggedIn, navigate]);

  const handleFirstOptionChange = (e) => {
    const selectedOption = e.target.value;
    setFirstOption(selectedOption);
    switch (selectedOption) {
      case 'User Interface':
        setSecondOptions(['Color Grading', 'Content Style', 'Element Layout']);
        break;
      case 'User Experience':
        setSecondOptions(['WebPage Performance', 'WebPage Quality']);
        break;
      case 'Website Security':
        setSecondOptions(['Security and Policy', 'Threats Mitigation']);
        break;
      case 'SEO':
        setSecondOptions(['Website Ranking', 'SEO Grading', 'Competitor Analysis', 'Keyword Tracking', 'Trend Analysis']);
        break;
      case 'Website Advertisement':
        setSecondOptions(['Ads Recommendation', 'Ads Positioning']);
        break;
      default:
        setSecondOptions([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // First, send scrape request
      const scrapeResponse = await axios.post('http://localhost:8000/scrape', {
        url,
        feature: firstOption,
        sub_feature: secondOption
      });
      console.log('Scrape Response:', scrapeResponse.data);
      // Initialize an array to hold multiple post requests
      let postRequests = [];
      // Define post requests based on sub_feature
      switch (secondOption) {
        case 'Color Grading':
          postRequests.push(axios.post('http://localhost:8000/color_grading', { url }));
          break;
        case 'Content Style':
          postRequests.push(axios.post('http://localhost:8000/content_style', { url }));
          break;
        case 'Element Layout':
          postRequests.push(axios.post('http://localhost:8000/responsive', { url }));
          break;
        case 'WebPage Performance':
          postRequests.push(axios.post('http://localhost:8000/webpage_performance', { url }));
          break;
        case 'WebPage Quality':
          postRequests.push(axios.post('http://localhost:8000/webpage_quality', { url }));
          break;
        case 'Security and Policy':
          postRequests.push(axios.post('http://localhost:8000/security_policy', { url }));
          break;
        case 'Threats Mitigation':
          postRequests.push(axios.post('http://localhost:8000/threats_mitigation', { url }));
          break;
        case 'Website Ranking':
          postRequests.push(axios.post('http://localhost:8000/website_ranking', { url }));
          break;
        case 'SEO Grading':
          postRequests.push(axios.post('http://localhost:8000/seo_grading', { url }));
          break;
        case 'Competitor Analysis':
          postRequests.push(axios.post('http://localhost:8000/competitor_analysis', { url }));
          break;
        case 'Keyword Tracking':
          postRequests.push(axios.post('http://localhost:8000/keyword_tracking', { url }));
          break;
        case 'Trend Analysis':
          postRequests.push(axios.post('http://localhost:8000/trend_analysis', { url }));
          break;
        case 'Ads Recommendation':
          postRequests.push(axios.post('http://localhost:8000/ads_recommendation', { url }));
          break;
        case 'Ads Positioning':
          postRequests.push(axios.post('http://localhost:8000/ads_positioning', { url }));
          break;
        default:
          postRequests.push(scrapeResponse);
      }
      // Execute all post requests
      const responses = await Promise.all(postRequests);
      console.log('Feature Responses:', responses);
      // Collect data from all responses
      const combinedData = responses.reduce((acc, response) => {
        return { ...acc, ...response.data };
      }, {});

      // Save report data
    const user = JSON.parse(localStorage.getItem("user"));
    const reportData = {
      user_id: user.user_id,
      feature: firstOption,
      sub_feature: secondOption,
      data: combinedData,
      url: url
    };
    await axios.post('http://localhost:8000/save_report', reportData);
      // Pass the combined data to the report page
      navigate('/report', { state: { data: combinedData, feature: firstOption, sub_feature: secondOption, url } });
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <div className="container">
      <h3 className="head">WebAnalyzer</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <p className="url-heading">Start analyzing your website</p>
        </div>
        <div>
          <label>URL:</label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
        </div>
        <div>
          <label>First Option:</label>
          <select
            value={firstOption}
            onChange={handleFirstOptionChange}
            required
          >
            <option value="">Select an option</option>
            <option value="User Interface">User Interface</option>
            <option value="User Experience">User Experience</option>
            <option value="Website Security">Website Security</option>
            <option value="SEO">SEO</option>
            <option value="Website Advertisement">Website Advertisement</option>
          </select>
        </div>
        {firstOption && (
          <div>
            <label>Second Option:</label>
            <select
              value={secondOption}
              onChange={(e) => setSecondOption(e.target.value)}
              required
            >
              <option value="">Select an option</option>
              {secondOptions.map((option, index) => (
                <option key={index} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        )}
        <button type="submit">Generate Report</button>
      </form>
    </div>
  );
};

export default DynamicForm;
