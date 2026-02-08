from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class AccountType(str, Enum):
    """Types of financial accounts."""
    SAVINGS = "savings"
    CURRENT = "current"
    FIXED_DEPOSIT = "fixed_deposit"
    MUTUAL_FUND = "mutual_fund"
    STOCKS = "stocks"
    EPF = "epf"
    PPF = "ppf"
    CREDIT_CARD = "credit_card"
    LOAN = "loan"
    INSURANCE = "insurance"


class TransactionType(str, Enum):
    """Types of financial transactions."""
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER = "transfer"
    INVESTMENT = "investment"
    WITHDRAWAL = "withdrawal"


class InvestmentData(BaseModel):
    """Investment portfolio data."""
    
    account_id: str = Field(..., description="Account identifier")
    account_name: str = Field(..., description="Account name")
    account_type: AccountType = Field(..., description="Type of account")
    balance: float = Field(..., description="Current balance")
    currency: str = Field(default="INR", description="Currency")
    returns: Optional[float] = Field(default=None, description="Returns percentage")
    risk_level: Optional[str] = Field(default=None, description="Risk level")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class DebtData(BaseModel):
    """Debt and liability data."""
    
    account_id: str = Field(..., description="Account identifier")
    account_name: str = Field(..., description="Account name")
    account_type: AccountType = Field(..., description="Type of account")
    outstanding_amount: float = Field(..., description="Outstanding debt amount")
    interest_rate: float = Field(..., description="Interest rate percentage")
    monthly_payment: float = Field(..., description="Monthly payment amount")
    remaining_tenure: int = Field(..., description="Remaining tenure in months")
    currency: str = Field(default="INR", description="Currency")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class NetWorthData(BaseModel):
    """Net worth calculation data."""
    
    user_id: str = Field(..., description="User identifier")
    total_assets: float = Field(..., description="Total assets value")
    total_liabilities: float = Field(..., description="Total liabilities value")
    net_worth: float = Field(..., description="Net worth (assets - liabilities)")
    currency: str = Field(default="INR", description="Currency")
    calculation_date: datetime = Field(default_factory=datetime.utcnow, description="Calculation date")
    assets_breakdown: Dict[str, float] = Field(default={}, description="Breakdown of assets")
    liabilities_breakdown: Dict[str, float] = Field(default={}, description="Breakdown of liabilities")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class FinancialData(BaseModel):
    """Complete financial data for a user."""
    
    user_id: str = Field(..., description="User identifier")
    investments: List[InvestmentData] = Field(default=[], description="Investment accounts")
    debts: List[DebtData] = Field(default=[], description="Debt accounts")
    net_worth: NetWorthData = Field(..., description="Net worth data")
    credit_score: Optional[int] = Field(default=None, description="Credit score")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 