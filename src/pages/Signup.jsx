import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { BrainCircuit, ChevronRight, ChevronLeft } from 'lucide-react';
import Button from '../components/Button';
import './Auth.css';

const questions = [
  {
    id: 'current_learning',
    title: "What are you currently learning?",
    type: 'text',
    placeholder: "e.g., Computer Science, Data Science, High School Math"
  },
  {
    id: 'subjects',
    title: "What subjects do you want help with?",
    type: 'tags',
    options: ["Mathematics", "Programming", "Physics", "Chemistry", "Biology", "Languages", "History", "Other"]
  },
  {
    id: 'level',
    title: "What's your current level?",
    type: 'radio',
    options: ["Beginner", "Intermediate", "Advanced"]
  },
  {
    id: 'goal',
    title: "What is your learning goal?",
    type: 'text',
    placeholder: "e.g., Pass my exams, Learn a new skill, Get a job"
  },
  {
    id: 'time',
    title: "How much time can you study each day?",
    type: 'radio',
    options: ["Less than 1 hour", "1-2 hours", "3-4 hours", "5+ hours"]
  },
  {
    id: 'difficult_topics',
    title: "Which topics are difficult for you?",
    type: 'text',
    placeholder: "e.g., Calculus, Pointers in C++, Cell biology"
  },
  {
    id: 'preference',
    title: "How do you prefer to learn?",
    type: 'radio',
    options: ["Visual (Diagrams, videos)", "Text-based (Reading)", "Interactive (Quizzes, coding)", "Audio (Listening)"]
  }
];

const Signup = () => {
  const [step, setStep] = useState(-1); // -1 is the initial account creation step

  const nextStep = () => setStep(prev => Math.min(prev + 1, questions.length));
  const prevStep = () => setStep(prev => Math.max(prev - 1, -1));

  const renderInitialStep = () => (
    <>
      <div className="auth-header text-center">
        <Link to="/" className="auth-logo">
          <BrainCircuit className="logo-icon" size={32} />
        </Link>
        <h2 className="heading-md mt-4">Create your account</h2>
        <p className="text-muted mt-2">Start your personalized learning journey</p>
      </div>
      
      <form className="auth-form mt-8">
        <div className="form-group">
          <label>Full Name</label>
          <input type="text" placeholder="John Doe" className="basic-input" />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input type="email" placeholder="you@example.com" className="basic-input" />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" placeholder="••••••••" className="basic-input" />
        </div>
        
        <Button variant="primary" className="w-full mt-6" type="button" onClick={nextStep}>
          Create Account
        </Button>
      </form>
      
      <div className="auth-footer text-center mt-8">
        <p className="text-muted">
          Already have an account? <Link to="/login" className="text-accent">Log in</Link>
        </p>
      </div>
    </>
  );

  const renderOnboardingStep = () => {
    if (step >= questions.length) {
      return (
        <div className="text-center py-8">
          <div className="success-icon mb-6">
            <BrainCircuit size={48} className="text-accent mx-auto" />
          </div>
          <h2 className="heading-md mb-4">You're all set!</h2>
          <p className="text-muted mb-8">We've personalized your learning environment based on your answers.</p>
          <Button variant="primary" to="/dashboard" className="w-full">Go to Dashboard</Button>
        </div>
      );
    }

    const currentQ = questions[step];

    return (
      <div className="onboarding-step">
        <div className="progress-bar-container mb-8">
          <div className="progress-bar" style={{ width: `${((step + 1) / questions.length) * 100}%` }}></div>
        </div>
        
        <button className="back-btn" onClick={prevStep}><ChevronLeft size={20} /> Back</button>
        
        <h2 className="heading-sm mt-6 mb-8">{currentQ.title}</h2>
        
        <div className="question-input">
          {currentQ.type === 'text' && (
            <input type="text" placeholder={currentQ.placeholder} className="basic-input lg-input" />
          )}
          
          {currentQ.type === 'radio' && (
            <div className="radio-group">
              {currentQ.options.map(opt => (
                <label key={opt} className="radio-label">
                  <input type="radio" name={currentQ.id} />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
          )}
          
          {currentQ.type === 'tags' && (
            <div className="tags-group">
              {currentQ.options.map(opt => (
                <label key={opt} className="tag-label">
                  <input type="checkbox" name={currentQ.id} />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
          )}
        </div>
        
        <div className="mt-10 flex justify-end">
          <Button variant="primary" onClick={nextStep}>
            Next <ChevronRight size={18} />
          </Button>
        </div>
      </div>
    );
  };

  return (
    <div className="auth-page">
      <div className="auth-container glass-panel">
        {step === -1 ? renderInitialStep() : renderOnboardingStep()}
      </div>
    </div>
  );
};

export default Signup;
