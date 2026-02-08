import React, { useState, useEffect, useRef } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase/config';
import ADKAgentViewer from '../ADKAgentViewer';

const ChatInterface = ({ user, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [userPhoneNumber, setUserPhoneNumber] = useState('');
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('unknown');
  const [showADKViewer, setShowADKViewer] = useState(false);
  const [adkSessionData, setAdkSessionData] = useState(null);
  const messagesEndRef = useRef(null);

  const BACKEND_URL = 'http://localhost:8001';

  useEffect(() => {
    fetchUserPhoneNumber();
  }, [user]);

  useEffect(() => {
    if (userPhoneNumber) {
      fetchUserSessions();
    }
  }, [userPhoneNumber]);

  useEffect(() => {
    checkBackendHealth();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchUserPhoneNumber = async () => {
    if (!user) return;
    
    try {
      const userRef = doc(db, 'users', user.uid);
      const userSnap = await getDoc(userRef);
      
      if (userSnap.exists()) {
        const userData = userSnap.data();
        const phoneNumber = userData.phoneNumber;
        if (phoneNumber) {
          let formattedPhone = phoneNumber;
          if (phoneNumber.startsWith('+91')) {
            formattedPhone = phoneNumber.substring(3);
          } else if (phoneNumber.startsWith('+')) {
            formattedPhone = phoneNumber.substring(1);
          }
          setUserPhoneNumber(formattedPhone);
        }
      }
    } catch (error) {
      console.error('Error fetching user phone number:', error);
      setError('Failed to fetch user phone number');
    }
  };

  const fetchUserSessions = async () => {
    if (!userPhoneNumber) return;

    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/sessions/${encodeURIComponent(userPhoneNumber)}?active_only=true`);
      const data = await response.json();
      
      if (data.success) {
        setSessions(data.sessions || []);
        if (!currentSession && data.sessions && data.sessions.length > 0) {
          setCurrentSession(data.sessions[0]);
          fetchSessionMessages(data.sessions[0].session_id);
        }
      }
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const fetchSessionMessages = async (sessionId) => {
    if (!userPhoneNumber || !sessionId) return;

    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/sessions/${encodeURIComponent(userPhoneNumber)}/${sessionId}`);
      const data = await response.json();
      
      if (data.success && data.session.messages) {
        setMessages(data.session.messages);
      }
    } catch (error) {
      console.error('Error fetching session messages:', error);
    }
  };

  const createNewSession = async () => {
    if (!userPhoneNumber) {
      setError('Phone number not available');
      return;
    }

    try {
      const params = new URLSearchParams({
        phone_number: userPhoneNumber,
        title: `Chat Session ${new Date().toLocaleString()}`
      });

      const response = await fetch(`${BACKEND_URL}/api/v1/sessions?${params.toString()}`, {
        method: 'POST'
      });

      const data = await response.json();
      
      if (data.success) {
        setCurrentSession(data.session);
        setMessages([]);
        await fetchUserSessions();
      } else {
        setError('Failed to create session: ' + (data.detail || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error creating session:', error);
      setError('Failed to create new session: ' + error.message);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !userPhoneNumber) return;

    const messageToSend = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);
    setError('');

    // Add user message to chat
    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: messageToSend,
      message_type: 'text',
      timestamp: new Date().toISOString(),
      metadata: null
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      let endpoint = '/api/v1/chat/simple';
      
      // Check if user wants ADK analysis
      const wantsADK = messageToSend.toLowerCase().includes('adk') || 
                      messageToSend.toLowerCase().includes('agent') ||
                      messageToSend.toLowerCase().includes('detailed');
      
      if (wantsADK) {
        endpoint = '/api/v1/chat/adk';
      }
      
      const params = new URLSearchParams({
        phone_number: userPhoneNumber,
        message: messageToSend
      });
      
      if (currentSession) {
        params.append('session_id', currentSession.session_id);
      }

      const response = await fetch(`${BACKEND_URL}${endpoint}?${params.toString()}`, {
        method: 'POST'
      });

      const data = await response.json();

      // Handle simple chat response
      if (data.message) {
        // Update current session if it's a new session
        if (!currentSession && data.session_id) {
          setCurrentSession({
            session_id: data.session_id,
            phone_number: userPhoneNumber
          });
        }

        // Handle ADK response
        if (endpoint === '/api/v1/chat/adk' && data.adk_session) {
          const aiMessage = {
            id: `ai-${Date.now()}`,
            role: 'assistant',
            content: data.response?.message || 'ADK analysis completed',
            message_type: 'adk_analysis',
            timestamp: data.response?.timestamp || new Date().toISOString(),
            metadata: {
              agent_type: 'adk_coordinator',
              confidence: data.response?.confidence || 'high',
              recommendations: data.response?.recommendations || [],
              insights: data.response?.insights || [],
              next_actions: data.response?.next_actions || [],
              adk_session: data.adk_session,
              agent_interactions: data.agent_interactions,
              collaboration_log: data.collaboration_log
            }
          };

          setMessages(prev => [...prev, aiMessage]);
          
          // Store ADK session data for viewer
          setAdkSessionData(data.adk_session);
          setShowADKViewer(true);
        }
        // Handle simple chat response
        else {
          const aiMessage = {
            id: `ai-${Date.now()}`,
            role: 'assistant',
            content: data.message,
            message_type: 'financial_analysis',
            timestamp: new Date().toISOString(),
            metadata: {
              agent_type: 'financial_assistant',
              confidence: 'high',
              session_id: data.session_id,
              firestore_stored: true
            }
          };

          setMessages(prev => [...prev, aiMessage]);
        }
      } else {
        setError('Failed to get response from AI: ' + (data.detail || data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to determine if a query is complex and needs collaborative analysis
  const isComplexFinancialQuery = (query) => {
    const complexKeywords = [
      'buy house', 'purchase property', 'retirement planning', 'financial planning',
      'investment portfolio', 'wealth management', 'estate planning', 'family finance',
      'tax strategy', 'insurance needs', 'budget review', 'financial goals',
      'savings plan', 'investment strategy', 'risk assessment', 'financial advice',
      'money management', 'financial future', 'wealth building', 'financial security'
    ];
    
    const queryLower = query.toLowerCase();
    return complexKeywords.some(keyword => queryLower.includes(keyword)) || 
           query.length > 100; // Long detailed queries likely need collaborative analysis
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const checkBackendHealth = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      const data = await response.json();
      
      if (data.status === 'healthy') {
        setBackendStatus('healthy');
      } else {
        setBackendStatus('unhealthy');
      }
    } catch (error) {
      setBackendStatus('error');
    }
  };

  const deleteSession = async (sessionId, event) => {
    event.stopPropagation(); // Prevent session selection when clicking delete
    
    if (!confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/sessions/${encodeURIComponent(userPhoneNumber)}/${sessionId}`, {
        method: 'DELETE'
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Remove session from local state
        setSessions(prevSessions => prevSessions.filter(s => s.session_id !== sessionId));
        
        // If deleted session was current session, clear it
        if (currentSession?.session_id === sessionId) {
          setCurrentSession(null);
          setMessages([]);
        }
      } else {
        console.error('❌ Failed to delete session:', data);
        alert('Failed to delete session: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('❌ Error deleting session:', error);
      alert('Error deleting session: ' + error.message);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-container">
        <div className="chat-header">
          <div className="chat-header-content">
            <h3>💬 AI Financial Assistant</h3>
            <p>Ask me anything about your finances</p>
            <div className="header-status">
              {userPhoneNumber && (
                <small style={{opacity: 0.7}}>Phone: +91 {userPhoneNumber}</small>
              )}
              <div className="backend-status">
                <span className={`status-indicator ${backendStatus}`}>
                  {backendStatus === 'healthy' ? '🟢' : backendStatus === 'unhealthy' ? '🟡' : '🔴'}
                </span>
                <small style={{opacity: 0.7}}>
                  Backend: {backendStatus === 'healthy' ? 'Connected' : backendStatus === 'unhealthy' ? 'Issues' : 'Disconnected'}
                </small>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="close-chat-btn">
            ✕
          </button>
        </div>

        <div className="chat-content">
          <div className="chat-sessions">
            <div className="sessions-header">
              <h4>Sessions</h4>
              <button onClick={createNewSession} className="new-session-btn">
                + New Chat
              </button>
            </div>
            <div className="sessions-list">
              {sessions.map((session) => (
                <div
                  key={session.session_id}
                  className={`session-item ${currentSession?.session_id === session.session_id ? 'active' : ''}`}
                  onClick={() => {
                    setCurrentSession(session);
                    fetchSessionMessages(session.session_id);
                  }}
                >
                  <div className="session-info">
                    <div className="session-title">{session.title}</div>
                    <div className="session-date">
                      {new Date(session.updated_at).toLocaleDateString()}
                    </div>
                  </div>
                  <button
                    className="delete-session-btn"
                    onClick={(e) => deleteSession(session.session_id, e)}
                    title="Delete session"
                  >
                    🗑️
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="chat-main">
            <div className="messages-container">
              {messages.length === 0 ? (
                <div className="empty-chat">
                  <div className="empty-chat-icon">💬</div>
                  <h4>Start a conversation</h4>
                  <p>Ask me about your investments, savings, or any financial questions!</p>
                  {userPhoneNumber && (
                    <div style={{fontSize: '0.8rem', opacity: 0.7, marginTop: '10px'}}>
                      Phone: +91 {userPhoneNumber}
                    </div>
                  )}
                </div>
              ) : (
                <div className="messages-list">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
                    >
                      <div className="message-content">
                        <div className="message-text">{message.content}</div>
                        <div className="message-time">
                          {formatTimestamp(message.timestamp)}
                        </div>
                      </div>
                      
                      {message.metadata && message.role === 'assistant' && (
                        (message.metadata.recommendations && message.metadata.recommendations.length > 0) ||
                        (message.metadata.insights && message.metadata.insights.length > 0) ||
                        (message.metadata.next_actions && message.metadata.next_actions.length > 0) ||
                        (message.metadata.collaborative_session && message.metadata.agent_analyses)
                      ) && (
                        <div className="message-metadata">
                          {message.metadata.adk_session && (
                            <div className="adk-analysis">
                              <h5>🤖 ADK Multi-Agent Analysis</h5>
                              <div className="adk-badge">
                                <span>🚀 ADK Agent System</span>
                              </div>
                              <div className="adk-summary">
                                <p><strong>Session ID:</strong> {message.metadata.adk_session.session_id}</p>
                                <p><strong>Total Agents:</strong> {message.metadata.adk_session.agent_responses?.length || 0}</p>
                                <p><strong>Collaboration Steps:</strong> {message.metadata.adk_session.collaboration_log?.length || 0}</p>
                              </div>
                              <button 
                                onClick={() => {
                                  setAdkSessionData(message.metadata.adk_session);
                                  setShowADKViewer(true);
                                }}
                                className="view-adk-btn"
                              >
                                🔍 View Detailed Agent Analysis
                              </button>
                            </div>
                          )}
                          
                          {message.metadata.collaborative_session && (
                            <div className="collaborative-analysis">
                              <h5>🤝 Multi-Agent Analysis</h5>
                              <div className="collaborative-badge">
                                <span>✨ Collaborative Analysis</span>
                              </div>
                              {message.metadata.agent_analyses && message.metadata.agent_analyses.length > 0 && (
                                <div className="agent-analyses">
                                  <h6>Agent Insights:</h6>
                                  <ul>
                                    {message.metadata.agent_analyses.map((analysis, index) => (
                                      <li key={index}>
                                        <strong>{analysis.agent_name || `Agent ${index + 1}`}:</strong> {analysis.analysis}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {message.metadata.validation_results && message.metadata.validation_results.length > 0 && (
                                <div className="validation-results">
                                  <h6>✅ Validation Results:</h6>
                                  <ul>
                                    {message.metadata.validation_results.map((validation, index) => (
                                      <li key={index}>
                                        <strong>{validation.category}:</strong> {validation.description}
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          )}
                          
                          {message.metadata.recommendations && message.metadata.recommendations.length > 0 && (
                            <div className="recommendations">
                              <h5>💡 Recommendations:</h5>
                              <ul>
                                {message.metadata.recommendations.map((rec, index) => (
                                  <li key={index}>{rec}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          {message.metadata.insights && message.metadata.insights.length > 0 && (
                            <div className="insights">
                              <h5>🔍 Insights:</h5>
                              <ul>
                                {message.metadata.insights.map((insight, index) => (
                                  <li key={index}>{insight}</li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {message.metadata.next_actions && message.metadata.next_actions.length > 0 && (
                            <div className="next-actions">
                              <h5>🎯 Next Actions:</h5>
                              <ul>
                                {message.metadata.next_actions.map((action, index) => (
                                  <li key={index}>{action}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>

            <div className="chat-input-container">
              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}
              
              <div className="input-wrapper">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me about your finances..."
                  className="chat-input"
                  disabled={isLoading}
                  rows="1"
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="send-btn"
                >
                  {isLoading ? '⏳' : '➤'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* ADK Agent Viewer Modal */}
      {showADKViewer && adkSessionData && (
        <div className="adk-modal-overlay">
          <div className="adk-modal">
            <div className="adk-modal-header">
              <h3>ADK Agent System Analysis</h3>
              <button 
                onClick={() => setShowADKViewer(false)}
                className="close-adk-btn"
              >
                ✕
              </button>
            </div>
            <div className="adk-modal-content">
              <ADKAgentViewer sessionData={adkSessionData} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface; 