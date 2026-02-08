const MCPClient = require('./mcp-client');
const {
  processNetWorthData,
  processCreditData,
  processEPFData,
  processMFTransactions
} = require('./utils');

/**
 * Test script for MCP integration
 * Run this to verify all functions work correctly
 */

async function testMCPIntegration() {
  console.log('🧪 Testing Fi MCP Integration...\n');

  try {
    // Initialize MCP client
    console.log('1. Initializing MCP client...');
    const mcpClient = new MCPClient();
    await mcpClient.initialize();
    console.log('✅ MCP client initialized successfully\n');

    // Test 1: List available tools
    console.log('2. Testing tool listing...');
    const tools = await mcpClient.listTools();
    console.log('✅ Available tools:', tools.tools?.map(t => t.name) || []);
    console.log('');

    // Test 2: Fetch net worth
    console.log('3. Testing net worth fetch...');
    try {
      const netWorthData = await mcpClient.fetchNetWorth();
      const processedNetWorth = processNetWorthData(netWorthData);
      console.log('✅ Net worth data fetched successfully');
      console.log(`   Total Net Worth: ${processedNetWorth.formattedTotalNetWorth}`);
      console.log(`   Assets: ${processedNetWorth.assets.length} items`);
    } catch (error) {
      console.log('⚠️  Net worth fetch failed:', error.message);
    }
    console.log('');

    // Test 3: Fetch credit report
    console.log('4. Testing credit report fetch...');
    try {
      const creditData = await mcpClient.fetchCreditReport();
      const processedCredit = processCreditData(creditData);
      console.log('✅ Credit report fetched successfully');
      console.log(`   Credit Score: ${processedCredit.creditScore || 'N/A'}`);
      console.log(`   Accounts: ${processedCredit.accounts.length} items`);
    } catch (error) {
      console.log('⚠️  Credit report fetch failed:', error.message);
    }
    console.log('');

    // Test 4: Fetch EPF details
    console.log('5. Testing EPF details fetch...');
    try {
      const epfData = await mcpClient.fetchEPFDetails();
      const processedEPF = processEPFData(epfData);
      console.log('✅ EPF details fetched successfully');
      console.log(`   Total Balance: ₹${processedEPF.totalBalance.toLocaleString()}`);
      console.log(`   Employee Share: ₹${processedEPF.employeeShare.toLocaleString()}`);
      console.log(`   Employer Share: ₹${processedEPF.employerShare.toLocaleString()}`);
    } catch (error) {
      console.log('⚠️  EPF details fetch failed:', error.message);
    }
    console.log('');

    // Test 5: Fetch mutual fund transactions
    console.log('6. Testing mutual fund transactions fetch...');
    try {
      const mfData = await mcpClient.fetchMFTransactions();
      const processedMF = processMFTransactions(mfData);
      console.log('✅ Mutual fund transactions fetched successfully');
      console.log(`   Total Transactions: ${processedMF.totalTransactions}`);
      console.log(`   Schemes: ${Object.keys(processedMF.schemes).length} items`);
    } catch (error) {
      console.log('⚠️  Mutual fund transactions fetch failed:', error.message);
    }
    console.log('');

    console.log('🎉 MCP integration test completed!');

  } catch (error) {
    console.error('❌ MCP integration test failed:', error.message);
    process.exit(1);
  }
}

/**
 * Test individual function with sample data
 */
function testDataProcessing() {
  console.log('🧪 Testing data processing functions...\n');

  // Sample net worth data
  const sampleNetWorth = {
    netWorthResponse: {
      totalNetWorthValue: {
        currencyCode: "INR",
        units: "1500000"
      },
      assetValues: [
        {
          netWorthAttribute: "ASSET_TYPE_SAVINGS_ACCOUNTS",
          value: {
            currencyCode: "INR",
            units: "500000"
          }
        }
      ]
    }
  };

  const processedNetWorth = processNetWorthData(sampleNetWorth);
  console.log('✅ Net worth processing test passed');
  console.log(`   Processed amount: ${processedNetWorth.formattedTotalNetWorth}`);

  // Sample credit data
  const sampleCredit = {
    creditReports: [{
      creditReportData: {
        score: {
          bureauScore: "750"
        },
        creditAccount: {
          creditAccountDetails: [{
            identificationNumber: "AV12345678",
            subscriberName: "Federal Bank",
            creditLimitAmount: "500000",
            currentBalance: "50000"
          }]
        }
      }
    }]
  };

  const processedCredit = processCreditData(sampleCredit);
  console.log('✅ Credit data processing test passed');
  console.log(`   Credit score: ${processedCredit.creditScore}`);

  // Sample EPF data
  const sampleEPF = {
    uanAccounts: [{
      rawDetails: {
        overall_pf_balance: {
          current_pf_balance: "250000",
          employee_share_total: {
            balance: "125000"
          },
          employer_share_total: {
            balance: "125000"
          }
        }
      }
    }]
  };

  const processedEPF = processEPFData(sampleEPF);
  console.log('✅ EPF data processing test passed');
  console.log(`   Total balance: ₹${processedEPF.totalBalance.toLocaleString()}`);

  // Sample MF transactions
  const sampleMF = {
    transactions: [{
      isinNumber: "INF123L01234",
      folioId: "1234567890",
      externalOrderType: "BUY",
      transactionDate: "2025-01-01T23:59:59Z",
      transactionAmount: {
        currencyCode: "INR",
        units: "10000"
      },
      transactionUnits: 98.765,
      schemeName: "Epifi Tax Saver Fund"
    }]
  };

  const processedMF = processMFTransactions(sampleMF);
  console.log('✅ MF transactions processing test passed');
  console.log(`   Transactions: ${processedMF.totalTransactions}`);

  console.log('\n🎉 All data processing tests passed!');
}

// Run tests if this file is executed directly
if (require.main === module) {
  console.log('🚀 Starting Fi MCP Integration Tests\n');
  
  // Test data processing first
  testDataProcessing();
  console.log('\n' + '='.repeat(50) + '\n');
  
  // Test actual MCP integration
  testMCPIntegration();
}

module.exports = {
  testMCPIntegration,
  testDataProcessing
}; 