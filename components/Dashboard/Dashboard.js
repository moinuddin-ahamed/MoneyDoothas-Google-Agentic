import React, { useState, useEffect } from 'react';
import GoogleSignIn from '../Auth/GoogleSignIn';
import ChatInterface from '../Chat/ChatInterface';
import { doc, getDoc, updateDoc } from 'firebase/firestore';
import { db } from '../../firebase/config';

const Dashboard = ({ user }) => {
  const [userPhoneNumber, setUserPhoneNumber] = useState('');
  const [showPhoneUpdate, setShowPhoneUpdate] = useState(false);
  const [newPhoneNumber, setNewPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showJsonModal, setShowJsonModal] = useState(false);
  const [jsonData, setJsonData] = useState(null);
  const [fetchingData, setFetchingData] = useState(false);
  const [currentFunction, setCurrentFunction] = useState('');
  const [showChat, setShowChat] = useState(false);
  const [financialData, setFinancialData] = useState({
    netWorth: null,
    creditScore: null,
    investments: null,
    transactions: null
  });

  useEffect(() => {
    fetchUserPhoneNumber();
  }, [user]);

  const fetchUserPhoneNumber = async () => {
    if (!user) return;
    
    try {
      const userRef = doc(db, 'users', user.uid);
      const userSnap = await getDoc(userRef);
      
      if (userSnap.exists()) {
        const userData = userSnap.data();
        setUserPhoneNumber(userData.phoneNumber || '');
      }
    } catch (error) {
      console.error('Error fetching user phone number:', error);
    }
  };

  const handlePhoneUpdate = async (e) => {
    e.preventDefault();
    
    if (!newPhoneNumber.trim()) {
      setError('Please enter a phone number');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const userRef = doc(db, 'users', user.uid);
      
      await updateDoc(userRef, {
        phoneNumber: newPhoneNumber.trim(),
        phoneNumberUpdatedAt: new Date()
      });

      setUserPhoneNumber(newPhoneNumber.trim());
      setNewPhoneNumber('');
      setShowPhoneUpdate(false);
    } catch (error) {
      console.error('Error updating phone number:', error);
      setError('Failed to update phone number. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchFinancialData = async (dataType) => {
    if (!userPhoneNumber) {
      alert('Please set your Fi account phone number first');
      return;
    }

    setFetchingData(true);
    setCurrentFunction(dataType);
    setError('');

    try {
      const baseUrl = 'https://us-central1-hackathon-62355.cloudfunctions.net';
      const functionMap = {
        'netWorth': 'getNetWorth',
        'creditReport': 'getCreditReport',
        'epfDetails': 'getEPFDetails',
        'mfTransactions': 'getMFTransactions',
        'bankTransactions': 'getBankTransactions'
      };
      
      const url = `${baseUrl}/${functionMap[dataType]}`;
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phoneNumber: userPhoneNumber
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setFinancialData(prev => ({
        ...prev,
        [dataType]: data
      }));
      setJsonData(data);
      setShowJsonModal(true);
    } catch (error) {
      console.error(`Error fetching ${dataType}:`, error);
      setError(`Failed to fetch ${dataType}: ${error.message}`);
    } finally {
      setFetchingData(false);
    }
  };

  const closeJsonModal = () => {
    setShowJsonModal(false);
    setJsonData(null);
    setCurrentFunction('');
  };

  const formatJsonData = (data) => {
    try {
      return JSON.stringify(data, null, 2);
    } catch (error) {
      return 'Invalid JSON data';
    }
  };

  const getDataStatus = (dataType) => {
    return financialData[dataType] ? '✅ Loaded' : ' Available';
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="user-welcome">
          <img 
            src={user.photoURL} 
            alt={user.displayName}
            className="user-avatar"
          />
          <div>
            <h2>Welcome back, {user.displayName}!</h2>
            <p>Your AI-powered financial companion</p>
            {userPhoneNumber && (
              <div className="phone-info">
                <span className="phone-label">Fi Account:</span>
                <span className="phone-number">+91 {userPhoneNumber}</span>
                <button 
                  onClick={() => setShowPhoneUpdate(true)}
                  className="update-phone-btn"
                >
                  Update
                </button>
              </div>
            )}
          </div>
        </div>
        <GoogleSignIn />
      </div>

      {showPhoneUpdate && (
        <div className="phone-update-modal">
          <div className="phone-update-card">
            <h3>Update Fi Account Phone Number</h3>
            <form onSubmit={handlePhoneUpdate}>
              <div className="input-group">
                <label htmlFor="newPhoneNumber" className="input-label">
                  New Phone Number
                </label>
                <div className="phone-input-container">
                  <span className="country-code">+91</span>
                  <input
                    type="tel"
                    id="newPhoneNumber"
                    value={newPhoneNumber}
                    onChange={(e) => setNewPhoneNumber(e.target.value)}
                    placeholder="Enter 10-digit number"
                    className="phone-input"
                    maxLength="10"
                    required
                  />
                </div>
              </div>

              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}

              <div className="modal-actions">
                <button 
                  type="button"
                  onClick={() => {
                    setShowPhoneUpdate(false);
                    setNewPhoneNumber('');
                    setError('');
                  }}
                  className="cancel-btn"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="update-btn"
                  disabled={loading}
                >
                  {loading ? 'Updating...' : 'Update Phone'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="dashboard-content">
        <div className="financial-overview">
          <h3> Financial Overview</h3>
          <p>Connect your Fi Money account to get personalized insights</p>
          
          <div className="financial-cards">
            <div className="financial-card">
              <div className="card-icon">📊</div>
              <h4>Net Worth</h4>
              <p>Track your total assets and liabilities</p>
              <button 
                onClick={() => fetchFinancialData('netWorth')}
                disabled={fetchingData || !userPhoneNumber}
                className="data-btn"
              >
                {fetchingData && currentFunction === 'netWorth' ? 'Loading...' : getDataStatus('netWorth')}
              </button>
            </div>

            <div className="financial-card">
              <div className="card-icon">💳</div>
              <h4>Credit Report</h4>
              <p>Monitor your credit score and history</p>
              <button 
                onClick={() => fetchFinancialData('creditReport')}
                disabled={fetchingData || !userPhoneNumber}
                className="data-btn"
              >
                {fetchingData && currentFunction === 'creditReport' ? 'Loading...' : getDataStatus('creditReport')}
              </button>
            </div>

            <div className="financial-card">
              <div className="card-icon">🏦</div>
              <h4>EPF Details</h4>
              <p>View your employee provident fund</p>
              <button 
                onClick={() => fetchFinancialData('epfDetails')}
                disabled={fetchingData || !userPhoneNumber}
                className="data-btn"
              >
                {fetchingData && currentFunction === 'epfDetails' ? 'Loading...' : getDataStatus('epfDetails')}
              </button>
            </div>

            <div className="financial-card">
              <div className="card-icon">📈</div>
              <h4>Mutual Funds</h4>
              <p>Track your investment portfolio</p>
              <button 
                onClick={() => fetchFinancialData('mfTransactions')}
                disabled={fetchingData || !userPhoneNumber}
                className="data-btn"
              >
                {fetchingData && currentFunction === 'mfTransactions' ? 'Loading...' : getDataStatus('mfTransactions')}
              </button>
            </div>

            <div className="financial-card">
              <div className="card-icon">🏛️</div>
              <h4>Bank Transactions</h4>
              <p>Analyze your spending patterns</p>
              <button 
                onClick={() => fetchFinancialData('bankTransactions')}
                disabled={fetchingData || !userPhoneNumber}
                className="data-btn"
              >
                {fetchingData && currentFunction === 'bankTransactions' ? 'Loading...' : getDataStatus('bankTransactions')}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>

        <div className="ai-features">
          <h3>🤖 AI-Powered Features</h3>
          <p>Get intelligent insights and personalized financial advice</p>
          
          <div className="feature-cards">
            <div className="feature-card primary">
              <div className="feature-icon">💬</div>
              <h4>AI Financial Assistant</h4>
              <p>Ask questions about your finances in natural language and get personalized advice</p>
              <button 
                className="feature-btn primary"
                onClick={() => setShowChat(true)}
              >
                Start Chat
              </button>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h4>Smart Insights</h4>
              <p>AI-powered analysis of your spending patterns and financial health</p>
              <button className="feature-btn">Coming Soon</button>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h4>Goal Tracking</h4>
              <p>Set and track your financial goals with AI recommendations</p>
              <button className="feature-btn">Coming Soon</button>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📈</div>
              <h4>Wealth Trends</h4>
              <p>Track your net worth over time with predictive insights</p>
              <button className="feature-btn">Coming Soon</button>
            </div>
          </div>
        </div>
      </div>

      {/* JSON Data Modal */}
      {showJsonModal && (
        <div className="json-modal">
          <div className="json-modal-content">
            <div className="json-modal-header">
              <h3>{currentFunction} Data</h3>
              <button onClick={closeJsonModal} className="close-btn">
                ✕
              </button>
            </div>
            <div className="json-content">
              <pre className="json-display">
                {formatJsonData(jsonData)}
              </pre>
            </div>
          </div>
        </div>
      )}

      {/* Chat Interface */}
      {showChat && (
        <ChatInterface 
          user={user} 
          onClose={() => setShowChat(false)} 
        />
      )}
    </div>
  );
};

export default Dashboard; 