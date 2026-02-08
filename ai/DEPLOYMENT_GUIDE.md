# FiMoney AI Agent - Deployment Guide

## Overview
This guide will help you deploy the FiMoney AI Agent backend to Google Cloud Run for external service integration.

## Prerequisites

1. **Google Cloud SDK**: Install and configure gcloud CLI
   ```bash
   # Install gcloud (if not already installed)
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

2. **Authentication**: Login to Google Cloud
   ```bash
   gcloud auth login
   gcloud config set project hackathon-62355
   ```

3. **Required APIs**: The deployment script will enable these automatically:
   - Cloud Build API
   - Cloud Run API
   - Firestore API
   - AI Platform API

## Quick Deployment

### Option 1: Automated Deployment (Recommended)
```bash
# Run the automated deployment script
./deploy_cloud_run.sh
```

### Option 2: Manual Deployment
```bash
# Navigate to backend directory
cd backend

# Deploy to Cloud Run
gcloud run deploy fi-money-ai-backend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=hackathon-62355,GOOGLE_CLOUD_REGION=us-central1" \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --concurrency 80 \
    --max-instances 10 \
    --port 8000

# Get the service URL
gcloud run services describe fi-money-ai-backend --region=us-central1 --format="value(status.url)"
```

## Configuration

### Environment Variables
The application uses these environment variables:

- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID (default: hackathon-62355)
- `GOOGLE_CLOUD_REGION`: Your preferred region (default: us-central1)

### Firestore Setup
The Firestore database is automatically configured during deployment. The application uses these collections:
- `users`: User profiles and statistics
- `sessions`: Chat sessions
- `messages`: Chat messages
- `contexts`: User context and preferences

## API Endpoints

Once deployed, your service will be available at:
`https://fi-money-ai-backend-<hash>-uc.a.run.app`

### Key Endpoints:
- **Health Check**: `GET /health`
- **API Documentation**: `GET /docs`
- **Chat**: `POST /api/v1/chat`
- **Multi-Agent Chat**: `POST /api/v1/chat/multi-agent`
- **Sessions**: `GET /api/v1/sessions`
- **Create Session**: `POST /api/v1/sessions`

### Example Usage:
```bash
# Health check
curl https://your-service-url/health

# Create a session
curl -X POST "https://your-service-url/api/v1/sessions?phone_number=+15551234567&title=Test%20Session"

# Send a chat message
curl -X POST "https://your-service-url/api/v1/chat?phone_number=+15551234567&message=Hello,%20I%20need%20financial%20advice"
```

## Testing the Deployment

### 1. Health Check
```bash
curl https://your-service-url/health
```
Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-24T...",
  "connectivity": {
    "agent_factory": true,
    "coordinator_agent": true,
    "mcp_service": true
  }
}
```

### 2. Create a Session
```bash
curl -X POST "https://your-service-url/api/v1/sessions?phone_number=+15551234567&title=Test%20Session"
```

### 3. Send a Chat Message
```bash
curl -X POST "https://your-service-url/api/v1/chat?phone_number=+15551234567&message=I%20need%20investment%20advice"
```

### 4. Multi-Agent Chat
```bash
curl -X POST "https://your-service-url/api/v1/chat/multi-agent?phone_number=+15551234567&message=I%20want%20to%20invest%20in%20stocks%20and%20need%20debt%20management%20advice"
```

## Integration with External Services

### Frontend Integration
```javascript
// Example JavaScript integration
const API_BASE_URL = 'https://your-service-url';

// Create a session
async function createSession(phoneNumber, title) {
    const response = await fetch(`${API_BASE_URL}/api/v1/sessions?phone_number=${phoneNumber}&title=${title}`, {
        method: 'POST'
    });
    return response.json();
}

// Send a chat message
async function sendMessage(phoneNumber, message, sessionId = null) {
    const params = new URLSearchParams({
        phone_number: phoneNumber,
        message: message
    });
    if (sessionId) params.append('session_id', sessionId);
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat?${params}`, {
        method: 'POST'
    });
    return response.json();
}
```

### Mobile App Integration
```python
# Example Python integration
import requests

API_BASE_URL = 'https://your-service-url'

def send_chat_message(phone_number, message, session_id=None):
    params = {
        'phone_number': phone_number,
        'message': message
    }
    if session_id:
        params['session_id'] = session_id
    
    response = requests.post(f'{API_BASE_URL}/api/v1/chat', params=params)
    return response.json()
```

## Monitoring and Logging

### View Logs
```bash
# View Cloud Run logs
gcloud logs read --project=hackathon-62355 --filter="resource.type=cloud_run_revision AND resource.labels.service_name=fi-money-ai-backend" --limit=50
```

### Monitor Performance
- Use Google Cloud Console to monitor:
  - Request latency
  - Error rates
  - Memory usage
  - CPU usage

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   gcloud auth login
   gcloud config set project hackathon-62355
   ```

2. **Permission Errors**
   ```bash
   # Ensure you have the necessary roles
   gcloud projects add-iam-policy-binding hackathon-62355 \
       --member="user:your-email@gmail.com" \
       --role="roles/run.admin"
   ```

3. **Service Not Starting**
   - Check the logs: `gcloud logs read --project=hackathon-62355`
   - Verify environment variables are set correctly
   - Ensure Firestore is properly configured

4. **API Errors**
   - Check the `/health` endpoint first
   - Verify Firestore connectivity
   - Check agent initialization logs

### Debug Mode
To run locally for debugging:
```bash
cd backend
source ../venv/bin/activate
python main.py
```

## Security Considerations

1. **Authentication**: Consider implementing API keys for production
2. **Rate Limiting**: Implement rate limiting for public endpoints
3. **CORS**: Configure CORS headers for web applications
4. **Environment Variables**: Use Google Secret Manager for sensitive data

## Cost Optimization

1. **Scaling**: Adjust `--max-instances` based on expected load
2. **Memory**: Start with 2Gi, adjust based on usage
3. **CPU**: Start with 2 CPUs, scale as needed
4. **Concurrency**: Adjust based on request patterns

## Support

For issues or questions:
1. Check the logs first
2. Test the `/health` endpoint
3. Verify Firestore connectivity
4. Review the API documentation at `/docs`

## Next Steps

After successful deployment:
1. Test all endpoints thoroughly
2. Integrate with your frontend/mobile app
3. Set up monitoring and alerting
4. Configure custom domain (optional)
5. Implement authentication (recommended for production) 