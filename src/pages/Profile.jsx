import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { User, Mail, GraduationCap, Save, LogOut, CheckCircle, AlertCircle } from 'lucide-react';
import Button from '../components/Button';

const Profile = () => {
  const { user, updateProfile, logout } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [classLevel, setClassLevel] = useState(user?.class_level || 1);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Name cannot be empty');
      return;
    }

    setError('');
    setSuccess(false);
    setSubmitting(true);

    try {
      const ok = await updateProfile({
        name,
        class_level: Number(classLevel)
      });
      if (ok) {
        setSuccess(true);
      }
    } catch (err) {
      setError(err.message || 'Failed to update profile details.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '4rem', background: 'var(--bg-primary)' }}>
      <div className="container" style={{ maxWidth: '600px' }}>
        
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <h1 className="heading-sm" style={{ fontWeight: 800 }}>Student Profile</h1>
          <p className="text-muted mt-1">Manage your account details and learning configurations</p>
        </div>

        {success && (
          <div className="glass-panel" style={{ padding: '1rem', border: '1px solid var(--success)', color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
            <CheckCircle size={20} />
            <span>Profile successfully updated!</span>
          </div>
        )}

        {error && (
          <div className="glass-panel" style={{ padding: '1rem', border: '1px solid var(--error)', color: 'var(--error)', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {/* Profile Card Form */}
        <div className="glass-panel" style={{ padding: '2rem', marginBottom: '1.5rem' }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            
            {/* Name Input */}
            <div className="form-group">
              <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Full Name</label>
              <div className="input-with-icon" style={{ position: 'relative' }}>
                <User size={18} className="input-icon" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                <input 
                  type="text" 
                  value={name} 
                  onChange={(e) => setName(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '0.85rem 1rem',
                    paddingLeft: '2.75rem',
                    background: 'var(--bg-tertiary)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)',
                    outline: 'none',
                    fontSize: '1rem'
                  }}
                />
              </div>
            </div>

            {/* Email (Disabled) */}
            <div className="form-group">
              <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Email Address (Cannot change)</label>
              <div style={{ position: 'relative' }}>
                <Mail size={18} className="input-icon" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                <input 
                  type="email" 
                  value={user?.email || ''} 
                  disabled
                  style={{
                    width: '100%',
                    padding: '0.85rem 1rem',
                    paddingLeft: '2.75rem',
                    background: 'var(--bg-tertiary)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-muted)',
                    outline: 'none',
                    fontSize: '1rem',
                    cursor: 'not-allowed'
                  }}
                />
              </div>
            </div>

            {/* Class Level Select */}
            <div className="form-group">
              <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Mathematics Class Level</label>
              <div style={{ position: 'relative' }}>
                <GraduationCap size={18} className="input-icon" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                <select 
                  value={classLevel} 
                  onChange={(e) => setClassLevel(Number(e.target.value))}
                  style={{
                    width: '100%',
                    padding: '0.85rem 1rem',
                    paddingLeft: '2.75rem',
                    background: 'var(--bg-tertiary)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)',
                    outline: 'none',
                    fontSize: '1rem',
                    appearance: 'none',
                    cursor: 'pointer'
                  }}
                >
                  <option value={1} style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>Class 1</option>
                  <option value={2} style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>Class 2</option>
                  <option value={3} style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>Class 3</option>
                  <option value={4} style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>Class 4</option>
                  <option value={5} style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)' }}>Class 5</option>
                </select>
              </div>
            </div>

            <Button 
              type="submit" 
              variant="primary" 
              disabled={submitting}
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem', marginTop: '0.5rem' }}
            >
              <Save size={16} /> {submitting ? 'Saving Changes...' : 'Save Settings'}
            </Button>
          </form>
        </div>

        {/* Danger logout container */}
        <div className="glass-panel" style={{ padding: '1.5rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700 }}>Exit Learning Session</h4>
            <p className="text-xs text-muted">You will be logged out of this device.</p>
          </div>
          <Button variant="ghost" onClick={logout} style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--error)', borderColor: 'rgba(239, 68, 68, 0.2)' }}>
            <LogOut size={16} /> Log Out
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
