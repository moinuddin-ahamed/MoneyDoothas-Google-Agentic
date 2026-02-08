# FiMoney AI Agent API Documentation

## Overview

The FiMoney AI Agent API provides a phone number-based chat system with multi-agent financial analysis capabilities. Each user is identified by their phone number and can have multiple active chat sessions.

## Base URL

```
https://your-backend-url.com
```

## Authentication

Currently, the API uses phone number-based authentication. All endpoints require a valid phone number.

## API Endpoints

### 1. Health Check

**GET** `/health`

Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "connectivity": {
    "agent_factory": true,
    "coordinator_agent": true,
    "mcp_service": true
  }
}
```

### 2. Chat Endpoints

#### Send Chat Message

**POST** `/api/v1/chat`

Send a message to the AI agent and get a response.

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "message": "How much money will I have at 40?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid-session-id",
  "phone_number": "+1234567890",
  "response": {
    "message": "Based on your current financial situation...",
    "agent_type": "investment_analyst",
    "confidence": 0.85,
    "recommendations": [
      "Consider increasing your SIP amount",
      "Diversify your portfolio"
    ],
    "insights": [
      "Your portfolio has grown 12% this year",
      "You have 3 underperforming funds"
    ],
    "next_actions": [
      "Review your mutual fund allocations",
      "Set up automatic rebalancing"
    ],
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "metadata": {
    "agent_used": "investment_analyst",
    "processing_time": "2024-01-15T10:30:01Z"
  }
}
```

#### Multi-Agent Chat

**POST** `/api/v1/chat/multi-agent`

