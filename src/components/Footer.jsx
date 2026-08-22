import React from 'react';
import { Link } from 'react-router-dom';
import { BrainCircuit, Mail, Share2, Globe } from 'lucide-react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          <div className="footer-brand">
            <Link to="/" className="navbar-logo">
              <BrainCircuit className="logo-icon" size={28} />
              <span className="logo-text">AI Tutor</span>
            </Link>
            <p className="footer-description">
              Your personalized learning journey powered by adaptive AI. Learn at your pace, master difficult concepts, and reach your goals.
            </p>
            <div className="social-links">
              <a href="#" className="social-link" aria-label="Mail"><Mail size={20} /></a>
              <a href="#" className="social-link" aria-label="Share"><Share2 size={20} /></a>
              <a href="#" className="social-link" aria-label="Globe"><Globe size={20} /></a>
            </div>
          </div>
          
          <div className="footer-links-group">
            <h4 className="footer-heading">Product</h4>
            <ul className="footer-links">
              <li><Link to="/#features">Features</Link></li>
              <li><Link to="/#how-it-works">How It Works</Link></li>
              <li><Link to="/dashboard">LMS</Link></li>
              <li><Link to="/#pricing">Pricing</Link></li>
            </ul>
          </div>
          
          <div className="footer-links-group">
            <h4 className="footer-heading">Community</h4>
            <ul className="footer-links">
              <li><Link to="/#community">Learner Stories</Link></li>
              <li><Link to="/#forum">Forums</Link></li>
              <li><Link to="/#discord">Discord Server</Link></li>
              <li><Link to="/#events">Events</Link></li>
            </ul>
          </div>
          
          <div className="footer-links-group">
            <h4 className="footer-heading">Company</h4>
            <ul className="footer-links">
              <li><Link to="/about">About Us</Link></li>
              <li><Link to="/contact">Contact</Link></li>
              <li><Link to="/privacy">Privacy Policy</Link></li>
              <li><Link to="/terms">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} AI Tutor. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
