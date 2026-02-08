# FiMoney AI Agent - Personal Finance AI Assistant

A multi-agent AI system that provides personalized financial insights using Google's Gemini models and Fi Money's MCP Server integration, with phone number-based user management and Firestore data persistence.

## 🎯 Overview

FiMoney AI Agent is a sophisticated multi-agent system that delivers deeply personalized financial insights by combining:

- **Phone number-based user management** for easy identification and session management
- **Multiple chat sessions per user** for organizing different conversation topics
- **Firestore data persistence** for reliable chat history and context storage
- **Structured financial data** from Fi Money's MCP Server
- **Conversational AI** using Google's Gemini models
- **Persistent chat context** for personalized experiences
- **Multi-agent orchestration** for specialized financial analysis

## 🏗️ Architecture

### Phone Number-Based User Management

- **User Identification**: Users are identified by their phone numbers
- **Multiple Sessions**: Each user can have multiple active chat sessions
- **Session Management**: Create, view, and manage sessions independently
- **Context Preservation**: Chat history is maintained per session for context

### Multi-Agent System

1. **Financial Coordinator Agent** - Primary advisor and conversation orchestrator
2. **Investment Analysis Agent** - Specialized in investment portfolio analysis
3. **Debt & Credit Agent** - Specialized in debt management and credit analysis
4. **Wealth Planning Agent** - Specialized in net worth analysis and long-term planning
5. **Financial Health Monitor Agent** - Specialized in anomaly detection and financial health

### Technology Stack

- **Google Cloud Functions** - MCP integration and data processing
- **Firestore** - Chat history, user context, and session storage
- **Vertex AI** - Gemini model integration
- **Cloud Run** - Agent orchestration service
- **Google Agent Framework** - Multi-agent orchestration

## 🚀 Features

### Phone Number-Based User Management
- **Easy User Identification**: Use phone numbers as unique user identifiers
- **Multiple Sessions**: Create separate sessions for different financial topics
- **Session Persistence**: All conversations are stored in Firestore
- **Context Awareness**: Each session maintains its own conversation history

### Natural Language Financial Conversations
- "How much money will I have at 40?"
- "How's my net worth growing?"
- "Can I afford a ₹50L home loan?"
- "Which SIPs underperformed the market?"

### Specialized Financial Analysis
- **Investment Analysis**: Portfolio performance, SIP analysis, rebalancing
- **Debt Management**: Loan affordability, debt optimization
- **Wealth Planning**: Net worth projections, retirement planning
- **Financial Health**: Anomaly detection, risk assessment

### Context-Aware Conversations
- Remembers user's financial goals and preferences
- Builds on previous conversations within each session
- Provides personalized recommendations
- Maintains conversation continuity across sessions

## 📁 Project Structure

```
FiMoneyAI/
├── backend/
│   ├── agents/           # Multi-agent system
│   ├── services/         # Business logic services
│   │   ├── firestore_service.py  # Firestore operations
│   │   ├── chat_service.py       # Chat management
│   │   └── agent_service.py      # Agent orchestration
│   ├── models/           # Data models
│   │   └── chat.py       # Phone number-based models
│   ├── utils/            # Utility functions
│   └── config/           # Configuration
├── API_DOCUMENTATION.md  # Complete API documentation
├── INTEGRATION_GUIDE.md  # Integration guide for existing frontend
├── deploy.sh            # Deployment script
├── test_api.py          # API testing script
└── env.example          # Environment configuration
```

## 🔧 Setup

### Prerequisites
- Python 3.11+
- Google Cloud SDK
- Firestore database
- Existing frontend with chat functionality

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd FiMoneyAI

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### Environment Setup
```bash
# Copy environment template
cp config.env .env

# Configure Google Cloud credentials
gcloud auth application-default login

# Update .env with your configuration
# - Set GOOGLE_CLOUD_PROJECT to your project ID
# - Set GOOGLE_API_KEY to your API key
# - Set MCP_FUNCTION_URL to your existing GCP functions URL
```

### Firestore Setup
1. Create a Firestore database in your Google Cloud project
2. Download the service account key and save as `service-account-key.json`
3. Configure Firestore security rules as needed

## 🚀 Deployment

### Quick Deployment
```bash
# Set your project ID
export GOOGLE_CLOUD_PROJECT=your-project-id

# Run the deployment script
./deploy.sh
```

### Manual Deployment
```bash
# Deploy the backend
cd backend
gcloud run deploy fi-money-ai-backend --source .
```

### Testing the Deployment
```bash
# Test the API functionality
python test_api.py https://your-service-url
```

## 📚 API Usage

### Basic Chat Integration
```javascript
// Send a message to the AI agent
const response = await fetch('/api/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone_number: '+1234567890',
    message: 'How much money will I have at 40?',
    session_id: 'optional-session-id'
  })
});

const result = await response.json();
// result.response.message contains the AI response
```

### Session Management
```javascript
// Create a new session
const sessionResponse = await fetch('/api/v1/sessions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone_number: '+1234567890',
    title: 'Investment Planning'
  })
});

// Get user sessions
const sessionsResponse = await fetch('/api/v1/sessions/+1234567890');
```

### WebSocket for Real-time Chat
```javascript
// Connect to WebSocket for real-time chat
const ws = new WebSocket(`ws://your-backend-url/ws/chat/+1234567890`);

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  // Handle the AI response in your chat UI
  displayMessage(data.response.message, 'assistant');
};
```

## 🔒 Security & Privacy

- Phone number-based user identification
- Secure Firestore data storage
- User-controlled data access
- Secure GCP function calls
- No data persistence without consent
- Export capabilities for user insights
- End-to-end encryption for sensitive data

## 📊 Data Flow

```
Your Frontend Chat → API Call → 
Phone Number Validation → 
Session Management → 
Multi-Agent System → 
Gemini Analysis → 
MCP Function Call → 
Financial Data → 
Specialized Agent Response → 
Firestore Storage → 
Formatted Response → Your Frontend
```

## 🧪 Testing

### Run API Tests
```bash
# Test local development server
python test_api.py

# Test deployed service
python test_api.py https://your-service-url
```

### Test Individual Endpoints
```bash
# Health check
curl https://your-service-url/health

# Create session
curl -X POST https://your-service-url/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "title": "Test Session"}'

# Send chat message
curl -X POST https://your-service-url/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "message": "Hello"}'
```

## 📖 Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Frontend integration guide
- **[Deployment Guide](deploy.sh)** - Automated deployment script

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For support and questions, please open an issue in the repository. 