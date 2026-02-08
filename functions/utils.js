/**
 * Utility functions for data processing and response formatting
 */

/**
 * Convert currency format to number
 * @param {Object} currencyObj - Currency object with units and nanos
 * @returns {number} - Converted amount
 */
function currencyToNumber(currencyObj) {
  if (!currencyObj || !currencyObj.units) return 0;
  
  const units = parseFloat(currencyObj.units) || 0;
  const nanos = parseFloat(currencyObj.nanos) || 0;
  
  return units + (nanos / 1000000000);
}

/**
 * Format currency for display
 * @param {number} amount - Amount to format
 * @param {string} currencyCode - Currency code (default: INR)
 * @returns {string} - Formatted currency string
 */
function formatCurrency(amount, currencyCode = 'INR') {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: currencyCode,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(amount);
}

/**
 * Calculate percentage change
 * @param {number} current - Current value
 * @param {number} previous - Previous value
 * @returns {number} - Percentage change
 */
function calculatePercentageChange(current, previous) {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
}

/**
 * Format date string
 * @param {string} dateString - Date string to format
 * @returns {string} - Formatted date
 */
function formatDate(dateString) {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    return dateString;
  }
}

/**
 * Process net worth response
 * @param {Object} response - Raw net worth response
 * @returns {Object} - Processed net worth data
 */
function processNetWorthData(response) {
  if (!response || !response.netWorthResponse) {
    return {
      totalNetWorth: 0,
      currency: 'INR',
      assets: [],
      error: 'No net worth data available'
    };
  }

  const netWorthData = response.netWorthResponse;
  const totalNetWorth = currencyToNumber(netWorthData.totalNetWorthValue);
  const currency = netWorthData.totalNetWorthValue?.currencyCode || 'INR';

  const assets = (netWorthData.assetValues || []).map(asset => ({
    type: asset.netWorthAttribute,
    value: currencyToNumber(asset.value),
    formattedValue: formatCurrency(currencyToNumber(asset.value), currency)
  }));

  return {
    totalNetWorth,
    formattedTotalNetWorth: formatCurrency(totalNetWorth, currency),
    currency,
    assets,
    mutualFunds: response.mfSchemeAnalytics?.schemeAnalytics || [],
    accountDetails: response.accountDetailsBulkResponse?.accountDetailsMap || {}
  };
}

/**
 * Process credit report data
 * @param {Object} response - Raw credit report response
 * @returns {Object} - Processed credit data
 */
function processCreditData(response) {
  if (!response || !response.creditReports || response.creditReports.length === 0) {
    return {
      creditScore: null,
      accounts: [],
      error: 'No credit data available'
    };
  }

  const creditData = response.creditReports[0].creditReportData;
  const score = creditData.score?.bureauScore;
  
  const accounts = (creditData.creditAccount?.creditAccountDetails || []).map(account => ({
    id: account.identificationNumber,
    subscriber: account.subscriberName,
    accountType: account.accountType,
    creditLimit: parseFloat(account.creditLimitAmount) || 0,
    currentBalance: parseFloat(account.currentBalance) || 0,
    paymentRating: account.paymentRating,
    accountStatus: account.accountStatus,
    openDate: account.openDate
  }));

  return {
    creditScore: score ? parseInt(score) : null,
    accounts,
    totalAccounts: creditData.creditAccount?.creditAccountSummary?.account?.creditAccountTotal || 0,
    activeAccounts: creditData.creditAccount?.creditAccountSummary?.account?.creditAccountActive || 0,
    outstandingBalance: creditData.creditAccount?.creditAccountSummary?.totalOutstandingBalance || {}
  };
}

/**
 * Process EPF data
 * @param {Object} response - Raw EPF response
 * @returns {Object} - Processed EPF data
 */
function processEPFData(response) {
  if (!response || !response.uanAccounts || response.uanAccounts.length === 0) {
    return {
      totalBalance: 0,
      employeeShare: 0,
      employerShare: 0,
      error: 'No EPF data available'
    };
  }

  const epfData = response.uanAccounts[0].rawDetails;
  const overallBalance = epfData.overall_pf_balance;

  // Employee share from overall_pf_balance
  const employeeShare = parseFloat(overallBalance?.employee_share_total?.balance) || 0;

  // Employer share: sum all est_details[*].pf_balance.employer_share.balance
  let employerShare = 0;
  if (Array.isArray(epfData.est_details)) {
    employerShare = epfData.est_details.reduce((sum, est) => {
      const bal = parseFloat(est?.pf_balance?.employer_share?.balance) || 0;
      return sum + bal;
    }, 0);
  }

  return {
    totalBalance: parseFloat(overallBalance?.current_pf_balance) || 0,
    employeeShare,
    employerShare,
    pensionBalance: parseFloat(overallBalance?.pension_balance) || 0,
    employerDetails: epfData.est_details || []
  };
}

