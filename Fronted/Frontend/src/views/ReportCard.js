import React from 'react';

const ReportCard = ({ date, title, feature, sub_feature, reportId, onClick }) => {
  return (
    <div className="report-card">
      <div className="report-details">
        <span className="maskgroup-text246 BodyTextInter12Regular">
          <span>{date}</span>
        </span>
        <span className="maskgroup-text260 BodyTextInter14Regular">
          <span>{feature} - {sub_feature}</span>
        </span>
      </div>
      <button onClick={() => onClick(reportId)} className="view-report-button">
        View Report
      </button>
    </div>
  );
};

export default ReportCard;
