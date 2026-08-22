import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { BrainCircuit, Mail, Lock, User, GraduationCap } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Button from '../components/Button';
import './Auth.css';

const Signup = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [classLevel, setClassLevel] = useState(1);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !email || !password) {
      setError('Please fill in all fields');
      return;
    }

    setError('');
    setSubmitting(true);

    try {
      const success = await signup(name, email, password, classLevel);
      if (success) {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container glass-panel">
        <div className="auth-header text-center">
          <Link to="/" className="auth-logo">
            <BrainCircuit className="logo-icon" size={32} />
          </Link>
          <h2 className="heading-md mt-4">Create your account</h2>
          <p className="text-muted mt-2">Start your personalized mathematics learning journey</p>
        </div>

        {error && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid var(--error)',
            color: 'var(--error)',
            padding: '0.75rem',
            borderRadius: 'var(--radius-sm)',
            marginTop: '1.5rem',
            fontSize: '0.875rem',
            textAlign: 'center'
          }}>
            {error}
          </div>
        )}

        <form className="auth-form mt-8" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <div className="input-with-icon">
              <User size={18} className="input-icon" />
              <input 
                type="text" 
                placeholder="John Doe" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Email</label>
            <div className="input-with-icon">
              <Mail size={18} className="input-icon" />
              <input 
                type="email" 
                placeholder="you@example.com" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-with-icon">
              <Lock size={18} className="input-icon" />
              <input 
                type="password" 
                placeholder="••••••••" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Select Mathematics Class Level</label>
            <div className="input-with-icon">
              <GraduationCap size={18} className="input-icon" />
              <select 
                value={classLevel} 
                onChange={(e) => setClassLevel(Number(e.target.value))}
                style={{
                  width: '100%',
                  padding: '0.875rem 1rem',
                  paddingLeft: '2.75rem',
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--text-primary)',
                  outline: 'none',
                  fontSize: '1rem',
                  appearance: 'none',
                  cursor: 'pointer'
                }}
              >
                <option value={1} style={{ background: '#18181b' }}>Class 1 (Counting & Addition Intro)</option>
                <option value={2} style={{ background: '#18181b' }}>Class 2 (Skip Counting & 2-Digit Math)</option>
                <option value={3} style={{ background: '#18181b' }}>Class 3 (Multiplication & Decimals Intro)</option>
                <option value={4} style={{ background: '#18181b' }}>Class 4 (Long Division & Geometry)</option>
                <option value={5} style={{ background: '#18181b' }}>Class 5 (Fractions, Percentages & Word Problems)</option>
              </select>
            </div>
          </div>

          <Button 
            variant="primary" 
            className="w-full mt-6" 
            type="submit"
            disabled={submitting}
          >
            {submitting ? 'Registering...' : 'Create Account & Start'}
          </Button>
        </form>

        <div className="auth-footer text-center mt-8">
          <p className="text-muted">
            Already have an account? <Link to="/login" className="text-accent">Log in</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