/**
 * Process mutual fund transactions
 * @param {Object} response - Raw MF transactions response
 * @returns {Object} - Processed transaction data
 */
function processMFTransactions(response) {
  if (!response || !response.mfTransactions) {
    return {
      transactions: [],
      schemes: {},
      error: 'No transaction data available'
    };
  }

  // Flatten all transactions from all schemes
  const transactions = [];
  response.mfTransactions.forEach(scheme => {
    scheme.txns.forEach(txn => {
      const [orderType, date, nav, units, amount] = txn;
      transactions.push({
        isin: scheme.isin,
        folioId: scheme.folioId,
        type: orderType === 1 ? 'BUY' : 'SELL',
        date: date,
        amount: amount,
        units: units,
        nav: nav,
        schemeName: scheme.schemeName
      });
    });
  });

  // Group by scheme
  const schemes = transactions.reduce((acc, tx) => {
    if (!acc[tx.isin]) {
      acc[tx.isin] = {
        isin: tx.isin,
        schemeName: tx.schemeName,
        transactions: [],
        totalInvested: 0,
        totalUnits: 0
      };
    }
    
    acc[tx.isin].transactions.push(tx);
    if (tx.type === 'BUY') {
      acc[tx.isin].totalInvested += tx.amount;
      acc[tx.isin].totalUnits += tx.units;
    } else {
      acc[tx.isin].totalInvested -= tx.amount;
      acc[tx.isin].totalUnits -= tx.units;
    }
    
    return acc;
  }, {});

  return {
    transactions,
    schemes,
    totalTransactions: transactions.length
  };
}

/**
 * Process bank transactions
 * @param {Object} response - Raw bank transactions response
 * @returns {Object} - Processed transaction data
 */
function processBankTransactions(response) {
  if (!response || !response.bankTransactions) {
    return {
      transactions: [],
      banks: {},
      error: 'No bank transaction data available'
    };
  }

  // Flatten all transactions from all banks
  const transactions = [];
  response.bankTransactions.forEach(bank => {
    bank.txns.forEach(txn => {
      const [amount, narration, date, type, mode, balance] = txn;
      const transactionType = getTransactionType(type);
      transactions.push({
        bank: bank.bank,
        amount: parseFloat(amount),
        narration: narration,
        date: date,
        type: transactionType,
        mode: mode,
        balance: parseFloat(balance)
      });
    });
  });

  // Group by bank
  const banks = transactions.reduce((acc, tx) => {
    if (!acc[tx.bank]) {
      acc[tx.bank] = {
        bank: tx.bank,
        transactions: [],
        totalCredits: 0,
        totalDebits: 0,
        currentBalance: 0
      };
    }
    
    acc[tx.bank].transactions.push(tx);
    if (tx.type === 'CREDIT') {
      acc[tx.bank].totalCredits += tx.amount;
    } else if (tx.type === 'DEBIT') {
      acc[tx.bank].totalDebits += tx.amount;
    }
    
    // Use the latest balance
    if (tx.balance > acc[tx.bank].currentBalance) {
      acc[tx.bank].currentBalance = tx.balance;
    }
    
    return acc;
  }, {});

  return {
    transactions,
    banks,
    totalTransactions: transactions.length
  };
}

/**
 * Get transaction type from numeric code
 * @param {number} typeCode - Transaction type code
 * @returns {string} - Transaction type
 */
function getTransactionType(typeCode) {
  const types = {
    1: 'CREDIT',
    2: 'DEBIT',
    3: 'OPENING',
    4: 'INTEREST',
    5: 'TDS',
    6: 'INSTALLMENT',
    7: 'CLOSING',
    8: 'OTHERS'
  };
  return types[typeCode] || 'UNKNOWN';
}

module.exports = {
  currencyToNumber,
  formatCurrency,
  calculatePercentageChange,
  formatDate,
  processNetWorthData,
  processCreditData,
  processEPFData,
  processMFTransactions,
  processBankTransactions
}; 