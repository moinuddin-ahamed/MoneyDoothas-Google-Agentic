import React, { useState } from 'react';
import { signInWithPopup, signOut } from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { auth, googleProvider, db } from '../../firebase/config';

const GoogleSignIn = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const signInWithGoogle = async () => {
    setLoading(true);
    setError('');
    
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;
      
      // Create or update user document in Firestore
      await createOrUpdateUserProfile(user);
      
      setUser(user);
      console.log('Successfully signed in:', user.displayName);
    } catch (error) {
      console.error('Sign-in error:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const signOutUser = async () => {
    try {
      await signOut(auth);
      setUser(null);
      console.log('Successfully signed out');
    } catch (error) {
      console.error('Sign-out error:', error);
      setError(error.message);
    }
  };

  const createOrUpdateUserProfile = async (user) => {
    const userRef = doc(db, 'users', user.uid);
    const userSnap = await getDoc(userRef);

    if (!userSnap.exists()) {
      // Create new user profile
      await setDoc(userRef, {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
        createdAt: new Date(),
        lastSignIn: new Date(),
        preferences: {
          currency: 'USD',
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
          notifications: true
        }
      });
      console.log('New user profile created');
    } else {
      // Update existing user's last sign-in
      await setDoc(userRef, {
        lastSignIn: new Date()
      }, { merge: true });
      console.log('User profile updated');
    }
  };

  // Listen for auth state changes
  React.useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user);
    });

    return () => unsubscribe();
  }, []);

  return (
    <div className="auth-container">
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      {!user ? (
        <button 
          onClick={signInWithGoogle}
          disabled={loading}
          className="google-signin-btn"
        >
          {loading ? 'Signing in...' : 'Sign in with Google'}
        </button>
      ) : (
        <div className="user-profile">
          <img 
            src={user.photoURL} 
            alt={user.displayName}
            className="user-avatar"
          />
          <div className="user-info">
            <h3>Welcome, {user.displayName}!</h3>
            <p>{user.email}</p>
          </div>
          <button 
            onClick={signOutUser}
            className="signout-btn"
          >
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
};

export default GoogleSignIn; 