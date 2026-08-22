import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ChevronLeft, Award, Check, X as WrongIcon, AlertCircle } from 'lucide-react';
import Button from '../components/Button';

const Assessment = () => {
  const { token, API_URL } = useAuth();
  const [searchParams] = useSearchParams();
  const type = searchParams.get('type') || 'diagnostic';
  const conceptId = searchParams.get('concept') ? Number(searchParams.get('concept')) : null;

  const [assessmentId, setAssessmentId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const startTest = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_URL}/api/assessments/start`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            assessment_type: type,
            concept_id: conceptId
          })
        });

        if (res.ok) {
          const data = await res.json();
          setAssessmentId(data.assessment_id);
          setQuestions(data.questions);
        } else {
          setError('Failed to initialize the assessment.');
        }
      } catch (err) {
        console.error('Error starting assessment:', err);
        setError('Error initializing assessment.');
      } finally {
        setLoading(false);
      }
    };

    startTest();
  }, [type, conceptId, token, API_URL]);

  const selectOption = (opt) => {
    const q = questions[currentIndex];
    setAnswers(prev => ({
      ...prev,
      [q.id]: opt
    }));
  };

  const handleNext = () => {
    setCurrentIndex(prev => Math.min(prev + 1, questions.length - 1));
  };

  const handlePrev = () => {
    setCurrentIndex(prev => Math.max(prev - 1, 0));
  };

  const handleSubmit = async () => {
    // Verify all questions answered
    const unanswered = questions.some(q => !answers[q.id]);
    if (unanswered) {
      setError('Please answer all questions before submitting.');
      return;
    }

    setError('');
    setSubmitting(true);

    try {
      const payloadAnswers = questions.map(q => ({
        question_id: q.id,
        submitted_answer: answers[q.id]
      }));

      const res = await fetch(`${API_URL}/api/assessments/${assessmentId}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          answers: payloadAnswers
        })
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
      } else {
        setError('Failed to submit assessment answers.');
      }
    } catch (err) {
      console.error('Error submitting assessment:', err);
      setError('Error submitting test.');
    } finally {
      setSubmitting(false);
    }
  };

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
        <div style={{ fontSize: '1.25rem' }}>Constructing assessment questions...</div>
      </div>
    );
  }

  const q = questions[currentIndex];

  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '4rem', background: 'var(--bg-primary)' }}>
      <div className="container" style={{ maxWidth: '800px' }}>
        
        {/* Header Back Button */}
        {!result && (
          <Link to="/dashboard" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', width: 'fit-content' }}>
            <ChevronLeft size={16} /> Cancel Test
          </Link>
        )}

        {/* Header Title */}
        <div style={{ marginBottom: '2.5rem', textAlign: result ? 'center' : 'left' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--accent-primary)', fontWeight: 600, textTransform: 'uppercase' }}>
            {type} Assessment
          </span>
          <h1 className="heading-sm" style={{ fontWeight: 700, marginTop: '0.25rem' }}>
            {result ? 'Assessment Results' : `Question ${currentIndex + 1} of ${questions.length}`}
          </h1>
        </div>

        {error && (
          <div className="glass-panel" style={{ padding: '1rem', border: '1px solid var(--error)', color: 'var(--error)', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {/* Results Screen */}
        {result ? (
          <div className="glass-panel" style={{ padding: '2.5rem', textAlign: 'center' }}>
            <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'rgba(14, 165, 233, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
              <Award className="text-accent" size={40} />
            </div>
            <h2 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.5rem' }}>{result.score}% Score</h2>
            <p className="text-muted" style={{ marginBottom: '2.5rem' }}>
              Awesome effort! We've registered this assessment and updated your Socratic learning pathway.
            </p>

            {/* Individual Answers Breakdown */}
            <div style={{ textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2rem' }}>
              {result.results.map((resItem, idx) => (
                <div key={idx} style={{ padding: '1.25rem 1.5rem', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)', background: 'rgba(255,255,255,0.01)' }}>
                  <h4 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.75rem', display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                    <span style={{ color: 'var(--accent-primary)', fontWeight: 700 }}>Q{idx + 1}.</span>
                    {resItem.question_text}
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', fontSize: '0.9rem', marginBottom: '0.75rem' }}>
                    <div>
                      <span className="text-muted">Your answer: </span>
                      <span style={{ fontWeight: 600, color: resItem.is_correct ? 'var(--success)' : 'var(--error)' }}>{resItem.submitted_answer}</span>
                      {resItem.is_correct ? (
                        <Check size={16} className="text-success" style={{ display: 'inline', marginLeft: '6px' }} />
                      ) : (
                        <WrongIcon size={16} className="text-error" style={{ display: 'inline', marginLeft: '6px' }} />
                      )}
                    </div>
                    {!resItem.is_correct && (
                      <div>
                        <span className="text-muted">Correct answer: </span>
                        <span style={{ fontWeight: 600, color: 'var(--success)' }}>{resItem.correct_answer}</span>
                      </div>
                    )}
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)', paddingTop: '0.50rem' }}>
                    <strong>Explanation:</strong> {resItem.explanation}
                  </p>
                </div>
              ))}
            </div>

            <Button variant="primary" to="/dashboard" style={{ padding: '0.75rem 2rem' }}>
              Go to Dashboard
            </Button>
          </div>
        ) : (
          /* Question Interface */
          q && (
            <div className="glass-panel" style={{ padding: '2rem' }}>
              {/* Question Text */}
              <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1.75rem', lineHeight: '1.5' }}>
                {q.question_text}
              </h2>

              {/* Option Grid */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '2.5rem' }}>
                {q.options.map((opt) => {
                  const isSelected = answers[q.id] === opt;
                  return (
                    <label 
                      key={opt}
                      style={{
                        padding: '1rem 1.25rem',
                        background: isSelected ? 'rgba(14, 165, 233, 0.1)' : 'rgba(0, 0, 0, 0.02)',
                        border: '1px solid',
                        borderColor: isSelected ? 'var(--accent-primary)' : 'var(--border-color)',
                        borderRadius: 'var(--radius-md)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.75rem',
                        cursor: 'pointer',
                        transition: 'all var(--transition-fast)'
                      }}
                    >
                      <input
                        type="radio"
                        name={`q-${q.id}`}
                        value={opt}
                        checked={isSelected}
                        onChange={() => selectOption(opt)}
                        style={{ accentColor: 'var(--accent-primary)', width: '16px', height: '16px' }}
                      />
                      <span style={{ fontSize: '1rem', color: 'var(--text-primary)', fontWeight: 500 }}>{opt}</span>
                    </label>
                  );
                })}
              </div>

              {/* Bottom Nav toolbar */}
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Button 
                  variant="ghost" 
                  onClick={handlePrev}
                  disabled={currentIndex === 0}
                  style={{ padding: '0.6rem 1.5rem' }}
                >
                  Previous
                </Button>

                {currentIndex < questions.length - 1 ? (
                  <Button 
                    variant="primary" 
                    onClick={handleNext}
                    disabled={!answers[q.id]}
                    style={{ padding: '0.6rem 1.5rem' }}
                  >
                    Next
                  </Button>
                ) : (
                  <Button 
                    variant="primary" 
                    onClick={handleSubmit}
                    disabled={submitting || !answers[q.id]}
                    style={{ padding: '0.6rem 1.75rem' }}
                  >
                    {submitting ? 'Submitting...' : 'Submit Answers'}
                  </Button>
                )}
              </div>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default Assessment;
