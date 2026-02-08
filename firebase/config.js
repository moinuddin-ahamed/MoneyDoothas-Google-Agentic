import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getAnalytics } from 'firebase/analytics';

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyCylUOAa5xcZCXv0hFrSBfHcNXiiq2PH8E",
  authDomain: "hackathon-62355.firebaseapp.com",
  projectId: "hackathon-62355",
  storageBucket: "hackathon-62355.firebasestorage.app",
  messagingSenderId: "267132178774",
  appId: "1:267132178774:web:06fba548bb940c1df4c6f7",
  measurementId: "G-C8QVMNX7NL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Auth
export const auth = getAuth(app);

// Initialize Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

// Initialize Firestore
export const db = getFirestore(app);

// Initialize Analytics (only in browser)
export const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;

export default app; 