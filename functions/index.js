const functions = require('@google-cloud/functions-framework');
const cors = require('cors');
const MCPClient = require('./mcp-client');
const {
  processNetWorthData,
  processCreditData,
  processEPFData,
  processMFTransactions,
  processBankTransactions,
  formatCurrency
} = require('./utils');

// Initialize CORS middleware
const corsMiddleware = cors({
  origin: true,
  credentials: true
});

// Helper function to handle CORS
function handleCORS(req, res) {
  return new Promise((resolve) => {
    corsMiddleware(req, res, resolve);
  });
}

// Helper function to send error response
function sendError(res, statusCode, message) {
  res.status(statusCode).json({
    success: false,
    error: message,
    timestamp: new Date().toISOString()
  });
}

// Helper function to send success response
function sendSuccess(res, data) {
  res.status(200).json({
    success: true,
    data,
    timestamp: new Date().toISOString()
  });
}

/**
 * Get Net Worth Data
 * Fetches comprehensive net worth information including assets, liabilities, and mutual fund details
 */
functions.http('getNetWorth', async (req, res) => {
  await handleCORS(req, res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const mcpBaseUrl = process.env.MCP_BASE_URL || 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream';
    const mcpClient = new MCPClient(mcpBaseUrl);
    const phoneNumber = req.query.phoneNumber || req.body?.phoneNumber || '9999999999';
    await mcpClient.initialize();
    await mcpClient.authenticate(phoneNumber);
    
    const rawData = await mcpClient.fetchNetWorth();
    console.log('Raw net worth data received:', JSON.stringify(rawData, null, 2));
    const processedData = processNetWorthData(rawData);
    console.log('Processed net worth data:', JSON.stringify(processedData, null, 2));
    
    sendSuccess(res, processedData);
  } catch (error) {
    console.error('Net worth fetch error:', error);
    sendError(res, 500, `Failed to fetch net worth: ${error.message}`);
  }
});

/**
 * Get Credit Report
 * Fetches credit score, account details, and credit utilization information
 */
functions.http('getCreditReport', async (req, res) => {
  await handleCORS(req, res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const mcpBaseUrl = process.env.MCP_BASE_URL || 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream';
    const mcpClient = new MCPClient(mcpBaseUrl);
    const phoneNumber = req.query.phoneNumber || req.body?.phoneNumber || '9999999999';
    await mcpClient.initialize();
    await mcpClient.authenticate(phoneNumber);
    
    const rawData = await mcpClient.fetchCreditReport();
    const processedData = processCreditData(rawData);
    
    sendSuccess(res, processedData);
  } catch (error) {
    console.error('Credit report fetch error:', error);
    sendError(res, 500, `Failed to fetch credit report: ${error.message}`);
  }
});

/**
 * Get EPF Details
 * Fetches Employee Provident Fund account information and balances
 */
functions.http('getEPFDetails', async (req, res) => {
  await handleCORS(req, res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const mcpBaseUrl = process.env.MCP_BASE_URL || 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream';
    const mcpClient = new MCPClient(mcpBaseUrl);
    const phoneNumber = req.query.phoneNumber || req.body?.phoneNumber || '9999999999';
    await mcpClient.initialize();
    await mcpClient.authenticate(phoneNumber);
    
    const rawData = await mcpClient.fetchEPFDetails();
    console.log('Raw EPF data received:', JSON.stringify(rawData, null, 2));
    const processedData = processEPFData(rawData);
    console.log('Processed EPF data:', JSON.stringify(processedData, null, 2));
    
    sendSuccess(res, processedData);
  } catch (error) {
    console.error('EPF details fetch error:', error);
    sendError(res, 500, `Failed to fetch EPF details: ${error.message}`);
  }
});

/**
 * Get Mutual Fund Transactions
 * Fetches mutual fund transaction history for portfolio analysis
 */
functions.http('getMFTransactions', async (req, res) => {
  await handleCORS(req, res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const mcpBaseUrl = process.env.MCP_BASE_URL || 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream';
    const mcpClient = new MCPClient(mcpBaseUrl);
    const phoneNumber = req.query.phoneNumber || req.body?.phoneNumber || '9999999999';
    await mcpClient.initialize();
    await mcpClient.authenticate(phoneNumber);
    
    const rawData = await mcpClient.fetchMFTransactions();
    const processedData = processMFTransactions(rawData);
    
    sendSuccess(res, processedData);
  } catch (error) {
    console.error('MF transactions fetch error:', error);
    sendError(res, 500, `Failed to fetch mutual fund transactions: ${error.message}`);
  }
});

/**
 * Get Bank Transactions
 * Fetches bank transaction history for financial analysis
 */
functions.http('getBankTransactions', async (req, res) => {
  await handleCORS(req, res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const mcpBaseUrl = process.env.MCP_BASE_URL || 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream';
    const mcpClient = new MCPClient(mcpBaseUrl);
    const phoneNumber = req.query.phoneNumber || req.body?.phoneNumber || '9999999999';
    await mcpClient.initialize();
    await mcpClient.authenticate(phoneNumber);
    
    const rawData = await mcpClient.fetchBankTransactions();
    const processedData = processBankTransactions(rawData);
    
    sendSuccess(res, processedData);
  } catch (error) {
    console.error('Bank transactions fetch error:', error);
    sendError(res, 500, `Failed to fetch bank transactions: ${error.message}`);
  }
});

/**
 * Health Check Endpoint
 * Verifies MCP connection and returns available tools
 */
functions.http('healthCheck', async (req, res) => {
  await handleCORS(req, res);
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const mcpBaseUrl = process.env.MCP_BASE_URL || 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream';
    const mcpClient = new MCPClient(mcpBaseUrl);
    await mcpClient.initialize();
    await mcpClient.authenticate();
    
    const tools = await mcpClient.listTools();
    
    sendSuccess(res, {
      status: 'healthy',
      mcpConnection: 'connected',
      availableTools: tools.tools || [],
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Health check error:', error);
    sendError(res, 503, `MCP connection failed: ${error.message}`);
  }
});

// Export for local testing
if (process.env.NODE_ENV === 'development') {
  module.exports = {
    getNetWorth: functions.http('getNetWorth'),
    getCreditReport: functions.http('getCreditReport'),
    getEPFDetails: functions.http('getEPFDetails'),
    getMFTransactions: functions.http('getMFTransactions'),
    getBankTransactions: functions.http('getBankTransactions'),
    healthCheck: functions.http('healthCheck')
  };
}