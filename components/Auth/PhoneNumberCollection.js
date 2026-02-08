import React, { useState, useEffect } from 'react';
import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '../../firebase/config';

const PhoneNumberCollection = ({ user, onComplete }) => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    checkExistingPhoneNumber();
  }, [user]);

  const checkExistingPhoneNumber = async () => {
    if (!user) return;
    
    try {
      const userRef = doc(db, 'users', user.uid);
      const userSnap = await getDoc(userRef);
      
      if (userSnap.exists() && userSnap.data().phoneNumber) {
        // Phone number already exists, proceed to dashboard
        onComplete();
      } else {
        setIsChecking(false);
      }
    } catch (error) {
      console.error('Error checking phone number:', error);
      setIsChecking(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!phoneNumber.trim()) {
      setError('Please enter a phone number');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const userRef = doc(db, 'users', user.uid);
      
      // Update user document with phone number
      await updateDoc(userRef, {
        phoneNumber: phoneNumber.trim(),
        fiAccountLinked: true,
        phoneNumberUpdatedAt: new Date()
      });

      console.log('Phone number saved successfully');
      onComplete();
    } catch (error) {
      console.error('Error saving phone number:', error);
      setError('Failed to save phone number. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (isChecking) {
    return (
      <div className="phone-collection-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Checking your account...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="phone-collection-container">
      <div className="phone-collection-card">
        <div className="phone-collection-header">
          <div className="user-info">
            <img 
              src={user.photoURL} 
              alt={user.displayName}
              className="user-avatar"
            />
            <div>
              <h2>Welcome, {user.displayName}!</h2>
              <p>Let's connect your Fi Money account</p>
            </div>
          </div>
        </div>

        <div className="phone-collection-content">
          <div className="fi-info">
            <div className="fi-logo">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect width="48" height="48" rx="24" fill="#6366F1"/>
                <path d="M12 24L20 32L36 16" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h3>Connect Your Fi Money Account</h3>
            <p>Enter the phone number linked to your Fi Money account to access your financial data and get personalized insights.</p>
          </div>

          <form onSubmit={handleSubmit} className="phone-form">
            <div className="input-group">
              <label htmlFor="phoneNumber" className="input-label">
                Phone Number (Fi Money Account)
              </label>
              <div className="phone-input-container">
                <span className="country-code">+91</span>
                <input
                  type="tel"
                  id="phoneNumber"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="Enter 10-digit number"
                  className="phone-input"
                  maxLength="10"
                  required
                />
              </div>
              <p className="input-hint">This should be the same number you use to log into Fi Money</p>
            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <button 
              type="submit" 
              className="connect-btn"
              disabled={loading}
            >
              {loading ? 'Connecting...' : 'Connect Fi Account'}
            </button>
          </form>

          <div className="security-note">
            <div className="security-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <p>Your data is encrypted and secure. We only use this to fetch your financial information from Fi Money.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhoneNumberCollection; 