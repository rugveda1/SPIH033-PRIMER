import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Award, CheckCircle, AlertTriangle, BookOpen, Clock, RefreshCw, Star, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';

const Progress = () => {
  const { token, API_URL } = useAuth();
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchProgress = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/auth/me/progress`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setProgress(data);
      }
    } catch (err) {
      console.error('Error fetching progress statistics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProgress();
  }, [token, API_URL]);

  if (loading) {
    return (
      <div style={{
        minHeight: 'calc(100vh - 80px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        paddingTop: '100px',
        background: 'var(--bg-primary)',
        color: 'var(--text-primary)'
      }}>
        <div style={{ fontSize: '1.25rem' }}>Analyzing learning history...</div>
      </div>
    );
  }

  if (!progress) {
    return (
      <div style={{ minHeight: '100vh', paddingTop: '120px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <p>No progress data found. Try practicing a few questions first!</p>
      </div>
    );
  }

  // Friendly socratic helper tips for mistakes
  const getMistakeTip = (errorType) => {
    switch (errorType) {
      case 'place_value_error':
        return "We noticed some place value slips! Remember to align digits in their correct columns (Hundreds, Tens, Ones) before adding or subtracting.";
      case 'calculation_error':
        return "You're super close! Just minor calculation flips. Double check your counting step-by-step or count on your fingers to verify.";
      case 'multiplication_error':
        return "Multiplication can be tricky! Remember it is just adding the same number in equal groups. Draw out arrays to visualize.";
      case 'division_error':
        return "Division is all about sharing equally! Think of sharing cookies among friends so everyone gets the exact same amount.";
      default:
        return "Keep going! Reviewing the topic's Socratic rules and practicing short questions is the best way to grow.";
    }
  };

  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '4rem', background: 'var(--bg-primary)' }}>
      <div className="container">
        
        {/* Header toolbar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h1 className="heading-lg" style={{ fontWeight: 800 }}>My Progress <span className="text-gradient">Statistics</span></h1>
            <p className="text-muted mt-1">Review your mathematical strengths, weak topics, and assessment logs</p>
          </div>
          <button 
            onClick={fetchProgress}
            style={{
              padding: '0.6rem 1.25rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-color)',
              background: 'rgba(255,255,255,0.02)',
              color: 'var(--text-primary)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '0.95rem'
            }}
          >
            <RefreshCw size={16} /> Refresh Stats
          </button>
        </div>

        {/* Progress Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.5rem',
          marginBottom: '2.5rem'
        }}>
          {/* Overall average card */}
          <div className="glass-panel" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center' }}>
            <Award className="text-accent" size={48} style={{ marginBottom: '1rem' }} />
            <h3 style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Overall Class Mastery</h3>
            <div style={{ fontSize: '3rem', fontWeight: 800, margin: '0.5rem 0', color: 'var(--text-primary)' }}>
              {Math.round(progress.overall_mastery)}%
            </div>
            <div style={{ width: '80%', height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${progress.overall_mastery}%`, height: '100%', background: 'var(--accent-gradient)' }}></div>
            </div>
          </div>

          {/* Recommended topic card */}
          <div className="glass-panel" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
              <Star className="text-accent" size={20} />
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Recommended Next Step</h3>
            </div>
            {progress.recommended_next_topic ? (
              <>
                <h4 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.25rem' }}>{progress.recommended_next_topic.name}</h4>
                <p className="text-sm text-muted" style={{ marginBottom: '1.25rem' }}>{progress.recommended_next_topic.description}</p>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <Link to={`/practice?concept=${progress.recommended_next_topic.id}`} className="nav-link">
                    <Button variant="primary" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>Practice Now</Button>
                  </Link>
                </div>
              </>
            ) : (
              <p className="text-muted">You have mastered all concepts in this class! Excellent work! 🎉</p>
            )}
          </div>
        </div>

        {/* Strengths & Weaknesses block */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
          gap: '1.5rem',
          marginBottom: '2.5rem'
        }}>
          {/* Strengths Card */}
          <div className="glass-panel" style={{ padding: '1.75rem' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--success)' }}>
              <CheckCircle size={20} /> My Strengths (Score &ge; 80%)
            </h3>
            {progress.strengths.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {progress.strengths.map(s => (
                  <div key={s.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.5rem 0', borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                    <span style={{ fontSize: '0.95rem' }}>{s.name}</span>
                    <span style={{ color: 'var(--success)', fontWeight: 600, fontSize: '0.95rem' }}>{Math.round(s.score)}% Mastery</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted text-sm">Keep practicing to build topic strengths!</p>
            )}
          </div>

          {/* Weaknesses Card */}
          <div className="glass-panel" style={{ padding: '1.75rem' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--warning)' }}>
              <AlertTriangle size={20} /> Areas to Improve (Score &lt; 80%)
            </h3>
            {progress.weaknesses.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {progress.weaknesses.map(w => (
                  <div key={w.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.5rem 0', borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                    <span style={{ fontSize: '0.95rem' }}>{w.name}</span>
                    <span style={{ color: 'var(--warning)', fontWeight: 600, fontSize: '0.95rem' }}>{Math.round(w.score)}% Mastery</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted text-sm">Brilliant! No weak topics detected.</p>
            )}
          </div>
        </div>

        {/* Mistakes logs */}
        {progress.recent_mistakes.length > 0 && (
          <div className="glass-panel" style={{ padding: '1.75rem', marginBottom: '2.5rem', borderLeft: '4px solid var(--warning)' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ShieldAlert className="text-warning" size={22} /> Socratic Feedback on Recent Mistakes
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {progress.recent_mistakes.map((mistake, idx) => (
                <div key={idx} style={{ padding: '1rem', background: 'rgba(255,255,255,0.01)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                  <span style={{ textTransform: 'capitalize', fontWeight: 700, fontSize: '0.95rem', color: 'var(--warning)' }}>
                    {mistake.replace('_', ' ')}
                  </span>
                  <p className="text-muted text-sm mt-1">{getMistakeTip(mistake)}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Learning History table */}
        <div className="glass-panel" style={{ padding: '1.75rem', marginBottom: '2.5rem', overflowX: 'auto' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Clock size={20} className="text-accent" /> Recent Learning Log (Last 10 Attempts)
          </h3>
          {progress.learning_history.length > 0 ? (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', minWidth: '550px' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border-color)', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Concept</th>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Question</th>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Result</th>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Error Pattern</th>
                </tr>
              </thead>
              <tbody>
                {progress.learning_history.map(hist => (
                  <tr key={hist.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', fontSize: '0.925rem' }}>
                    <td style={{ padding: '0.75rem 0.5rem', fontWeight: 600 }}>{hist.concept_name}</td>
                    <td style={{ padding: '0.75rem 0.5rem', color: 'var(--text-secondary)' }}>{hist.question_text}</td>
                    <td style={{ padding: '0.75rem 0.5rem', color: hist.is_correct ? 'var(--success)' : 'var(--error)' }}>
                      {hist.is_correct ? 'Correct' : 'Incorrect'}
                    </td>
                    <td style={{ padding: '0.75rem 0.5rem', color: 'var(--text-muted)', textTransform: 'capitalize' }}>
                      {hist.is_correct ? '-' : hist.error_type.replace('_', ' ')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-muted text-sm">No recent attempts logged. Go practice to populate history logs.</p>
          )}
        </div>

        {/* Assessments history table */}
        <div className="glass-panel" style={{ padding: '1.75rem', overflowX: 'auto' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <BookOpen size={20} className="text-accent" /> Completed Assessments
          </h3>
          {progress.completed_assessments.length > 0 ? (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', minWidth: '500px' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border-color)', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                  <th style={{ padding: '0.75rem 0.5rem' }}>ID</th>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Test Type</th>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Score</th>
                  <th style={{ padding: '0.75rem 0.5rem' }}>Completed Date</th>
                </tr>
              </thead>
              <tbody>
                {progress.completed_assessments.map(ass => (
                  <tr key={ass.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)', fontSize: '0.925rem' }}>
                    <td style={{ padding: '0.75rem 0.5rem', color: 'var(--text-muted)' }}>#{ass.id}</td>
                    <td style={{ padding: '0.75rem 0.5rem', textTransform: 'capitalize', fontWeight: 600 }}>{ass.assessment_type}</td>
                    <td style={{ padding: '0.75rem 0.5rem', color: 'var(--accent-primary)', fontWeight: 700 }}>{ass.score}%</td>
                    <td style={{ padding: '0.75rem 0.5rem', color: 'var(--text-muted)' }}>{new Date(ass.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-muted text-sm">No assessments completed yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Progress;
