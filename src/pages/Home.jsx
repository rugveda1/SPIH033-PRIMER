import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, Target, TrendingUp, BookOpen, MessageSquare, 
  BarChart, Sparkles, Zap, ChevronDown, CheckCircle2,
  GraduationCap, Clock
} from 'lucide-react';
import Button from '../components/Button';
import FeatureCard from '../components/FeatureCard';
import './Home.css';

const fadeIn = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.2 }
  }
};

const Home = () => {
  const [activeFaq, setActiveFaq] = useState(null);

  const toggleFaq = (index) => {
    setActiveFaq(activeFaq === index ? null : index);
  };

  const faqs = [
    { question: "What is AI Tutor?", answer: "AI Tutor is an intelligent learning management system that adapts to your unique learning style, pace, and weaknesses." },
    { question: "How is AI Tutor different from a normal LMS?", answer: "Traditional LMS platforms offer static content for everyone. AI Tutor analyzes your performance in real-time and dynamically adjusts the curriculum, difficulty, and explanations." },
    { question: "How does adaptive learning work?", answer: "Our AI tracks your interactions, quiz results, and time spent on topics to build a knowledge graph, identifying exactly where you need help." },
    { question: "Can AI Tutor explain difficult concepts?", answer: "Yes, the tutor can break down complex topics into simpler analogies and step-by-step guides tailored to your current understanding." },
    { question: "Can I learn at my own pace?", answer: "Absolutely. The platform speeds up when you're mastering concepts and slows down to provide extra help when you're struggling." },
    { question: "Does AI Tutor track my progress?", answer: "Yes, you get access to a comprehensive dashboard showing your mastery levels across all subjects and topics." }
  ];

  const communityQuestions = [
    "Have you ever understood a lecture but still couldn't solve the problem?",
    "Have you ever been stuck on a concept with nobody to explain it?",
    "Does your current LMS know what you're struggling with?",
    "Do you wish your study plan adapted to your performance?"
  ];

  return (
    <div className="home-page">
      {/* 2. HERO SECTION */}
      <section className="hero-section">
        <div className="hero-background">
          <div className="gradient-sphere sphere-1"></div>
          <div className="gradient-sphere sphere-2"></div>
        </div>
        
        <div className="container hero-container">
          <motion.div 
            className="hero-content"
            initial="hidden"
            animate="visible"
            variants={staggerContainer}
          >
            <motion.div variants={fadeIn} className="hero-problem">
              <span className="problem-badge">The Problem</span>
              <h1 className="heading-xl">Learning was never <br/><span className="text-gradient">one-size-fits-all.</span></h1>
              <p className="hero-subtitle">
                Every student learns differently, but traditional learning gives everyone the same pace, content, and path. Overloaded with resources, stuck on difficult concepts, and frustrated by a rigid system.
              </p>
            </motion.div>

            <motion.div variants={fadeIn} className="hero-solution">
              <div className="solution-divider">
                <div className="line"></div>
                <Sparkles className="sparkle-icon" size={24} />
                <div className="line"></div>
              </div>
              <h2 className="heading-md">What if your learning platform learned about <span className="text-gradient">YOU?</span></h2>
              
              <div className="hero-actions">
                <Button variant="primary" to="/signup">Start Learning</Button>
                <Button variant="secondary" to="#how-it-works">See How It Works</Button>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* 3. STORYTELLING SECTION */}
      <section className="section story-section" id="story">
        <div className="container">
          <motion.div 
            className="story-container"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
          >
            <div className="story-traditional">
              <h3 className="story-title text-muted">The Old Way</h3>
              <div className="story-nodes">
                <div className="node disabled">Start Course</div>
                <div className="node-connector"></div>
                <div className="node disabled">Get Stuck</div>
                <div className="node-connector"></div>
                <div className="node danger">Fall Behind</div>
              </div>
            </div>

            <div className="story-transformation">
              <h2 className="heading-lg">AI Tutor <span className="text-gradient">changes the journey.</span></h2>
            </div>

            <div className="story-modern">
              <div className="pipeline">
                {['Understand', 'Identify', 'Adapt', 'Teach', 'Assess', 'Improve'].map((step, idx) => (
                  <motion.div key={step} variants={fadeIn} className="pipeline-step glass-panel">
                    <span className="step-number">0{idx + 1}</span>
                    <h4>{step}</h4>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* 4. WHY CHOOSE AI TUTOR */}
      <section className="section why-section">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="heading-lg">Why should your learning platform <span className="text-gradient">adapt to you?</span></h2>
            <p className="text-lg mt-4">Experience the unfair advantage of personalized education.</p>
          </div>
          
          <div className="grid feature-grid mt-12">
            <FeatureCard 
              icon={Target} title="Personalized Learning" 
              description="Content that matches your exact knowledge level and learning style." 
            />
            <FeatureCard 
              icon={TrendingUp} title="Adaptive Difficulty" 
              description="Questions get harder as you improve, and easier when you need a break." 
            />
            <FeatureCard 
              icon={Brain} title="Weak-topic Detection" 
              description="Automatically identifies knowledge gaps before they become problems." 
            />
            <FeatureCard 
              icon={MessageSquare} title="AI Tutoring" 
              description="24/7 access to an infinitely patient tutor that explains concepts clearly." 
            />
          </div>
        </div>
      </section>

      {/* 5. HOW IT WORKS */}
      <section className="section how-it-works-section" id="how-it-works">
        <div className="container">
          <div className="section-header">
            <h2 className="heading-lg">The Intelligence Pipeline</h2>
          </div>
          
          <div className="pipeline-visual mt-12">
            <div className="pipeline-track">
              <div className="pipeline-item">
                <div className="item-icon"><GraduationCap /></div>
                <div className="item-content">
                  <h4>Student Activity</h4>
                  <p>You interact with course materials</p>
                </div>
              </div>
              <div className="pipeline-arrow"><ChevronDown /></div>
              <div className="pipeline-item highlight">
                <div className="item-icon"><Brain /></div>
                <div className="item-content">
                  <h4>AI Understands</h4>
                  <p>Analyzes strengths & weaknesses</p>
                </div>
              </div>
              <div className="pipeline-arrow"><ChevronDown /></div>
              <div className="pipeline-item">
                <div className="item-icon"><Zap /></div>
                <div className="item-content">
                  <h4>Adapts Learning</h4>
                  <p>Generates custom questions & paths</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. AI TUTOR EXPERIENCE */}
      <section className="section experience-section">
        <div className="container">
          <div className="experience-layout">
            <div className="experience-content">
              <h2 className="heading-lg">A tutor that actually <span className="text-gradient">listens.</span></h2>
              <p className="text-lg mt-4 mb-8">
                Stop reading static textbooks. Engage in a dynamic dialogue where the AI breaks down complex concepts step-by-step until you truly understand.
              </p>
              <ul className="experience-list">
                <li><CheckCircle2 className="text-success" /> Concept explanations</li>
                <li><CheckCircle2 className="text-success" /> Contextual examples</li>
                <li><CheckCircle2 className="text-success" /> Socratic questioning</li>
                <li><CheckCircle2 className="text-success" /> Instant feedback</li>
              </ul>
            </div>
            
            <div className="experience-mockup glass-panel">
              <div className="mockup-header">
                <div className="mac-dots"><span></span><span></span><span></span></div>
                <span className="mockup-title">AI Tutor Session</span>
              </div>
              <div className="chat-interface">
                <div className="message student">
                  <p>I don't understand recursion.</p>
                </div>
                <div className="message tutor">
                  <p>Let's start with the basic idea! Imagine you are standing in a line of people and want to know what position you are in, but you can only see the person directly in front of you.</p>
                  <p>What's the easiest way to find out your position?</p>
                </div>
                <div className="message student">
                  <p>I could ask the person in front of me what their position is, and add 1?</p>
                </div>
                <div className="message tutor">
                  <p>Exactly! 🎉 That's recursion. You broke a big problem (finding your position) into a smaller version of the same problem (finding the position of the person in front of you).</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 8. LMS SERVICE */}
      <section className="section lms-section" id="lms">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="heading-lg">An LMS that <span className="text-gradient">learns with you.</span></h2>
            <p className="text-lg mt-4">AI Tutor is not merely a chatbot. It's a complete architectural rethinking of the Learning Management System.</p>
          </div>
          
          <div className="dashboard-mockup mt-12 glass-panel">
            <div className="sidebar">
              <div className="nav-item active"><BookOpen size={18}/> Courses</div>
              <div className="nav-item"><BarChart size={18}/> Progress</div>
              <div className="nav-item"><Target size={18}/> Weak Topics</div>
            </div>
            <div className="main-area">
              <div className="top-bar">
                <h3>Machine Learning 101</h3>
                <div className="progress-pill">78% Mastery</div>
              </div>
              <div className="content-grid">
                <div className="card">
                  <h4>Up Next for You</h4>
                  <p className="text-sm text-muted">Based on your recent struggles with Neural Networks</p>
                  <Button variant="primary" className="mt-4 w-full">Start Custom Lesson</Button>
                </div>
                <div className="card">
                  <h4>Knowledge Graph</h4>
                  <div className="fake-graph"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 9. VOICE OF THE COMMUNITY */}
      <section className="section community-section" id="community">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="heading-lg">Tell us how you <span className="text-gradient">learn.</span></h2>
          </div>
          
          <div className="poll-grid mt-12">
            {communityQuestions.map((q, i) => (
              <div key={i} className="poll-card glass-panel">
                <p className="poll-question">"{q}"</p>
                <div className="poll-actions mt-6">
                  <button className="poll-btn yes">Yes, often</button>
                  <button className="poll-btn no">No</button>
                </div>
              </div>
            ))}
          </div>
          
          <div className="community-statement text-center mt-12">
            <h3 className="heading-md">We're building AI Tutor around what learners actually need.</h3>
            <div className="testimonial-placeholders mt-8">
              {[1,2,3].map(i => (
                <div key={i} className="t-placeholder glass-panel">
                  <div className="t-header">
                    <div className="t-avatar"></div>
                    <div className="t-info">
                      <div className="t-name"></div>
                      <div className="t-role"></div>
                    </div>
                  </div>
                  <div className="t-body"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* 10. PRODUCT VISION */}
      <section className="section vision-section">
        <div className="container">
          <div className="vision-grid">
            <div>
              <h2 className="heading-lg">The Vision</h2>
              <p className="text-lg mt-4">We are actively building the future of personalized education.</p>
            </div>
            <div className="roadmap glass-panel">
              <div className="roadmap-col">
                <h4 className="text-accent">Available Now</h4>
                <ul>
                  <li><CheckCircle2 size={16}/> Adaptive Learning</li>
                  <li><CheckCircle2 size={16}/> AI Tutoring Chat</li>
                  <li><CheckCircle2 size={16}/> Progress Tracking</li>
                </ul>
              </div>
              <div className="roadmap-col">
                <h4 className="text-muted">Coming Soon</h4>
                <ul className="text-muted">
                  <li><Clock size={16}/> Voice Tutoring</li>
                  <li><Clock size={16}/> Mobile App</li>
                  <li><Clock size={16}/> Multimodal Learning</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 11. FAQ */}
      <section className="section faq-section" id="faq">
        <div className="container max-w-3xl">
          <div className="section-header text-center">
            <h2 className="heading-lg">Frequently Asked <span className="text-gradient">Questions</span></h2>
          </div>
          
          <div className="faq-accordion mt-12">
            {faqs.map((faq, index) => (
              <div 
                key={index} 
                className={`faq-item glass-panel ${activeFaq === index ? 'active' : ''}`}
                onClick={() => toggleFaq(index)}
              >
                <div className="faq-question">
                  <h3>{faq.question}</h3>
                  <ChevronDown className="faq-icon" />
                </div>
                <AnimatePresence>
                  {activeFaq === index && (
                    <motion.div 
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="faq-answer"
                    >
                      <p>{faq.answer}</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 12. FINAL CTA */}
      <section className="section final-cta-section">
        <div className="hero-background">
          <div className="gradient-sphere sphere-3"></div>
        </div>
        <div className="container text-center">
          <h2 className="heading-xl">Your learning journey shouldn't look like <span className="text-gradient">everyone else's.</span></h2>
          <p className="text-lg mt-6 max-w-2xl mx-auto">
            Start with where you are. Learn at your pace. Let AI Tutor adapt with you.
          </p>
          <div className="mt-10">
            <Button variant="primary" to="/signup" className="btn-large">Start Your Learning Journey</Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
