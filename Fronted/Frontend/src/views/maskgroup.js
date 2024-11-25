import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import axios from 'axios';
import DashboardCard from './DashboardCard';
import './newMaskgroup.css';  // Updated CSS file
import PieChart from './PieChart';

const Maskgroup = () => {
  const location = useLocation();
  const { data, feature, sub_feature, url } = location.state || {};
  const [reportsData, setReportsData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReports = async () => {
      const user = JSON.parse(localStorage.getItem("user"));
      if (user) {
        try {
          const response = await axios.get(`http://localhost:8000/reports/${user.user_id}`);
          setReportsData(response.data);
        } catch (error) {
          console.error('Error fetching reports:', error);
        }
      }
    };
    fetchReports();
  }, []);

  const handleReportClick = async (reportId) => {
    try {
      const response = await axios.get(`http://localhost:8000/report/${reportId}`);
      navigate('/report', { state: { data: response.data, feature: response.data.feature, sub_feature: response.data.sub_feature, url: response.data.url } });
    } catch (error) {
      console.error('Error fetching report:', error);
    }
  };

  const pieChartData = data && data.results && data.results.total_score ? [data.results.total_score, 70 - data.results.total_score] : [0, 70];
  const numericalData = data && data.results && data.results.numerical_data ? data.results.numerical_data : {};
  const cardsData = Object.keys(numericalData).map((key, index) => {
    const card = numericalData[key];
    return {
      title: card.title,
      value: card.value || 0,
      percentage: '',
      className: `maskgroup-dashboardcard${index + 4}`
    };
  });

  const oneLinerData = data && data.results && data.results.one_liner_data ? data.results.one_liner_data : [];
  const [hoveredDetail, setHoveredDetail] = useState({ detail: '', position: { top: 0, left: 0 } });

  const handleMouseEnter = (event, detail) => {
    const rect = event.target.getBoundingClientRect();
    const newPosition = {
      top: rect.top + window.scrollY + 20,
      left: rect.left + window.scrollX + 20,
    };
    setHoveredDetail({
      detail,
      position: newPosition
    });
  };

  const handleMouseLeave = () => {
    setHoveredDetail({ detail: '', position: { top: 0, left: 0 } });
  };

  const recentReports = reportsData.sort((a, b) => b.report_id - a.report_id).slice(0, 5);

  return (
    <div className="container-group"> {/* Added container */}
      <Helmet>
        <title>Web Analyzer Report</title>
      </Helmet>
      <h1>{feature} - {sub_feature}</h1>
      <h2>Report for the {url}</h2>
      <div className="maskgroup-dashboard">
        {cardsData.slice(0, 4).map((card, index) => (
          <DashboardCard
            key={index}
            title={card.title}
            value={card.value}
            percentage={card.percentage}
            className={`maskgroup-card`}
          />
        ))}
        {cardsData.slice(4, 8).map((card, index) => (
          <DashboardCard
            key={index}
            title={card.title}
            value={card.value}
            percentage={card.percentage}
            className={`maskgroup-card`}
          />
        ))}
      </div>
      <div className="maskgroup-lower-section">
        <div className="maskgroup-chart-container">
          <PieChart data={pieChartData} />
        </div>
        <div className="maskgroup-one-liner">
          {oneLinerData.map((line, index) => (
            <span
              key={index}
              className="maskgroup-text"
              onMouseEnter={(e) => handleMouseEnter(e, line.details)}
              onMouseLeave={handleMouseLeave}
            >
              {line.title} <i className="info-icon">(i)</i>
              {hoveredDetail.detail === line.details && (
                <div className="hover-details" style={{ top: hoveredDetail.position.top, left: hoveredDetail.position.left }}>
                  <span>{hoveredDetail.detail}</span>
                </div>
              )}
            </span>
          ))}
        </div>
      </div>
      <div className="maskgroup-reports">
      {recentReports.map((report, index) => (
        <div className="report-item" key={index}>
          <div className="report-row">
            <span className="report-title">{`Report: ${report.report_id}`}</span>
            <span className="report-url">{`Report for the ${report.url}`}</span>
            <span className="report-date">
              {`Date: ${new Date(report.date).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}`}
            </span>
          </div>
          <div className="report-row">
            <span className="report-feature">{`Feature: ${report.feature}`}</span>
            <span className="report-subfeature">{`Sub-Feature: ${report.sub_feature}`}</span>
            <button className="view-report-button" onClick={() => handleReportClick(report.report_id)}>View Report</button>
          </div>
        </div>
      ))}
    </div>
    </div>
  );
};

export default Maskgroup;
