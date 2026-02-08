const axios = require('axios');

class MCPClient {
  constructor(baseUrl = 'https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream') {
    this.baseUrl = baseUrl;
    this.sessionId = null;
    this.isAuthenticated = false;
  }

  /**
   * Initialize MCP session and get session ID from response header
   */
  async initialize() {
    try {
      const response = await axios.post(this.baseUrl, {
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          capabilities: {
            tools: {}
          },
          clientInfo: {
            name: 'fi-mcp-functions',
            version: '1.0.0'
          }
        }
      });

      // Extract session ID from response header
      this.sessionId = response.headers['mcp-session-id'];
      if (!this.sessionId) {
        throw new Error('No session ID received from MCP server');
      }

      console.log('MCP session initialized with session ID:', this.sessionId);
      return response.data;
    } catch (error) {
      if (error.response) {
        console.error('Failed to initialize MCP session:', {
          status: error.response.status,
          headers: error.response.headers,
          data: error.response.data
        });
      } else {
        console.error('Failed to initialize MCP session:', error.message);
      }
      throw new Error('MCP initialization failed');
    }
  }

  /**
   * Authenticate with the MCP server using the session ID from initialization
   */
  async authenticate(phoneNumber = '9999999999') {
    try {
      if (!this.sessionId) {
        throw new Error('Session ID not available. Call initialize() first.');
      }
      const authResponse = await axios.post(
        `${this.baseUrl.replace('/mcp/stream', '')}/login`,
        `sessionId=${this.sessionId}&phoneNumber=${phoneNumber}`,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      if (authResponse.status === 200) {
        this.isAuthenticated = true;
        console.log('MCP authentication successful');
        return true;
      } else {
        throw new Error(`Authentication failed with status: ${authResponse.status}`);
      }
    } catch (error) {
      console.error('MCP authentication failed:', error.message);
      throw new Error('MCP authentication failed');
    }
  }

  /**
   * List available tools
   */
  async listTools() {
    try {
      const response = await axios.post(this.baseUrl, {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/list',
        params: {}
      }, {
        headers: {
          'MCP-Session-ID': this.sessionId
        }
      });

      return response.data.result;
    } catch (error) {
      if (error.response) {
        console.error('Failed to list tools:', {
          status: error.response.status,
          headers: error.response.headers,
          data: error.response.data
        });
      } else {
        console.error('Failed to list tools:', error.message);
      }
      throw new Error('Failed to list MCP tools');
    }
  }

  /**
   * Call MCP tool
   */
  async callTool(toolName, arguments_ = {}) {
    try {
      const response = await axios.post(this.baseUrl, {
        jsonrpc: '2.0',
        id: Date.now(),
        method: 'tools/call',
        params: {
          name: toolName,
          arguments: arguments_
        }
      }, {
        headers: {
          'MCP-Session-ID': this.sessionId
        }
      });

      if (response.data.error) {
        throw new Error(response.data.error.message);
      }

      // Parse the content from the JSON-RPC response
      const result = response.data.result;
      if (result && result.content && result.content.length > 0) {
        const content = result.content[0];
        if (content.type === 'text' && content.text) {
          try {
            return JSON.parse(content.text);
          } catch (parseError) {
            console.error('Failed to parse MCP response:', parseError);
            return result; // Return raw result if parsing fails
          }
        }
      }
      
      return result;
    } catch (error) {
      if (error.response) {
        console.error(`Failed to call tool ${toolName}:`, {
          status: error.response.status,
          headers: error.response.headers,
          data: error.response.data
        });
      } else {
        console.error(`Failed to call tool ${toolName}:`, error.message);
      }
      throw new Error(`MCP tool call failed: ${error.message}`);
    }
  }

  /**
   * Fetch net worth data
   */
  async fetchNetWorth() {
    return await this.callTool('fetch_net_worth');
  }

  /**
   * Fetch credit report data
   */
  async fetchCreditReport() {
    return await this.callTool('fetch_credit_report');
  }

  /**
   * Fetch EPF details
   */
  async fetchEPFDetails() {
    return await this.callTool('fetch_epf_details');
  }

  /**
   * Fetch mutual fund transactions
   */
  async fetchMFTransactions() {
    return await this.callTool('fetch_mf_transactions');
  }

  /**
   * Fetch bank transactions
   */
  async fetchBankTransactions() {
    return await this.callTool('fetch_bank_transactions');
  }
}

module.exports = MCPClient; 