import React from 'react';
import './FeatureCard.css';

const FeatureCard = ({ icon: Icon, title, description, label }) => {
  return (
    <div className="feature-card glass-panel">
      {label && <span className="feature-label">{label}</span>}
      <div className="feature-icon-wrapper">
        <Icon className="feature-icon" size={24} />
      </div>
      <h3 className="feature-title">{title}</h3>
      <p className="feature-description">{description}</p>
    </div>
  );
};

export default FeatureCard;
