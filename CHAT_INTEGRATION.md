# Chat Integration with AI Backend

## Overview

The chat functionality has been successfully integrated with your existing frontend, allowing users to interact with the AI financial assistant using their phone number from their profile.

## Features

### ✅ Integrated Features

1. **User Authentication Integration**
   - Uses phone number from logged-in user's profile
   - Automatically formats phone number for API calls (+91 prefix)
   - Seamless integration with existing Firebase authentication

2. **Chat Sessions Management**
   - Create new chat sessions
   - View existing sessions
   - Switch between different conversations
   - Session persistence across browser sessions

3. **Real-time Chat Interface**
   - Modern, responsive chat UI
   - Message history with timestamps
   - Loading states and error handling
   - Auto-scroll to latest messages

4. **AI Response Features**
   - Displays AI recommendations and insights
   - Shows agent type and confidence levels
   - Rich message formatting with metadata

## Backend Integration

### API Endpoints Used

- **Health Check**: `GET /health`
- **Create Session**: `POST /api/v1/sessions`
- **Get Sessions**: `GET /api/v1/sessions/{phone_number}`
- **Get Session Details**: `GET /api/v1/sessions/{phone_number}/{session_id}`
- **Send Message**: `POST /api/v1/chat`

### Backend URL
```
https://fi-money-ai-backend-t6ntegeouq-uc.a.run.app
```

## How It Works

### 1. User Authentication Flow
```javascript
// User logs in with Google
// Phone number is stored in Firebase
// Chat component fetches phone number from user profile
const userRef = doc(db, 'users', user.uid);
const userSnap = await getDoc(userRef);
const phoneNumber = userSnap.data().phoneNumber;
```

### 2. Chat Session Flow
```javascript
// Create new session
const response = await fetch(`${BACKEND_URL}/api/v1/sessions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone_number: userPhoneNumber,
    title: 'Chat Session'
  })
});
```

### 3. Message Sending Flow
```javascript
// Send message to AI
const response = await fetch(`${BACKEND_URL}/api/v1/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone_number: userPhoneNumber,
    message: userMessage,
    session_id: currentSession?.session_id
  })
});
```

## File Structure

```
components/
├── Chat/
│   └── ChatInterface.js     # Main chat component
├── Dashboard/
│   └── Dashboard.js         # Updated with chat integration
└── Auth/
    └── ...                  # Existing auth components

styles/
├── globals.css              # Updated with chat styles import
└── chat.css                 # Chat-specific styles
```

## Usage

### For Users

1. **Sign in with Google** - Existing authentication flow
2. **Set Phone Number** - If not already set, user will be prompted
3. **Click "Start Chat"** - Opens the chat interface
4. **Ask Questions** - Type financial questions in natural language
5. **View Responses** - Get AI-powered financial advice with recommendations

### For Developers

1. **Chat Component**: `components/Chat/ChatInterface.js`
2. **Integration Point**: `components/Dashboard/Dashboard.js`
3. **Styling**: `styles/chat.css`
4. **Backend URL**: Configured in ChatInterface component

## Error Handling

- **Phone Number Missing**: Shows error if user hasn't set phone number
- **Network Errors**: Displays user-friendly error messages
- **API Failures**: Graceful fallback with retry options
- **Session Issues**: Automatic session recovery

## Testing

Run the test script to verify integration:
```bash
node test_chat_integration.js
```

## Security

- Phone numbers are validated and formatted
- API calls use HTTPS
- User authentication required
- Session-based conversation tracking

## Future Enhancements

- [ ] WebSocket support for real-time messaging
- [ ] File upload for financial documents
- [ ] Voice message support
- [ ] Multi-language support
- [ ] Advanced analytics and insights

## Troubleshooting

### Common Issues

1. **Phone Number Not Found**
   - Ensure user has completed phone number setup
   - Check Firebase user document structure

2. **API Connection Issues**
   - Verify backend URL is correct
   - Check network connectivity
   - Ensure CORS is properly configured

3. **Session Not Loading**
   - Clear browser cache
   - Check browser console for errors
   - Verify API responses

### Debug Mode

Enable debug logging by adding to ChatInterface.js:
```javascript
const DEBUG = true;
if (DEBUG) console.log('API Response:', data);
```

## API Documentation

For detailed API documentation, see: `ai/API_DOCUMENTATION.md`

## Deployment Status

✅ **Backend**: Deployed to Google Cloud Run  
✅ **Frontend**: Integrated with existing Next.js app  
✅ **Database**: Firestore integration working  
✅ **Authentication**: Google Sign-in with phone number  

The chat integration is now fully functional and ready for use! 