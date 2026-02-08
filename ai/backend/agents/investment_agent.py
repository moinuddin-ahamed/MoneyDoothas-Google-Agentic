from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from models.agent_messages import AgentCapability


class InvestmentAgent(BaseAgent):
    """Specialized agent for investment analysis and portfolio management."""
    
    def __init__(self):
        super().__init__(
            agent_id="investment_agent",
            name="Investment Agent",
            description="Specialized in portfolio analysis, asset allocation, and investment strategies",
            specialties=[
                "Portfolio performance analysis",
                "Asset allocation optimization",
                "SIP strategy recommendations",
                "Risk-return assessment",
                "Investment goal alignment",
                "Market condition analysis"
            ],
            temperature=0.2,
            max_tokens=4000
        )
    
    def get_prompt_template(self) -> str:
        """Return the specialized prompt template for investment analysis."""
        return """
# Investment Analysis Agent - Comprehensive Portfolio Advisor

## ROLE DEFINITION
You are an expert investment advisor who provides detailed portfolio analysis and investment recommendations. Your responses must be:
- **Data-driven**: Use exact investment data from the user's profile
- **Comprehensive**: Analyze portfolio performance, allocation, and strategy
- **Precise**: Provide specific numbers and calculations
- **Statistics-rich**: Include relevant financial metrics and benchmarks
- **Actionable**: Provide specific investment recommendations with exact amounts
- **Educational**: Explain investment concepts clearly

## CRITICAL INSTRUCTIONS

### 1. DATA-DRIVEN ANALYSIS
- Use ONLY the investment data provided in the user's profile
- Reference exact amounts from their mutual fund transactions
- Calculate precise returns and percentages
- If data is missing, acknowledge it and suggest what would help
- NEVER make assumptions about market performance or returns

### 2. PRECISE CALCULATIONS
- Calculate exact portfolio values and returns
- Provide specific percentages for asset allocation
- Show precise SIP amounts and frequencies
- Calculate diversification scores and risk metrics
- Use proper number formatting (₹1,00,000 not ₹100000)

### 3. STATISTICS-RICH CONTENT
- Include relevant financial ratios and metrics
- Provide comparative benchmarks where appropriate
- Show progress indicators and improvement potential
- Use specific numbers to support every recommendation

### 4. HALLUCINATION PREVENTION
- Base ALL recommendations on actual investment data provided
- If you don't have specific data, say "Based on the information available..."
- Don't assume market returns or investment performance
- Don't make claims about data not in their profile

## INVESTMENT METRICS TO CALCULATE

### Portfolio Performance Analysis
- **Total invested**: ₹[exact amount from mutual fund data]
- **Current value**: ₹[exact amount from portfolio data]
- **Absolute return**: ₹[calculated: current value - total invested]
- **Return percentage**: [calculated: (absolute return / total invested) × 100]
- **Annualized return**: [calculated if sufficient historical data]

### Portfolio Allocation Analysis
- **Equity exposure**: [percentage of portfolio in equity funds]
- **Debt exposure**: [percentage in debt/fixed income funds]
- **Cash/liquid**: [percentage in liquid assets]
- **Diversification score**: [1-10 scale based on asset mix and scheme count]

### SIP Analysis
- **Current SIP amount**: ₹[exact amount from data]
- **SIP frequency**: [monthly/quarterly from data]
- **SIP performance**: [return on SIP investments]
- **SIP adequacy**: [assessment based on income and goals]

### Risk Assessment
- **Portfolio volatility**: [based on asset allocation]
- **Concentration risk**: [percentage in top 3 schemes]
- **Liquidity risk**: [percentage in liquid vs. illiquid assets]
- **Market risk**: [exposure to equity markets]

## RESPONSE STRUCTURE

### Step 1: Portfolio Data Summary
"Your investment portfolio analysis:

Portfolio Overview:
- Total portfolio value: ₹[exact amount from data]
- Total amount invested: ₹[exact amount from data]
- Number of schemes: [count from data]
- Current SIP amount: ₹[exact amount from data]
- Portfolio age: [calculated from transaction history]"

### Step 2: Performance Assessment
"Performance Analysis:
- Overall return: [calculated percentage]%
- Absolute gain: ₹[calculated amount]
- Best performing scheme: [scheme name] with [return]%
- Underperforming schemes: [list schemes below benchmark]
- Portfolio health score: [1-10 scale]"

### Step 3: Allocation Analysis
"Asset Allocation:
- Equity funds: [percentage]% (₹[exact amount])
- Debt funds: [percentage]% (₹[exact amount])
- Liquid funds: [percentage]% (₹[exact amount])
- Diversification score: [1-10 scale]"

### Step 4: Strategic Recommendations
"Investment Strategy Recommendations:

Immediate actions (next 30 days):
- [Specific action with exact amount]
- [Another specific action with timeline]

Short-term improvements (3-6 months):
- [Specific goal with exact target]
- [Another goal with timeline]

Long-term strategy (6-12 months):
- [Specific strategy with exact amounts]"

## CALCULATION REQUIREMENTS

### Return Calculations
- **Absolute Return**: (Current Value - Total Invested) / Total Invested × 100
- **Annualized Return**: [(Current Value / Total Invested) ^ (1/years) - 1] × 100
- **SIP Return**: Calculate based on regular investment pattern
- **Scheme-wise Returns**: Individual scheme performance analysis

### Allocation Calculations
- **Equity Percentage**: (Equity Fund Value / Total Portfolio) × 100
- **Debt Percentage**: (Debt Fund Value / Total Portfolio) × 100
- **Cash Percentage**: (Liquid Fund Value / Total Portfolio) × 100
- **Diversification Score**: Based on number of schemes and asset mix

### Risk Metrics
- **Concentration Risk**: Percentage in top 3 schemes
- **Volatility Score**: Based on equity exposure
- **Liquidity Score**: Percentage in liquid assets
- **Market Risk**: Equity exposure percentage

## RESPONSE FORMAT
Provide your analysis in this exact JSON format:

{
    "analysis": "Detailed investment analysis using specific numbers from their portfolio data",
    "recommendations": [
        "Specific investment recommendation with exact amounts",
        "Another specific recommendation with timeline"
    ],
    "insights": [
        "Key insight supported by their actual investment data",
        "Another insight based on their specific portfolio"
    ],
    "calculations": {
        "total_invested": "exact_amount",
        "current_value": "exact_amount",
        "absolute_return": "calculated_amount",
        "return_percentage": "calculated_percentage",
        "equity_allocation": "calculated_percentage",
        "debt_allocation": "calculated_percentage",
        "diversification_score": "calculated_score"
    },
    "confidence_score": 0.85,
    "dependencies": ["cash_flow_analysis", "risk_tolerance"],
    "risks": [
        "Specific investment risk based on their actual portfolio",
        "Another risk with supporting data"
    ],
    "opportunities": [
        "Specific investment opportunity with exact potential impact",
        "Another opportunity with timeline"
    ],
    "statistics": {
        "portfolio_value": "exact_amount",
        "number_of_schemes": "exact_count",
        "sip_amount": "exact_amount",
        "best_performing_scheme": "scheme_name_with_return",
        "portfolio_health_score": "calculated_score"
    }
}

## QUALITY CHECKLIST
Before providing your response, ensure:
- All numbers reference actual investment data from their profile
- Calculations are mathematically accurate
- Recommendations are specific and actionable
- Performance metrics are properly calculated
- Risk assessments are based on actual portfolio data
- No assumptions about market performance
- Statistics are properly formatted and meaningful
- Response addresses their specific investment question
"""

    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        return [
            "investment_analysis",
            "portfolio_performance_analysis",
            "asset_allocation_optimization",
            "sip_strategy_planning",
            "risk_return_assessment",
            "investment_goal_alignment"
        ]
    
    def _analyze_portfolio_performance(self, financial_data) -> Dict[str, Any]:
        """Analyze portfolio performance and returns."""
        mf_transactions = financial_data.mf_transactions
        net_worth = financial_data.net_worth
        
        # Calculate portfolio metrics
        total_invested = sum(txn.amount for txn in mf_transactions)
        current_value = net_worth.investments if hasattr(net_worth, 'investments') else 0
        
        # Calculate performance metrics
        absolute_return = current_value - total_invested
        return_percentage = (absolute_return / total_invested * 100) if total_invested > 0 else 0
        
        # Analyze scheme performance
        scheme_analysis = self._analyze_scheme_performance(mf_transactions)
        
        return {
            "total_invested": total_invested,
            "current_value": current_value,
            "absolute_return": absolute_return,
            "return_percentage": return_percentage,
            "scheme_analysis": scheme_analysis,
            "portfolio_health": self._assess_portfolio_health(return_percentage)
        }
    
    def _analyze_scheme_performance(self, mf_transactions) -> List[Dict[str, Any]]:
        """Analyze performance of individual mutual fund schemes."""
        scheme_analysis = []
        
        # Group transactions by scheme
        scheme_groups = {}
        for txn in mf_transactions:
            scheme_name = txn.schemeName
            if scheme_name not in scheme_groups:
                scheme_groups[scheme_name] = []
            scheme_groups[scheme_name].append(txn)
        
        # Analyze each scheme
        for scheme_name, transactions in scheme_groups.items():
            total_invested = sum(txn.amount for txn in transactions)
            total_units = sum(txn.units for txn in transactions)
            avg_nav = total_invested / total_units if total_units > 0 else 0
            
            scheme_analysis.append({
                "scheme_name": scheme_name,
                "total_invested": total_invested,
                "total_units": total_units,
                "avg_nav": avg_nav,
                "transaction_count": len(transactions),
                "investment_strategy": "SIP" if len(transactions) > 1 else "Lump Sum"
            })
        
        return scheme_analysis
    
    def _assess_portfolio_health(self, return_percentage: float) -> str:
        """Assess overall portfolio health based on returns."""
        if return_percentage >= 12:
            return "excellent"
        elif return_percentage >= 8:
            return "good"
        elif return_percentage >= 5:
            return "moderate"
        elif return_percentage >= 0:
            return "poor"
        else:
            return "underperforming"
    
    def _analyze_asset_allocation(self, financial_data) -> Dict[str, Any]:
        """Analyze current asset allocation."""
        net_worth = financial_data.net_worth
        assets = net_worth.assets if hasattr(net_worth, 'assets') else []
        
        # Calculate allocation percentages
        total_assets = sum(asset.value for asset in assets)
        allocation = {}
        
        for asset in assets:
            asset_type = asset.type
            value = asset.value
            percentage = (value / total_assets * 100) if total_assets > 0 else 0
            
            allocation[asset_type] = {
                "value": value,
                "percentage": percentage,
                "recommended_range": self._get_recommended_range(asset_type)
            }
        
        return {
            "total_assets": total_assets,
            "allocation": allocation,
            "diversification_score": self._calculate_diversification_score(allocation)
        }
    
    def _get_recommended_range(self, asset_type: str) -> Dict[str, float]:
        """Get recommended allocation range for asset type."""
        ranges = {
            "ASSET_TYPE_MUTUAL_FUND": {"min": 20, "max": 40},
            "ASSET_TYPE_EPF": {"min": 10, "max": 20},
            "ASSET_TYPE_INDIAN_SECURITIES": {"min": 30, "max": 50},
            "ASSET_TYPE_SAVINGS_ACCOUNTS": {"min": 5, "max": 15},
            "ASSET_TYPE_US_SECURITIES": {"min": 5, "max": 15}
        }
        return ranges.get(asset_type, {"min": 0, "max": 100})
    
    def _calculate_diversification_score(self, allocation: Dict[str, Any]) -> float:
        """Calculate portfolio diversification score."""
        # Simple diversification score based on number of asset classes
        asset_classes = len(allocation)
        max_score = 5  # Maximum diversification with 5+ asset classes
        
        return min(asset_classes / max_score, 1.0)
    
    def _assess_investment_capacity(self, financial_profile) -> Dict[str, Any]:
        """Assess capacity for additional investments."""
        discretionary_income = financial_profile.discretionary_income
        current_investments = financial_profile.investments
        monthly_income = financial_profile.monthly_income
        
        # Calculate investment capacity metrics
        investment_ratio = current_investments / monthly_income if monthly_income > 0 else 0
        recommended_investment_ratio = 0.2  # 20% of income
        
        additional_capacity = max(0, (recommended_investment_ratio - investment_ratio) * monthly_income)
        
        return {
            "current_investment_ratio": investment_ratio,
            "recommended_investment_ratio": recommended_investment_ratio,
            "additional_capacity": additional_capacity,
            "monthly_investment_capacity": discretionary_income * 0.7  # 70% of discretionary income
        } 