import React, { useState, useEffect } from 'react';
// CSS moved to global styles

const ADKAgentViewer = ({ sessionData }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [expandedAgents, setExpandedAgents] = useState({});

  if (!sessionData) {
    return (
      <div className="adk-viewer">
        <div className="adk-header">
          <h2>ADK Agent System</h2>
          <p>No session data available</p>
        </div>
      </div>
    );
  }

  const toggleAgentExpansion = (agentId) => {
    setExpandedAgents(prev => ({
      ...prev,
      [agentId]: !prev[agentId]
    }));
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#10b981';
    if (confidence >= 0.6) return '#f59e0b';
    return '#ef4444';
  };

  const getValidationStatusColor = (status) => {
    switch (status) {
      case 'APPROVED': return '#10b981';
      case 'NEEDS_REVISION': return '#f59e0b';
      case 'CRITICAL_ERRORS': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="adk-viewer">
      <div className="adk-header">
        <h2>ADK Agent System</h2>
        <div className="session-info">
          <span>Session: {sessionData.session_id}</span>
          <span>Query: "{sessionData.user_query}"</span>
        </div>
      </div>

      <div className="adk-tabs">
        <button 
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={activeTab === 'agents' ? 'active' : ''}
          onClick={() => setActiveTab('agents')}
        >
          Agent Responses
        </button>
        <button 
          className={activeTab === 'collaboration' ? 'active' : ''}
          onClick={() => setActiveTab('collaboration')}
        >
          Collaboration Log
        </button>
        <button 
          className={activeTab === 'final' ? 'active' : ''}
          onClick={() => setActiveTab('final')}
        >
          Final Response
        </button>
      </div>

      <div className="adk-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="stats-grid">
              <div className="stat-card">
                <h3>Total Agents</h3>
                <span className="stat-value">{sessionData.agent_responses?.length || 0}</span>
              </div>
              <div className="stat-card">
                <h3>Collaboration Steps</h3>
                <span className="stat-value">{sessionData.collaboration_log?.length || 0}</span>
              </div>
              <div className="stat-card">
                <h3>Session Time</h3>
                <span className="stat-value">{formatTimestamp(sessionData.timestamp)}</span>
              </div>
            </div>

            <div className="agent-summary">
              <h3>Agent Performance Summary</h3>
              <div className="agent-cards">
                {sessionData.agent_responses?.map((agent, index) => (
                  <div key={index} className="agent-card">
                    <div className="agent-header">
                      <h4>{agent.agent_name}</h4>
                      <span 
                        className="confidence-badge"
                        style={{ backgroundColor: getConfidenceColor(agent.confidence) }}
                      >
                        {Math.round(agent.confidence * 100)}%
                      </span>
                    </div>
                    <p className="agent-summary-text">
                      {agent.response_summary}
                    </p>
                    <small>{formatTimestamp(agent.timestamp)}</small>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'agents' && (
          <div className="agents-tab">
            <h3>Individual Agent Responses</h3>
            {sessionData.agent_responses?.map((agent, index) => (
              <div key={index} className="agent-detail-card">
                <div className="agent-detail-header">
                  <h4>{agent.agent_name}</h4>
                  <div className="agent-meta">
                    <span 
                      className="confidence-badge"
                      style={{ backgroundColor: getConfidenceColor(agent.confidence) }}
                    >
                      Confidence: {Math.round(agent.confidence * 100)}%
                    </span>
                    <span className="timestamp">{formatTimestamp(agent.timestamp)}</span>
                  </div>
                </div>
                
                <div className="agent-content">
                  <div className="input-section">
                    <h5>Input Query:</h5>
                    <p>{agent.input_query}</p>
                  </div>
                  
                  <div className="response-section">
                    <h5>Response:</h5>
                    <div className="response-content">
                      <pre>{agent.response}</pre>
                    </div>
                  </div>
                  
                  <div className="reasoning-section">
                    <h5>Reasoning:</h5>
                    <p>{agent.reasoning}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'collaboration' && (
          <div className="collaboration-tab">
            <h3>Collaboration Process</h3>
            <div className="collaboration-timeline">
              {sessionData.collaboration_log?.map((step, index) => (
                <div key={index} className="timeline-step">
                  <div className="step-header">
                    <span className="step-number">{index + 1}</span>
                    <h4>{step.step.replace('_', ' ').toUpperCase()}</h4>
                    <span className="step-time">{formatTimestamp(step.timestamp)}</span>
                  </div>
                  
                  <div className="step-details">
                    <p><strong>Agent:</strong> {step.agent_name}</p>
                    
                    {step.validation_status && (
                      <div className="validation-info">
                        <span 
                          className="validation-status"
                          style={{ backgroundColor: getValidationStatusColor(step.validation_status) }}
                        >
                          {step.validation_status}
                        </span>
                        {step.critical_errors > 0 && (
                          <span className="error-count">Critical Errors: {step.critical_errors}</span>
                        )}
                        {step.moderate_concerns > 0 && (
                          <span className="concern-count">Concerns: {step.moderate_concerns}</span>
                        )}
                      </div>
                    )}
                    
                    <div className="step-summary">
                      <p>{step.response_summary}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'final' && (
          <div className="final-tab">
            <h3>Final Synthesized Response</h3>
            <div className="final-response-card">
              <div className="response-content">
                <p>{sessionData.final_response}</p>
              </div>
              
              <div className="response-meta">
                <span className="timestamp">Generated at: {formatTimestamp(sessionData.timestamp)}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ADKAgentViewer; 