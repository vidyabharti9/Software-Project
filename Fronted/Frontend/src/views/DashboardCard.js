import React from 'react';

const DashboardCard = ({ title, value, percentage, className, arrowClass }) => {
  return (
    <div className={className}>
      <div className="dashboard-card-content">
        <div className="card-title">
          <span className="maskgroup-text145 BodyTextInter16Medium">
            <span>{title}</span>
          </span>
        </div>
        <div className="card-value">
          <span className="maskgroup-text147">
            <span>{value}</span>
          </span>
          <div className="maskgroup-badge-tag10">
            <span className="maskgroup-text149">
              <span>{percentage}</span>
            </span>
            <span className={arrowClass}></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardCard;
