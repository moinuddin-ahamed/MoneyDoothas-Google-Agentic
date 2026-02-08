import { useAuth } from '../components/Auth/AuthContext';
import GoogleSignIn from '../components/Auth/GoogleSignIn';
import PhoneNumberCollection from '../components/Auth/PhoneNumberCollection';
import Dashboard from '../components/Dashboard/Dashboard';
import { useState, useEffect } from 'react';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../firebase/config';

export default function Home() {
  const { user, isAuthenticated } = useAuth();
  const [hasPhoneNumber, setHasPhoneNumber] = useState(false);
  const [isCheckingPhone, setIsCheckingPhone] = useState(false);

  useEffect(() => {
    if (isAuthenticated && user) {
      checkPhoneNumber();
    }
  }, [isAuthenticated, user]);

  const checkPhoneNumber = async () => {
    if (!user) return;
    
    setIsCheckingPhone(true);
    try {
      const userRef = doc(db, 'users', user.uid);
      const userSnap = await getDoc(userRef);
      
      if (userSnap.exists() && userSnap.data().phoneNumber) {
        setHasPhoneNumber(true);
      } else {
        setHasPhoneNumber(false);
      }
    } catch (error) {
      console.error('Error checking phone number:', error);
      setHasPhoneNumber(false);
    } finally {
      setIsCheckingPhone(false);
    }
  };

  const handlePhoneNumberComplete = () => {
    setHasPhoneNumber(true);
  };

  if (!isAuthenticated) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>Financial AI Assistant</h1>
          <p>Your personal financial advisor powered by AI</p>
        </header>

        <main className="app-main">
          <div className="auth-section">
            <div className="auth-card">
              <h2>Welcome to Your Financial AI Assistant</h2>
              <p>Sign in with Google to get started with personalized financial insights</p>
              <GoogleSignIn />
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (isCheckingPhone) {
    return (
      <div className="app">
        <div className="loading-container">
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Setting up your account...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!hasPhoneNumber) {
    return (
      <div className="app">
        <PhoneNumberCollection user={user} onComplete={handlePhoneNumberComplete} />
      </div>
    );
  }

  return (
    <div className="app">
      <Dashboard user={user} />
    </div>
  );
} 