import React from 'react';
import './Button.css';
import { Link } from 'react-router-dom';

const Button = ({ children, variant = 'primary', to, onClick, className = '', ...props }) => {
  const baseClass = `btn btn-${variant} ${className}`;
  
  if (to) {
    return (
      <Link to={to} className={baseClass} {...props}>
        {children}
      </Link>
    );
  }
  
  return (
    <button className={baseClass} onClick={onClick} {...props}>
      {children}
    </button>
  );
};

export default Button;