Get responses from multiple specialized agents for complex queries.

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "message": "Analyze my investment portfolio and debt situation",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid-session-id",
  "phone_number": "+1234567890",
  "response": {
    "primary_response": {
      "message": "Comprehensive analysis...",
      "agent_type": "coordinator",
      "confidence": 0.9
    },
    "specialized_response": {
      "message": "Investment analysis...",
      "agent_type": "investment_analyst",
      "confidence": 0.85
    },
    "agent_used": "investment_analyst",
    "confidence": 0.9
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. Session Management

#### Create New Session

**POST** `/api/v1/sessions`

Create a new chat session for a user.

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "title": "Investment Planning Session"
}
```

**Response:**
```json
{
  "success": true,
  "session": {
    "session_id": "uuid-session-id",
    "phone_number": "+1234567890",
    "title": "Investment Planning Session",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "is_active": true
  }
}
```

#### Get User Sessions

**GET** `/api/v1/sessions/{phone_number}`

Get all chat sessions for a user.

**Query Parameters:**
- `active_only` (boolean, default: true) - Only return active sessions

**Response:**
```json
{
  "success": true,
  "phone_number": "+1234567890",
  "sessions": [
    {
      "session_id": "uuid-session-id-1",
      "title": "Investment Planning Session",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:35:00Z",
      "is_active": true,
      "message_count": 5
    },
    {
      "session_id": "uuid-session-id-2",
      "title": "Debt Management Session",
      "created_at": "2024-01-14T15:20:00Z",
      "updated_at": "2024-01-14T15:45:00Z",
      "is_active": true,
      "message_count": 3
    }
  ],
  "total_sessions": 2
}
```

#### Get Session Details

**GET** `/api/v1/sessions/{phone_number}/{session_id}`

Get detailed information about a specific chat session including all messages.

**Response:**
```json
{
  "success": true,
  "session": {
    "session_id": "uuid-session-id",
    "phone_number": "+1234567890",
    "title": "Investment Planning Session",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z",
    "is_active": true,
    "messages": [
      {
        "id": "msg-uuid-1",
        "role": "user",
        "content": "How much money will I have at 40?",
        "message_type": "text",
        "timestamp": "2024-01-15T10:30:00Z",
        "metadata": null
      },
      {
        "id": "msg-uuid-2",
        "role": "assistant",
        "content": "Based on your current financial situation...",
        "message_type": "analysis",
        "timestamp": "2024-01-15T10:30:05Z",
        "metadata": {
          "agent_type": "investment_analyst",
          "confidence": 0.85
        }
      }
    ],
    "context": {
      "phone_number": "+1234567890",
      "financial_goals": ["savings", "investment"],
      "risk_tolerance": "moderate",
      "investment_horizon": "medium",
      "preferred_currencies": ["INR"],
      "notification_preferences": {},
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:05Z"
    },
    "metadata": null
  }
}
```

#### Deactivate Session

**DELETE** `/api/v1/sessions/{phone_number}/{session_id}`

Deactivate a chat session.

**Response:**
```json
{
  "success": true,
  "session_id": "uuid-session-id",
  "phone_number": "+1234567890",
  "message": "Session deactivated successfully"
}
```

### 4. User Management

#### Get User Statistics

**GET** `/api/v1/users/{phone_number}/stats`

Get user statistics and activity information.

**Response:**
```json
{
  "success": true,
  "stats": {
    "phone_number": "+1234567890",
    "name": "John Doe",
    "total_sessions": 5,
    "active_sessions": 2,
    "created_at": "2024-01-10T09:00:00Z",
    "last_active": "2024-01-15T10:35:00Z"
  }
}
```

### 5. Financial Data

#### Get Financial Data

**GET** `/api/v1/financial-data`

Get comprehensive financial data for analysis.

**Response:**
```json
{
  "financial_data": {
    "investments": {
      "total_value": 500000,
      "sip_amount": 10000,
      "portfolio": [...]
    },
    "debts": {
      "total_debt": 200000,
      "loans": [...]
    },
    "savings": {
      "total_savings": 300000,
      "accounts": [...]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 6. WebSocket Chat

#### Real-time Chat

**WebSocket** `/ws/chat/{phone_number}`

Connect to WebSocket for real-time chat functionality.

**Connection:**
```javascript
const ws = new WebSocket(`ws://your-backend-url/ws/chat/+1234567890`);
```

**Send Message:**
```json
{
  "message": "How much money will I have at 40?",
  "session_id": "optional-session-id"
}
```

**Receive Response:**
```json
{
  "success": true,
  "session_id": "uuid-session-id",
  "phone_number": "+1234567890",
  "response": {
    "message": "Based on your current financial situation...",
    "agent_type": "investment_analyst",
    "confidence": 0.85,
    "recommendations": [...],
    "insights": [...],
    "next_actions": [...],
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (missing required parameters)
- `404` - Not Found (session not found)
- `403` - Forbidden (access denied)
- `500` - Internal Server Error

### Example Error Response

```json
{
  "detail": "Phone number is required"
}
```

## Integration Examples

### JavaScript/Node.js

```javascript
// Send a chat message
async function sendChatMessage(phoneNumber, message, sessionId = null) {
  const response = await fetch('/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      phone_number: phoneNumber,
      message: message,
      session_id: sessionId
    })
  });
  
  return await response.json();
}

// Create a new session
async function createSession(phoneNumber, title = null) {
  const response = await fetch('/api/v1/sessions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      phone_number: phoneNumber,
      title: title
    })
  });
  
  return await response.json();
}

// Get user sessions
async function getUserSessions(phoneNumber, activeOnly = true) {
  const response = await fetch(`/api/v1/sessions/${phoneNumber}?active_only=${activeOnly}`);
  return await response.json();
}
```

### Python

```python
import requests

# Send a chat message
def send_chat_message(phone_number, message, session_id=None):
    response = requests.post('/api/v1/chat', json={
        'phone_number': phone_number,
        'message': message,
        'session_id': session_id
    })
    return response.json()

# Create a new session
def create_session(phone_number, title=None):
    response = requests.post('/api/v1/sessions', json={
        'phone_number': phone_number,
        'title': title
    })
    return response.json()

# Get user sessions
def get_user_sessions(phone_number, active_only=True):
    response = requests.get(f'/api/v1/sessions/{phone_number}?active_only={active_only}')
    return response.json()
```

## Best Practices

1. **Phone Number Format**: Use international format (e.g., +1234567890)
2. **Session Management**: Create new sessions for different conversation topics
3. **Error Handling**: Always check the `success` field in responses
4. **Rate Limiting**: Implement appropriate rate limiting for your use case
5. **Context Preservation**: Use session IDs to maintain conversation context

## Deployment

### Environment Variables

Set these environment variables in your deployment:

```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
VERTEX_AI_LOCATION=us-central1
MCP_FUNCTION_URL=https://your-mcp-function-url
```

### Firestore Setup

1. Create a Firestore database in your Google Cloud project
2. Set up the service account key file (`service-account-key.json`)
3. Configure Firestore security rules as needed

### Health Monitoring

Monitor the `/health` endpoint to ensure the service is running properly and all dependencies are available. 