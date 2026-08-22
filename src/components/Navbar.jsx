import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BrainCircuit, Menu, X, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Button from './Button';
import './Navbar.css';

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  const navLinks = user 
    ? [
        { name: 'Dashboard', path: '/dashboard' },
        { name: 'Mastery Map', path: '/courses' },
        { name: 'Socratic Tutor', path: '/tutor' },
        { name: 'Progress Stats', path: '/progress' },
        { name: 'Profile', path: '/profile' },
      ]
    : [
        { name: 'Home', path: '/' },
        { name: 'How It Works', path: '/#how-it-works' },
        { name: 'Features', path: '/#features' },
        { name: 'FAQ', path: '/#faq' },
      ];

  return (
    <header className={`navbar ${isScrolled ? 'scrolled' : ''}`}>
      <div className="container navbar-container">
        <Link to="/" className="navbar-logo">
          <BrainCircuit className="logo-icon" size={28} />
          <span className="logo-text">AI Tutor</span>
        </Link>

        <nav className={`navbar-links ${mobileMenuOpen ? 'open' : ''}`}>
          {navLinks.map((link) => (
            <Link key={link.name} to={link.path} className="nav-link">
              {link.name}
            </Link>
          ))}
          
          <div className="navbar-actions-mobile">
            {user ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
                <span className="text-sm text-muted">Class {user.class_level} • {user.name}</span>
                <Button variant="ghost" onClick={logout} className="w-full">
                  <LogOut size={16} style={{ marginRight: '8px' }} /> Log Out
                </Button>
              </div>
            ) : (
              <>
                <Button variant="ghost" to="/login">Log In</Button>
                <Button variant="primary" to="/signup">Start Learning</Button>
              </>
            )}
          </div>
        </nav>

        <div className="navbar-actions">
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span className="text-muted" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem' }}>
                <User size={16} /> Class {user.class_level} • {user.name}
              </span>
              <Button variant="ghost" onClick={logout}>
                <LogOut size={16} style={{ marginRight: '8px' }} /> Log Out
              </Button>
            </div>
          ) : (
            <>
              <Button variant="ghost" to="/login">Log In</Button>
              <Button variant="primary" to="/signup">Start Learning</Button>
            </>
          )}
        </div>

        <button 
          className="mobile-menu-btn"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle Menu"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
    </header>
  );
};

export default Navbar;
