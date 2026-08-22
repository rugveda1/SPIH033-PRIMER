import React from 'react';
import { Construction } from 'lucide-react';
import Button from '../components/Button';

const PlaceholderPage = ({ title, description }) => {
  return (
    <div style={{
      minHeight: 'calc(100vh - 80px)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '4rem 1rem',
      paddingTop: '120px',
      textAlign: 'center'
    }}>
      <div className="glass-panel" style={{ padding: '4rem 2rem', maxWidth: '600px', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem' }}>
        <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'rgba(14, 165, 233, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Construction size={40} className="text-accent" />
        </div>
        <h1 className="heading-md">{title}</h1>
        <p className="text-lg text-muted">{description}</p>
        <div className="mt-4">
          <Button variant="primary" to="/">Back to Home</Button>
        </div>
      </div>
    </div>
  );
};

export default PlaceholderPage;
