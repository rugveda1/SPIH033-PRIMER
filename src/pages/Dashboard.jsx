import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Award, Compass, Play, BookOpen, MessageSquare, ClipboardList } from 'lucide-react';
import Button from '../components/Button';

const Dashboard = () => {
  const { user, token, API_URL } = useAuth();
  const [recommendation, setRecommendation] = useState(null);
  const [concepts, setConcepts] = useState([]);
  const [masteryList, setMasteryList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch next recommended concept
        const recRes = await fetch(`${API_URL}/api/recommendations/next`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (recRes.ok) {
          const recData = await recRes.json();
          setRecommendation(recData);
        }

        // Fetch concepts for the student's class level
        const conceptsRes = await fetch(`${API_URL}/api/concepts?class_level=${user.class_level}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (conceptsRes.ok) {
          const conceptsData = await conceptsRes.json();
          setConcepts(conceptsData);

          // For each concept, check readiness & mastery
          const masteryPromises = conceptsData.map(async (c) => {
            const readyRes = await fetch(`${API_URL}/api/concepts/${c.id}/ready`, {
              headers: { 'Authorization': `Bearer ${token}` }
            });
            if (readyRes.ok) {
              const readyData = await readyRes.json();
              // Calculate mastery score for this concept (which is returned in the prerequisites status,
              // but we can query it directly or extract from readiness)
              return { conceptId: c.id, isReady: readyData.is_ready, readinessData: readyData };
            }
            return { conceptId: c.id, isReady: false };
          });

          const readinessResults = await Promise.all(masteryPromises);

          // Get mastery records to calculate average mastery
          const masteryMap = {};
          readinessResults.forEach(r => {
            masteryMap[r.conceptId] = r;
          });
          setMasteryList(readinessResults);
        }
      } catch (err) {
        console.error('Error fetching dashboard statistics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user.class_level, token, API_URL]);

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
        <div style={{ fontSize: '1.25rem' }}>Loading learning metrics...</div>
      </div>
    );
  }

  // Calculate stats
  const totalConceptsCount = concepts.length;
  // Calculate average mastery score or similar from user progress
  // Since we don't have a direct average API, we can calculate from readiness results or mock
  // Let's check readiness status for concepts. We'll query if any are mastered.
  // Actually, we can get mastery records by fetching an API or from the local state
  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '3rem', background: 'var(--bg-primary)' }}>
      <div className="container">
        {/* Welcome Section */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h1 className="heading-lg" style={{ fontWeight: 800 }}>Welcome back, <span className="text-gradient">{user.name}</span>!</h1>
            <p className="text-muted mt-1">Ready to learn some mathematics today? You are placed in Class {user.class_level}.</p>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <Button variant="ghost" to="/assessment?type=diagnostic" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ClipboardList size={18} /> Diagnostic Assessment
            </Button>
            <Button variant="primary" to="/courses" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Play size={18} /> Resume Journey
            </Button>
          </div>
        </div>

        {/* Stats Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.5rem',
          marginBottom: '2.5rem'
        }}>
          {/* Recommendation Card */}
          <div className="glass-panel" style={{ padding: '1.75rem', position: 'relative', overflow: 'hidden' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <Compass className="text-accent" size={24} />
              <h3 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Recommended Next Step</h3>
            </div>
            {recommendation ? (
              <>
                <h4 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                  {recommendation.name}
                </h4>
                <p className="text-muted text-sm" style={{ marginBottom: '1.5rem', minHeight: '40px' }}>
                  {recommendation.description}
                </p>
                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  <Button variant="primary" to={`/practice?concept=${recommendation.id}`} style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}>
                    Practice Question
                  </Button>
                  <Button variant="ghost" to={`/tutor?concept=${recommendation.id}`} style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}>
                    Socratic Chat
                  </Button>
                </div>
              </>
            ) : (
              <p className="text-muted">Analyzing your learning pathway...</p>
            )}
          </div>

          {/* Overall Stats Card */}
          <div className="glass-panel" style={{ padding: '1.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <Award className="text-accent" size={24} />
              <h3 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Mathematics Class {user.class_level}</h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span className="text-muted">Mastery Map Progress</span>
                  <span className="text-accent" style={{ fontWeight: 600 }}>{totalConceptsCount} Topics</span>
                </div>
                <div style={{ height: '8px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '100%', height: '100%', background: 'var(--accent-gradient)' }}></div>
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0' }}>
                <div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Learning Goal</div>
                  <div style={{ fontSize: '1rem', fontWeight: 600 }}>Master all Class {user.class_level} topics</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Current Status</div>
                  <div style={{ fontSize: '1rem', color: 'var(--success)', fontWeight: 600 }}>Active Learner</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Syllabus / Class Concept Pathway */}
        <h2 className="heading-sm" style={{ marginBottom: '1.5rem', fontWeight: 700 }}>Active Concepts</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {concepts.map((concept, index) => {
            const mastery = masteryList.find(m => m.conceptId === concept.id);
            const isReady = mastery ? mastery.isReady : (index === 0);
            
            return (
              <div 
                key={concept.id} 
                className="glass-panel" 
                style={{ 
                  padding: '1.25rem 1.75rem', 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  gap: '1rem',
                  opacity: isReady ? 1 : 0.65
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1, minWidth: '250px' }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    background: isReady ? 'rgba(14, 165, 233, 0.12)' : 'rgba(0, 0, 0, 0.04)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    color: isReady ? 'var(--accent-primary)' : 'var(--text-muted)'
                  }}>
                    {index + 1}
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {concept.name}
                      {!isReady && <span style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px', color: 'var(--text-muted)' }}>Locked</span>}
                      {isReady && <span style={{ fontSize: '0.75rem', background: 'rgba(16,185,129,0.1)', padding: '2px 6px', borderRadius: '4px', color: 'var(--success)' }}>Ready</span>}
                    </h3>
                    <p className="text-muted text-sm mt-0.5">{concept.description}</p>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <Button 
                      variant="primary" 
                      to={`/practice?concept=${concept.id}`} 
                      disabled={!isReady}
                      style={{ padding: '0.5rem 1rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
                    >
                      <BookOpen size={14} /> Practice
                    </Button>
                    <Button 
                      variant="ghost" 
                      to={`/tutor?concept=${concept.id}`} 
                      disabled={!isReady}
                      style={{ padding: '0.5rem 1rem', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
                    >
                      <MessageSquare size={14} /> Tutor
                    </Button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
