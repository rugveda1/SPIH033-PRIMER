import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Send, ChevronLeft, HelpCircle, AlertCircle } from 'lucide-react';

const Tutor = () => {
  const { token, user, API_URL } = useAuth();
  const [searchParams] = useSearchParams();
  const queryConceptId = Number(searchParams.get('concept'));

  const [concepts, setConcepts] = useState([]);
  const [selectedConceptId, setSelectedConceptId] = useState(queryConceptId || '');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  
  const messagesEndRef = useRef(null);

  // Load class topics list on mount
  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const res = await fetch(`${API_URL}/api/concepts?class_level=${user.class_level}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setConcepts(data);
          // Default to first concept if none provided in query
          if (!queryConceptId && data.length > 0) {
            setSelectedConceptId(data[0].id);
          }
        }
      } catch (err) {
        console.error('Error fetching chat topics:', err);
      }
    };
    fetchTopics();
  }, [user.class_level, token, API_URL, queryConceptId]);

  // Load chat session messages when concept selection changes
  useEffect(() => {
    if (!selectedConceptId) return;

    const fetchSessionMessages = async () => {
      setLoading(true);
      try {
        // Fetch sessions
        const sessionRes = await fetch(`${API_URL}/api/chat/sessions`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (sessionRes.ok) {
          const sessions = await sessionRes.json();
          // Find session matching selected concept
          const match = sessions.find(s => s.concept_id === Number(selectedConceptId));
          if (match) {
            const msgRes = await fetch(`${API_URL}/api/chat/sessions/${match.id}/messages`, {
              headers: { 'Authorization': `Bearer ${token}` }
            });
            if (msgRes.ok) {
              const msgData = await msgRes.json();
              setMessages(msgData);
              return;
            }
          }
        }
        
        // If no prior session found, initialize default greeting
        const activeConcept = concepts.find(c => c.id === Number(selectedConceptId));
        const conceptName = activeConcept ? activeConcept.name : 'mathematics';
        setMessages([
          {
            id: 0,
            role: 'assistant',
            content: `Hi there, ${user.name}! I am your Socratic Math Tutor. Let's learn about "${conceptName}" today! 🌟 Ask me any question, or we can look at some examples together.`,
            timestamp: new Date().toISOString()
          }
        ]);
      } catch (err) {
        console.error('Error fetching chat history:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSessionMessages();
  }, [selectedConceptId, concepts, token, API_URL, user]);

  // Scroll to bottom on message updates
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;

    const userText = input;
    setInput('');
    setSending(true);

    // Append user message immediately
    const tempUserMsg = {
      id: Date.now(),
      role: 'user',
      content: userText,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: userText,
          concept_id: Number(selectedConceptId)
        })
      });

      if (res.ok) {
        const responseData = await res.json();
        setMessages(prev => [...prev, responseData]);
      } else {
        // Appends a friendly system failure text
        setMessages(prev => [...prev, {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Oops! I had a little hiccup. Let\'s try saying that again! 😊',
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (err) {
      console.error('Chat error:', err);
    } finally {
      setSending(false);
    }
  };

  const getSocraticHint = async () => {
    setSending(true);
    try {
      const res = await fetch(`${API_URL}/api/chat/hint`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          concept_id: Number(selectedConceptId)
        })
      });

      if (res.ok) {
        const data = await res.json();
        // Insert Grok's hint as an assistant message
        setMessages(prev => [...prev, {
          id: Date.now(),
          role: 'assistant',
          content: `💡 Clue: ${data.hint}`,
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (err) {
      console.error('Error getting Socratic hint:', err);
    } finally {
      setSending(false);
    }
  };

  const getMistakeExplanation = async () => {
    setSending(true);
    try {
      const res = await fetch(`${API_URL}/api/chat/explain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          concept_id: Number(selectedConceptId)
        })
      });

      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [...prev, {
          id: Date.now(),
          role: 'assistant',
          content: `🔍 Socratic Breakdown: ${data.explanation}`,
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (err) {
      console.error('Error getting mistake explanation:', err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', paddingTop: '100px', paddingBottom: '2rem', background: 'var(--bg-primary)', display: 'flex', flexDirection: 'column' }}>
      <div className="container" style={{ maxWidth: '900px', display: 'flex', flexDirection: 'column', flex: 1 }}>
        
        {/* Header toolbar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <Link to="/dashboard" style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--text-secondary)' }}>
            <ChevronLeft size={16} /> Back to Dashboard
          </Link>
          
          {/* Concept Select dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Topic:</span>
            <select
              value={selectedConceptId}
              onChange={(e) => setSelectedConceptId(e.target.value)}
              style={{
                padding: '0.5rem 1rem',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-primary)',
                outline: 'none',
                fontSize: '0.95rem',
                cursor: 'pointer'
              }}
            >
              {concepts.map(c => (
                <option key={c.id} value={c.id} style={{ background: '#18181b' }}>{c.name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Chat Conversation Box */}
        <div className="glass-panel" style={{
          flex: 1,
          minHeight: '450px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          overflow: 'hidden',
          marginBottom: '1rem'
        }}>
          {/* Messages Log */}
          <div style={{
            flex: 1,
            padding: '2rem',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '1.25rem',
            maxHeight: '500px'
          }}>
            {loading ? (
              <div style={{ textAlign: 'center', color: 'var(--text-muted)', margin: 'auto' }}>
                Restoring tutor session...
              </div>
            ) : (
              messages.map((msg) => {
                const isUser = msg.role === 'user';
                return (
                  <div
                    key={msg.id}
                    style={{
                      display: 'flex',
                      justifyContent: isUser ? 'flex-end' : 'flex-start',
                      alignItems: 'flex-start',
                      gap: '0.75rem'
                    }}
                  >
                    {!isUser && (
                      <div style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '50%',
                        background: 'var(--accent-gradient)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#f8fafc',
                        fontSize: '0.85rem',
                        fontWeight: 700,
                        flexShrink: 0
                      }}>
                        T
                      </div>
                    )}
                    <div style={{
                      maxWidth: '75%',
                      padding: '0.85rem 1.25rem',
                      borderRadius: '16px',
                      borderTopRightRadius: isUser ? '4px' : '16px',
                      borderTopLeftRadius: isUser ? '16px' : '4px',
                      background: isUser ? 'var(--accent-primary)' : 'var(--bg-tertiary)',
                      border: isUser ? 'none' : '1px solid var(--border-color)',
                      color: isUser ? '#ffffff' : 'var(--text-primary)',
                      fontSize: '0.975rem',
                      lineHeight: '1.45',
                      whiteSpace: 'pre-line'
                    }}>
                      {msg.content}
                    </div>
                  </div>
                );
              })
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Socratic Helper Buttons Bar */}
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            padding: '0.5rem 1.5rem',
            background: 'rgba(0,0,0,0.2)',
            borderTop: '1px solid var(--border-color)',
            flexWrap: 'wrap'
          }}>
            <button
              onClick={getSocraticHint}
              disabled={sending}
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--accent-primary)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
                padding: '4px 8px'
              }}
            >
              <HelpCircle size={15} /> Stuck? Get a Clue
            </button>
            <button
              onClick={getMistakeExplanation}
              disabled={sending}
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--warning)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
                padding: '4px 8px'
              }}
            >
              <AlertCircle size={15} /> Explain My Last Mistake
            </button>
          </div>

          {/* Form message input */}
          <form onSubmit={handleSend} style={{
            display: 'flex',
            padding: '1.25rem 1.5rem',
            background: 'rgba(0,0,0,0.15)',
            borderTop: '1px solid var(--border-color)',
            alignItems: 'center',
            gap: '1rem'
          }}>
            <input
              type="text"
              placeholder="Ask me how to solve a problem..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={sending}
              style={{
                flex: 1,
                padding: '0.85rem 1.25rem',
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-primary)',
                outline: 'none',
                fontSize: '1rem'
              }}
            />
            <button
              type="submit"
              disabled={!input.trim() || sending}
              style={{
                width: '45px',
                height: '45px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--accent-gradient)',
                border: 'none',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#f8fafc',
                cursor: 'pointer',
                transition: 'opacity var(--transition-fast)'
              }}
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Tutor;
