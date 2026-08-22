import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Brain, ArrowRight, MessageSquare, ChevronLeft, AlertCircle, HelpCircle as HelpIcon } from 'lucide-react';
import Button from '../components/Button';

const Practice = () => {
  const { token, API_URL } = useAuth();
  const [searchParams] = useSearchParams();
  const conceptId = Number(searchParams.get('concept'));
  const navigate = useNavigate();

  const [concept, setConcept] = useState(null);
  const [question, setQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [answered, setAnswered] = useState(false);
  const [result, setResult] = useState(null);
  const [hint, setHint] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadQuestion = React.useCallback(async () => {
    setLoading(true);
    setAnswered(false);
    setSelectedOption('');
    setResult(null);
    setHint('');
    try {
      const res = await fetch(`${API_URL}/api/practice/question?concept_id=${conceptId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setQuestion(data);
      } else {
        setError('Failed to fetch a practice question');
      }
    } catch (err) {
      console.error('Error loading question:', err);
      setError('Error loading question.');
    } finally {
      setLoading(false);
    }
  }, [API_URL, conceptId, token]);

  useEffect(() => {
    if (!conceptId) {
      navigate('/courses');
      return;
    }

    const fetchConceptDetails = async () => {
      try {
        const res = await fetch(`${API_URL}/api/concepts/${conceptId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setConcept(data);
          loadQuestion();
        } else {
          setError('Failed to load concept details');
          setLoading(false);
        }
      } catch (err) {
        console.error('Error fetching concept details:', err);
        setError('Error loading practice topic.');
        setLoading(false);
      }
    };

    fetchConceptDetails();
  }, [conceptId, token, API_URL, navigate, loadQuestion]);

  const getHint = async () => {
    if (!question) return;
    setHint('Thinking of a clue...');
    try {
      const res = await fetch(`${API_URL}/api/chat/hint`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          concept_id: conceptId,
          question_id: question.id
        })
      });

      if (res.ok) {
        const data = await res.json();
        setHint(data.hint);
      } else {
        setHint('Sorry, I couldn\'t generate a clue right now.');
      }
    } catch (err) {
      console.error('Error getting hint:', err);
      setHint('Could not fetch clue.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedOption || submitting || answered) return;

    setSubmitting(true);
    try {
      const res = await fetch(`${API_URL}/api/practice/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          question_id: question.id,
          submitted_answer: selectedOption
        })
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
        setAnswered(true);
      } else {
        setError('Submission failed. Please try again.');
      }
    } catch (err) {
      console.error('Error submitting answer:', err);
      setError('Connection error. Could not evaluate.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading && !question) {
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
        <div style={{ fontSize: '1.25rem' }}>Preparing question...</div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '4rem', background: 'var(--bg-primary)' }}>
      <div className="container" style={{ maxWidth: '800px' }}>
        {/* Back Link */}
        <Link to="/courses" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', width: 'fit-content' }}>
          <ChevronLeft size={16} /> Back to Mastery Map
        </Link>

        {concept && (
          <div style={{ marginBottom: '2rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--accent-primary)', fontWeight: 600 }}>PRACTICE SESSION</span>
            <h1 className="heading-sm" style={{ fontWeight: 700, marginTop: '0.25rem' }}>{concept.name}</h1>
          </div>
        )}

        {error && (
          <div className="glass-panel" style={{ padding: '1rem', border: '1px solid var(--error)', color: 'var(--error)', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {question && (
          <div className="glass-panel" style={{ padding: '2rem', marginBottom: '1.5rem' }}>
            {/* Question Text */}
            <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1.75rem', lineHeight: '1.5' }}>
              {question.question_text}
            </h2>

            {/* Options Form */}
            <form onSubmit={handleSubmit}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '2rem' }}>
                {question.options.map((opt) => {
                  const isSelected = selectedOption === opt;
                  const isCorrectAnswer = result?.correct_answer === opt;
                  
                  let optionBg = 'rgba(0, 0, 0, 0.02)';
                  let optionBorder = 'var(--border-color)';
                  
                  if (isSelected) {
                    optionBg = 'rgba(14, 165, 233, 0.1)';
                    optionBorder = 'var(--accent-primary)';
                  }
                  
                  if (answered) {
                    if (isCorrectAnswer) {
                      optionBg = 'rgba(16, 185, 129, 0.08)';
                      optionBorder = 'var(--success)';
                    } else if (isSelected && !result?.is_correct) {
                      optionBg = 'rgba(239, 68, 68, 0.08)';
                      optionBorder = 'var(--error)';
                    }
                  }

                  return (
                    <label 
                      key={opt}
                      style={{
                        padding: '1rem 1.25rem',
                        background: optionBg,
                        border: '1px solid',
                        borderColor: optionBorder,
                        borderRadius: 'var(--radius-md)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.75rem',
                        cursor: answered ? 'default' : 'pointer',
                        transition: 'all var(--transition-fast)'
                      }}
                    >
                      <input
                        type="radio"
                        name="option"
                        value={opt}
                        checked={isSelected}
                        onChange={() => !answered && setSelectedOption(opt)}
                        disabled={answered}
                        style={{ accentColor: 'var(--accent-primary)', width: '16px', height: '16px' }}
                      />
                      <span style={{ fontSize: '1rem', color: 'var(--text-primary)', fontWeight: 500 }}>{opt}</span>
                    </label>
                  );
                })}
              </div>

              {/* Action Buttons */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  {!answered && (
                    <Button 
                      type="button" 
                      variant="ghost" 
                      onClick={getHint}
                      style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
                    >
                      <HelpIcon size={16} /> Need a Hint?
                    </Button>
                  )}
                  <Button 
                    type="button" 
                    variant="ghost" 
                    to={`/tutor?concept=${conceptId}`}
                    style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
                  >
                    <MessageSquare size={16} /> Socratic Tutor
                  </Button>
                </div>
                
                {!answered ? (
                  <Button 
                    type="submit" 
                    variant="primary" 
                    disabled={!selectedOption || submitting}
                    style={{ padding: '0.6rem 1.75rem', fontSize: '0.95rem' }}
                  >
                    {submitting ? 'Checking...' : 'Check Answer'}
                  </Button>
                ) : (
                  <Button 
                    type="button" 
                    variant="primary" 
                    onClick={loadQuestion}
                    style={{ padding: '0.6rem 1.75rem', fontSize: '0.95rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}
                  >
                    Next Question <ArrowRight size={16} />
                  </Button>
                )}
              </div>
            </form>
          </div>
        )}

        {/* Hint Display */}
        {hint && (
          <div className="glass-panel" style={{ padding: '1.25rem 1.5rem', marginBottom: '1.5rem', background: 'rgba(14, 165, 233, 0.05)', borderLeft: '4px solid var(--accent-primary)' }}>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--accent-primary)', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <Brain size={16} /> Socratic Clue:
            </h4>
            <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>{hint}</p>
          </div>
        )}

        {/* Feedback Explanation Display */}
        {answered && result && (
          <div className="glass-panel" style={{
            padding: '1.5rem 1.75rem',
            background: result.is_correct ? 'rgba(16, 185, 129, 0.02)' : 'rgba(239, 68, 68, 0.02)',
            borderLeft: '4px solid',
            borderColor: result.is_correct ? 'var(--success)' : 'var(--error)'
          }}>
            <h3 style={{
              fontSize: '1.1rem',
              fontWeight: 700,
              color: result.is_correct ? 'var(--success)' : 'var(--error)',
              marginBottom: '0.5rem'
            }}>
              {result.is_correct ? '🎉 Brilliant! That is correct!' : '💡 Let\'s look at this together:'}
            </h3>
            
            <p style={{ fontSize: '1rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
              {result.explanation}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Practice;
