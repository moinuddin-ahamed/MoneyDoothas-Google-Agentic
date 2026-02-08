from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class TransactionType(str, Enum):
    """Types of financial transactions."""
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    INSTALLMENT = "INSTALLMENT"
    INTEREST = "INTEREST"
    OTHERS = "OTHERS"


class TransactionMode(str, Enum):
    """Modes of transaction."""
    UPI = "UPI"
    CARD_PAYMENT = "CARD_PAYMENT"
    CASH = "CASH"
    FT = "FT"
    ATM = "ATM"
    NEFT = "NEFT"
    IMPS = "IMPS"
    ACH = "ACH"
    BILLPAY = "BILLPAY"
    CHARGES = "CHARGES"
    INTEREST = "INTEREST"
    INSTALLMENT = "INSTALLMENT"
    OTHERS = "OTHERS"


class BankTransaction(BaseModel):
    """Individual bank transaction model."""
    
    bank: str = Field(..., description="Bank name")
    amount: float = Field(..., description="Transaction amount")
    narration: str = Field(..., description="Transaction description")
    date: str = Field(..., description="Transaction date")
    type: TransactionType = Field(..., description="Transaction type")
    mode: TransactionMode = Field(..., description="Transaction mode")
    balance: float = Field(..., description="Account balance after transaction")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CreditAccount(BaseModel):
    """Credit account information."""
    
    subscriber: str = Field(..., description="Lender name")
    accountType: str = Field(..., description="Account type code")
    creditLimit: float = Field(default=0, description="Credit limit")
    currentBalance: float = Field(..., description="Current outstanding balance")
    paymentRating: str = Field(..., description="Payment history rating")
    accountStatus: str = Field(..., description="Account status code")
    openDate: str = Field(..., description="Account opening date")


class CreditReport(BaseModel):
    """Credit report data model."""
    
    creditScore: Optional[int] = Field(default=None, description="Credit score")
    accounts: List[CreditAccount] = Field(default=[], description="Credit accounts")
    totalAccounts: Optional[str] = Field(default="0", description="Total number of accounts")
    activeAccounts: Optional[str] = Field(default="0", description="Number of active accounts")
    outstandingBalance: Dict[str, Any] = Field(default={}, description="Outstanding balance details")


class MutualFundTransaction(BaseModel):
    """Mutual fund transaction model."""
    
    isin: str = Field(..., description="ISIN code")
    folioId: str = Field(..., description="Folio ID")
    type: str = Field(..., description="Transaction type (BUY/SELL)")
    date: str = Field(..., description="Transaction date")
    amount: float = Field(..., description="Transaction amount")
    units: float = Field(..., description="Number of units")
    nav: float = Field(..., description="Net Asset Value")
    schemeName: str = Field(..., description="Scheme name")


class EPFDetails(BaseModel):
    """EPF account details."""
    
    totalBalance: float = Field(..., description="Total EPF balance")
    employeeShare: float = Field(..., description="Employee contribution")
    employerShare: float = Field(..., description="Employer contribution")
    pensionBalance: Optional[float] = Field(default=0.0, description="Pension balance")
    employerDetails: List[Dict[str, Any]] = Field(default=[], description="Employer details")


class Asset(BaseModel):
    """Asset information."""
    
    type: str = Field(..., description="Asset type")
    value: float = Field(..., description="Asset value")
    formattedValue: str = Field(..., description="Formatted value")


class NetWorth(BaseModel):
    """Net worth data model."""
    
    totalNetWorth: float = Field(..., description="Total net worth")
    formattedTotalNetWorth: str = Field(..., description="Formatted net worth")
    currency: str = Field(default="INR", description="Currency")
    assets: List[Asset] = Field(default=[], description="Asset breakdown")
    mutualFunds: List[Dict[str, Any]] = Field(default=[], description="Mutual fund details")
    accountDetails: Dict[str, Any] = Field(default={}, description="Account details")


class ComprehensiveFinancialData(BaseModel):
    """Comprehensive financial profile."""
    
    phone_number: str = Field(..., description="User phone number")
    bank_transactions: List[BankTransaction] = Field(default=[], description="Bank transactions")
    credit_report: CreditReport = Field(..., description="Credit report")
    epf_details: EPFDetails = Field(..., description="EPF details")
    mf_transactions: List[MutualFundTransaction] = Field(default=[], description="Mutual fund transactions")
    net_worth: NetWorth = Field(..., description="Net worth data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class FinancialProfile(BaseModel):
    """Processed financial profile for agent analysis."""
    
    # Income Analysis
    monthly_income: float = Field(..., description="Monthly income")
    income_stability: str = Field(..., description="Income stability assessment")
    income_source: str = Field(..., description="Primary income source")
    
    # Expense Analysis
    monthly_expenses: float = Field(..., description="Monthly expenses")
    expense_categories: Dict[str, float] = Field(default={}, description="Expense breakdown")
    discretionary_income: float = Field(..., description="Discretionary income")
    
    # Asset Analysis
    total_assets: float = Field(..., description="Total assets")
    liquid_savings: float = Field(..., description="Liquid savings")
    investments: float = Field(..., description="Investment portfolio")
    retirement_savings: float = Field(..., description="Retirement savings")
    
    # Debt Analysis
    total_debt: float = Field(..., description="Total debt")
    credit_score: int = Field(..., description="Credit score")
    debt_to_income_ratio: float = Field(..., description="Debt to income ratio")
    
    # Investment Analysis
    portfolio_value: float = Field(..., description="Portfolio value")
    investment_schemes: int = Field(..., description="Number of investment schemes")
    portfolio_performance: str = Field(..., description="Portfolio performance assessment")
    
    # Risk Analysis
    emergency_fund_adequacy: str = Field(..., description="Emergency fund assessment")
    insurance_coverage: str = Field(..., description="Insurance coverage assessment")
    financial_stability_score: float = Field(..., description="Financial stability score")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 