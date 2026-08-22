import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { BookOpen, MessageSquare, Lock, CheckCircle2 } from 'lucide-react';
import Button from '../components/Button';

const Courses = () => {
  const { token, user, API_URL } = useAuth();
  const [selectedClass, setSelectedClass] = useState(user.class_level || 1);
  const [concepts, setConcepts] = useState([]);
  const [readinessMap, setReadinessMap] = useState({});
  const [loading, setLoading] = useState(true);

  const classes = [1, 2, 3, 4, 5];

  useEffect(() => {
    const fetchSyllabus = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_URL}/api/concepts?class_level=${selectedClass}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setConcepts(data);

          // Fetch readiness context for each concept to verify locking/mastery scores
          const readPromises = data.map(async (c) => {
            const readyRes = await fetch(`${API_URL}/api/concepts/${c.id}/ready`, {
              headers: { 'Authorization': `Bearer ${token}` }
            });
            if (readyRes.ok) {
              const rData = await readyRes.json();
              return { id: c.id, data: rData };
            }
            return { id: c.id, data: null };
          });

          const results = await Promise.all(readPromises);
          const rMap = {};
          results.forEach(r => {
            if (r.data) rMap[r.id] = r.data;
          });
          setReadinessMap(rMap);
        }
      } catch (err) {
        console.error('Error fetching concept map:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSyllabus();
  }, [selectedClass, token, API_URL]);

  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '4rem', background: 'var(--bg-primary)' }}>
      <div className="container">
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h1 className="heading-lg" style={{ fontWeight: 800 }}>Mathematics <span className="text-gradient">Mastery Map</span></h1>
          <p className="text-muted mt-2">Explore math concepts, unlock levels, and master prerequisites sequentially</p>
        </div>

        {/* Class Selector Tabs */}
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '0.75rem',
          marginBottom: '2.5rem',
          flexWrap: 'wrap'
        }}>
          {classes.map(c => (
            <button
              key={c}
              onClick={() => setSelectedClass(c)}
              style={{
                padding: '0.75rem 1.5rem',
                borderRadius: 'var(--radius-full)',
                border: '1px solid',
                borderColor: selectedClass === c ? 'var(--accent-primary)' : 'var(--border-color)',
                background: selectedClass === c ? 'var(--accent-gradient)' : 'var(--bg-tertiary)',
                color: selectedClass === c ? '#ffffff' : 'var(--text-primary)',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all var(--transition-fast)'
              }}
            >
              Class {c}
              {user.class_level === c && <span style={{ marginLeft: '6px', fontSize: '0.75rem', background: 'rgba(255,255,255,0.2)', padding: '2px 6px', borderRadius: '4px' }}>My Class</span>}
            </button>
          ))}
        </div>

        {/* Syllabus Grid */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
            Loading Class {selectedClass} pathway...
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '1.5rem'
          }}>
            {concepts.map((concept, index) => {
              const readiness = readinessMap[concept.id];
              const isReady = readiness ? readiness.is_ready : (index === 0);
              
              // We'll extract current mastery from the prerequisite check response if it checks itself,
              // or compute from attempts. Let's make sure if there is no mastery, it defaults.
              // Actually, since get_learning_context yields it, let's verify if the concept is mastered.
              // We can determine mastery status based on prerequisites:
              // Let's assume if score >= 80 it's mastered. Let's see if the student already completed it.
              // We'll calculate score or show it. Let's assume we can fetch the mastery directly or mock
              // score details for styling.
              // Let's query the mastery status: if we don't have score in readiness, we default.
              // Wait, let's assume we can check if it's mastered by looking at its score.
              // Since the API returns prerequisites with mastery, we can calculate readiness.
              // To get the mastery score of this specific concept:
              // We'll show a mastery progress bar or status.
              // Let's fetch mastery from the readiness context. We can calculate it or display a placeholder.
              
              return (
                <div 
                  key={concept.id}
                  className="glass-panel"
                  style={{
                    padding: '1.75rem',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    position: 'relative',
                    transition: 'all var(--transition-normal)',
                    opacity: isReady ? 1 : 0.65,
                    border: isReady ? '1px solid var(--border-color)' : '1px solid rgba(255,255,255,0.03)'
                  }}
                >
                  <div>
                    {/* Status Icons */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
                      <span className="text-xs text-muted" style={{ fontWeight: 600 }}>TOPIC {index + 1}</span>
                      {!isReady ? (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                          <Lock size={14} /> Locked
                        </span>
                      ) : (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.8rem', color: 'var(--success)' }}>
                          <CheckCircle2 size={14} /> Ready
                        </span>
                      )}
                    </div>

                    <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>{concept.name}</h3>
                    <p className="text-sm text-muted" style={{ marginBottom: '1.5rem', lineHeight: '1.4' }}>{concept.description}</p>
                    
                    {/* Objectives list */}
                    {concept.learning_objectives && concept.learning_objectives.length > 0 && (
                      <div style={{ marginBottom: '1.5rem' }}>
                        <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>Learning Objectives:</h4>
                        <ul style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                          {concept.learning_objectives.map(obj => (
                            <li key={obj} style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                              <span style={{ width: '4px', height: '4px', borderRadius: '50%', background: 'var(--accent-primary)' }}></span>
                              {obj}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.5rem' }}>
                    <Button
                      variant="primary"
                      to={`/practice?concept=${concept.id}`}
                      disabled={!isReady}
                      style={{ flex: 1, padding: '0.6rem 1rem', fontSize: '0.875rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem' }}
                    >
                      <BookOpen size={15} /> Practice
                    </Button>
                    <Button
                      variant="ghost"
                      to={`/tutor?concept=${concept.id}`}
                      disabled={!isReady}
                      style={{ flex: 1, padding: '0.6rem 1rem', fontSize: '0.875rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.35rem' }}
                    >
                      <MessageSquare size={15} /> Socratic Tutor
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default Courses;
