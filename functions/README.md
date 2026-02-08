# Fi MCP Google Cloud Functions

This repository contains Google Cloud Functions that integrate with the Fi MCP (Model Context Protocol) to provide comprehensive financial data access.

## 🚀 Features

- **Net Worth Analysis**: Complete asset and liability breakdown
- **Credit Report Access**: Credit scores and account details
- **EPF Information**: Employee Provident Fund balances and details
- **Mutual Fund Analytics**: Transaction history and portfolio analysis
- **Financial Dashboard**: Comprehensive financial overview
- **Portfolio Analytics**: Detailed investment insights

## 📋 Prerequisites

- Google Cloud Platform account
- Google Cloud CLI installed and configured
- Node.js 18+ installed
- Fi MCP server running on `http://localhost:8080/mcp/stream`

## 🛠️ Setup

### 1. Install Dependencies

```bash
cd functions
npm install
```

### 2. Configure Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Update Configuration

Edit `deploy.sh` and replace `your-project-id` with your actual Google Cloud project ID.

## 🚀 Deployment

### Quick Deploy

```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Manual Deploy

```bash
# Deploy individual functions
gcloud functions deploy getNetWorth \
  --gen2 \
  --runtime=nodejs18 \
  --region=us-central1 \
  --source=. \
  --entry-point=getNetWorth \
  --trigger-http \
  --allow-unauthenticated \
  --memory=256MB \
  --timeout=60s
```

## 📡 API Endpoints

### 1. Get Net Worth Data
```
GET /getNetWorth
```

**Response:**
```json
{
  "success": true,
  "data": {
    "totalNetWorth": 1500000,
    "formattedTotalNetWorth": "₹15,00,000.00",
    "currency": "INR",
    "assets": [
      {
        "type": "ASSET_TYPE_SAVINGS_ACCOUNTS",
        "value": 500000,
        "formattedValue": "₹5,00,000.00"
      }
    ],
    "mutualFunds": [...],
    "accountDetails": {...}
  }
}
```

### 2. Get Credit Report
```
GET /getCreditReport
```

**Response:**
```json
{
  "success": true,
  "data": {
    "creditScore": 750,
    "accounts": [
      {
        "id": "AV12345678",
        "subscriber": "Federal Bank",
        "accountType": "10",
        "creditLimit": 500000,
        "currentBalance": 50000
      }
    ],
    "totalAccounts": 2,
    "activeAccounts": 2
  }
}
```

### 3. Get EPF Details
```
GET /getEPFDetails
```

**Response:**
```json
{
  "success": true,
  "data": {
    "totalBalance": 250000,
    "employeeShare": 125000,
    "employerShare": 125000,
    "pensionBalance": 50000,
    "employerDetails": [...]
  }
}
```

### 4. Get Mutual Fund Transactions
```
GET /getMFTransactions
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "isin": "INF123L01234",
        "type": "BUY",
        "date": "2025-01-01T23:59:59Z",
        "amount": 10000,
        "units": 98.765,
        "schemeName": "Epifi Tax Saver Fund"
      }
    ],
    "schemes": {...},
    "totalTransactions": 25
  }
}
```

### 5. Get Financial Dashboard
```
GET /getFinancialDashboard
```

**Response:**
```json
{
  "success": true,
  "data": {
    "netWorth": {...},
    "credit": {...},
    "epf": {...},
    "mutualFunds": {...},
    "summary": {
      "totalAssets": 1500000,
      "creditScore": 750,
      "epfBalance": 250000,
      "totalTransactions": 25,
      "lastUpdated": "2025-01-01T12:00:00.000Z"
    }
  }
}
```

### 6. Get Portfolio Analytics
```
GET /getPortfolioAnalytics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "portfolio": {
      "totalNetWorth": 1500000,
      "formattedNetWorth": "₹15,00,000.00",
      "assetBreakdown": [...],
      "mutualFundSchemes": [...]
    },
    "mutualFunds": {
      "totalTransactions": 25,
      "schemes": {...},
      "transactionHistory": [...]
    },
    "insights": [
      {
        "type": "net_worth",
        "message": "Your total net worth is ₹15,00,000.00",
        "priority": "high"
      }
    ]
  }
}
```

### 7. Health Check
```
GET /healthCheck
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "mcpConnection": "connected",
    "availableTools": [
      "fetch_net_worth",
      "fetch_credit_report",
      "fetch_epf_details",
      "fetch_mf_transactions"
    ],
    "timestamp": "2025-01-01T12:00:00.000Z"
  }
}
```

## 🔧 Configuration

### Environment Variables

- `MCP_BASE_URL`: MCP server URL (default: `http://localhost:8080/mcp/stream`)

### Function Settings

- **Runtime**: Node.js 18
- **Memory**: 256MB
- **Timeout**: 60 seconds
- **Authentication**: Unauthenticated (for demo purposes)

## 🧪 Testing

### Local Testing

```bash
# Install functions framework
npm install -g @google-cloud/functions-framework

# Start local server
functions-framework --target=getNetWorth --port=8081

# Test with curl
curl http://localhost:8081
```

### Testing with Sample Data

```bash
# Test net worth endpoint
curl -X GET "https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/getNetWorth"

# Test health check
curl -X GET "https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/healthCheck"
```

## 📊 Error Handling

All functions return consistent error responses:

```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2025-01-01T12:00:00.000Z"
}
```

Common error scenarios:
- MCP server not running
- Network connectivity issues
- Invalid data format
- Authentication failures

## 🔒 Security Considerations

1. **CORS**: All functions support CORS for web applications
2. **Input Validation**: All inputs are validated before processing
3. **Error Logging**: Errors are logged for debugging
4. **Rate Limiting**: Consider implementing rate limiting for production

## 🚀 Production Deployment

For production deployment:

1. **Update MCP URL**: Change `MCP_BASE_URL` to production MCP server
2. **Add Authentication**: Implement proper authentication
3. **Enable Monitoring**: Set up Cloud Monitoring
4. **Add Logging**: Configure structured logging
5. **Set up CI/CD**: Automate deployment pipeline

## 📝 Troubleshooting

### Common Issues

1. **MCP Connection Failed**
   - Verify MCP server is running on localhost:8080
   - Check network connectivity
   - Verify MCP server configuration

2. **Function Timeout**
   - Increase timeout in deployment script
   - Optimize data processing
   - Check MCP server response time

3. **Memory Issues**
   - Increase memory allocation
   - Optimize data processing
   - Implement pagination for large datasets

### Debug Commands

```bash
# View function logs
gcloud functions logs read getNetWorth --region=us-central1

# Check function status
gcloud functions describe getNetWorth --region=us-central1

# Test function locally
functions-framework --target=getNetWorth --port=8081
```

## 📚 Additional Resources

- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Fi MCP Documentation](./README.md)
- [Node.js Documentation](https://nodejs.org/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 