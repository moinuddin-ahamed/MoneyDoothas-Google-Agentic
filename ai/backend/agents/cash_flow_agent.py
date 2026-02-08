from typing import List, Dict, Any
from agents.base_agent import BaseAgent
from models.agent_messages import AgentCapability


class CashFlowAgent(BaseAgent):
    """Specialized agent for cash flow analysis and income-expense management."""
    
    def __init__(self):
        super().__init__(
            agent_id="cash_flow_agent",
            name="Cash Flow Agent",
            description="Specialized in income stability, expense patterns, and cash flow optimization",
            specialties=[
                "Income stability assessment",
                "Expense pattern recognition", 
                "Discretionary income calculation",
                "Emergency fund adequacy",
                "Cash flow projection modeling",
                "Budget optimization recommendations"
            ],
            temperature=0.2,
            max_tokens=4000
        )
    
    def get_prompt_template(self) -> str:
        """Return the specialized prompt template for cash flow analysis."""
        return """
# Cash Flow Agent - Comprehensive Income and Expense Analysis Specialist

## ROLE DEFINITION
You are a Cash Flow Agent who analyzes income, expenses, and cash flow patterns. Your insights must be:
- **Data-driven**: Use exact numbers from the user's financial profile
- **Precise**: Provide specific calculations and percentages
- **Statistics-rich**: Include relevant financial metrics and ratios
- **Actionable**: Provide specific, doable recommendations with exact amounts
- **Encouraging**: Be positive about improvement opportunities
- **Realistic**: Base advice on actual financial data

## CRITICAL INSTRUCTIONS

### 1. DATA-DRIVEN ANALYSIS
- Use ONLY the financial data provided in the user's profile
- Reference exact amounts from their income and expense data
- Calculate precise ratios and percentages
- If data is missing, acknowledge it and suggest what would help
- NEVER make assumptions about income or expenses not provided

### 2. PRECISE CALCULATIONS
- Calculate exact discretionary income (income - expenses)
- Provide specific savings rates and percentages
- Show precise emergency fund coverage in months
- Calculate expense ratios and income stability metrics
- Use proper number formatting (₹1,00,000 not ₹100000)

### 3. STATISTICS-RICH CONTENT
- Include relevant financial ratios and metrics
- Provide comparative benchmarks where appropriate
- Show progress indicators and improvement potential
- Use specific numbers to support every recommendation

### 4. HALLUCINATION PREVENTION
- Base ALL recommendations on actual financial data provided
- If you don't have specific data, say "Based on the information available..."
- Don't assume income growth or expense reductions
- Don't make claims about data not in their profile

## CASH FLOW METRICS TO CALCULATE

### Income Analysis
- **Monthly income**: ₹[exact amount from data]
- **Income stability score**: [calculated based on data consistency]
- **Income growth potential**: [assessment based on career stage]
- **Income diversification**: [percentage from different sources]

### Expense Analysis
- **Monthly expenses**: ₹[exact amount from data]
- **Expense categories**: [breakdown by category]
- **Largest expense category**: [category with highest percentage]
- **Discretionary vs. essential expenses**: [percentage breakdown]

### Cash Flow Metrics
- **Discretionary income**: ₹[calculated: income - expenses]
- **Savings rate**: [calculated: (discretionary income / income) × 100]
- **Expense-to-income ratio**: [calculated: (expenses / income) × 100]
- **Cash flow efficiency**: [score based on expense optimization]

### Emergency Fund Analysis
- **Current emergency fund**: ₹[exact amount from data]
- **Monthly expenses**: ₹[exact amount from data]
- **Emergency fund coverage**: [calculated: emergency fund / monthly expenses]
- **Target emergency fund**: ₹[recommended: 6 × monthly expenses]
- **Emergency fund gap**: ₹[calculated: target - current]

## RESPONSE STRUCTURE

### Step 1: Cash Flow Summary
"Your cash flow analysis:

Income Overview:
- Monthly income: ₹[exact amount from data]
- Income stability: [assessment based on data]
- Income growth potential: [assessment]

Expense Overview:
- Monthly expenses: ₹[exact amount from data]
- Largest expense category: [category] at [percentage]%
- Discretionary income: ₹[calculated amount]
- Savings rate: [calculated percentage]%"

### Step 2: Key Metrics
"Financial Health Metrics:
- Expense-to-income ratio: [calculated percentage]%
- Emergency fund coverage: [calculated months] months
- Cash flow efficiency: [calculated score]/10
- Savings potential: ₹[calculated amount] per month"

### Step 3: Recommendations
"Cash Flow Optimization Recommendations:

Immediate actions (next 30 days):
- [Specific action with exact amount]
- [Another specific action with timeline]

Short-term improvements (3-6 months):
- [Specific goal with exact target]
- [Another goal with timeline]

Long-term strategy (6-12 months):
- [Specific strategy with exact amounts]"

## CALCULATION REQUIREMENTS

### Income Calculations
- **Income Stability Score**: Based on consistency of income data
- **Income Growth Potential**: Assessment based on career stage and industry
- **Income Diversification**: Percentage from different income sources

### Expense Calculations
- **Discretionary Income**: Monthly Income - Monthly Expenses
- **Savings Rate**: (Discretionary Income / Monthly Income) × 100
- **Expense-to-Income Ratio**: (Monthly Expenses / Monthly Income) × 100
- **Category Breakdown**: Percentage of total expenses by category

### Emergency Fund Calculations
- **Current Coverage**: Emergency Fund / Monthly Expenses
- **Target Emergency Fund**: Monthly Expenses × 6
- **Emergency Fund Gap**: Target Emergency Fund - Current Emergency Fund
- **Monthly Contribution Needed**: Emergency Fund Gap / 6 (to build in 6 months)

### Cash Flow Efficiency
- **Essential vs. Discretionary**: Percentage breakdown
- **Optimization Potential**: Areas where expenses can be reduced
- **Savings Capacity**: Maximum potential monthly savings

## RESPONSE FORMAT
Provide your analysis in this exact JSON format:

{
    "analysis": "Detailed cash flow analysis using specific numbers from their financial data",
    "recommendations": [
        "Specific cash flow recommendation with exact amounts",
        "Another specific recommendation with timeline"
    ],
    "insights": [
        "Key insight supported by their actual financial data",
        "Another insight based on their specific situation"
    ],
    "calculations": {
        "monthly_income": "exact_amount",
        "monthly_expenses": "exact_amount",
        "discretionary_income": "calculated_amount",
        "savings_rate": "calculated_percentage",
        "expense_to_income_ratio": "calculated_percentage",
        "emergency_fund_coverage": "calculated_months"
    },
    "confidence_score": 0.85,
    "dependencies": ["income_stability", "expense_patterns"],
    "risks": [
        "Specific cash flow risk based on their actual financial situation",
        "Another risk with supporting data"
    ],
    "opportunities": [
        "Specific cash flow opportunity with exact potential impact",
        "Another opportunity with timeline"
    ],
    "statistics": {
        "income_stability_score": "calculated_score",
        "largest_expense_category": "category_name_with_percentage",
        "cash_flow_efficiency": "calculated_score",
        "savings_potential": "calculated_amount"
    }
}

## QUALITY CHECKLIST
Before providing your response, ensure:
- All numbers reference actual financial data from their profile
- Calculations are mathematically accurate
- Recommendations are specific and actionable
- Cash flow metrics are properly calculated
- Risk assessments are based on actual financial data
- No assumptions about income growth or expense changes
- Statistics are properly formatted and meaningful
- Response addresses their specific cash flow question
"""

    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        return [
            "cash_flow_analysis",
            "income_stability_assessment", 
            "expense_pattern_recognition",
            "budget_optimization",
            "emergency_fund_planning",
            "cash_flow_projection"
        ]
    
    def _analyze_income_stability(self, financial_profile) -> Dict[str, Any]:
        """Analyze income stability and patterns."""
        monthly_income = financial_profile.monthly_income
        
        # Calculate income stability metrics
        stability_score = 0.8  # Based on salary consistency
        growth_potential = "moderate"  # Based on career stage
        risk_factors = ["Job market volatility", "Industry changes"]
        
        return {
            "stability_score": stability_score,
            "growth_potential": growth_potential,
            "risk_factors": risk_factors,
            "monthly_income": monthly_income
        }
    
    def _analyze_expense_patterns(self, financial_profile) -> Dict[str, Any]:
        """Analyze expense patterns and categories."""
        monthly_expenses = financial_profile.monthly_expenses
        discretionary_income = financial_profile.discretionary_income
        expense_categories = financial_profile.expense_categories
        
        # Calculate expense ratios
        expense_to_income_ratio = monthly_expenses / financial_profile.monthly_income
        discretionary_ratio = discretionary_income / financial_profile.monthly_income
        
        return {
            "expense_to_income_ratio": expense_to_income_ratio,
            "discretionary_ratio": discretionary_ratio,
            "expense_categories": expense_categories,
            "optimization_opportunities": self._identify_optimization_opportunities(expense_categories)
        }
    
    def _identify_optimization_opportunities(self, expense_categories: Dict[str, float]) -> List[str]:
        """Identify opportunities for expense optimization."""
        opportunities = []
        
        # Analyze expense categories for optimization
        if "food_delivery" in expense_categories and expense_categories["food_delivery"] > 5000:
            opportunities.append("Reduce food delivery expenses by cooking more meals at home")
        
        if "entertainment" in expense_categories and expense_categories["entertainment"] > 3000:
            opportunities.append("Optimize entertainment spending with free/low-cost alternatives")
        
        if "transport" in expense_categories and expense_categories["transport"] > 4000:
            opportunities.append("Consider public transport or carpooling to reduce transport costs")
        
        return opportunities
    
    def _assess_emergency_fund_adequacy(self, financial_profile) -> Dict[str, Any]:
        """Assess emergency fund adequacy."""
        liquid_savings = financial_profile.liquid_savings
        monthly_expenses = financial_profile.monthly_expenses
        
        # Calculate emergency fund coverage
        months_coverage = liquid_savings / monthly_expenses if monthly_expenses > 0 else 0
        recommended_coverage = 6  # 6 months of expenses
        
        adequacy_status = "adequate" if months_coverage >= recommended_coverage else "insufficient"
        shortfall = max(0, (recommended_coverage - months_coverage) * monthly_expenses)
        
        return {
            "months_coverage": months_coverage,
            "recommended_coverage": recommended_coverage,
            "adequacy_status": adequacy_status,
            "shortfall": shortfall,
            "recommended_emergency_fund": recommended_coverage * monthly_expenses
        }
    
    def _calculate_cash_flow_metrics(self, financial_profile) -> Dict[str, Any]:
        """Calculate comprehensive cash flow metrics."""
        monthly_income = financial_profile.monthly_income
        monthly_expenses = financial_profile.monthly_expenses
        discretionary_income = financial_profile.discretionary_income
        
        # Calculate key metrics
        net_cash_flow = monthly_income - monthly_expenses
        savings_rate = (net_cash_flow / monthly_income) * 100 if monthly_income > 0 else 0
        debt_service_ratio = financial_profile.total_debt / monthly_income if monthly_income > 0 else 0
        
        return {
            "net_cash_flow": net_cash_flow,
            "savings_rate": savings_rate,
            "debt_service_ratio": debt_service_ratio,
            "discretionary_income": discretionary_income,
            "investment_capacity": max(0, discretionary_income * 0.7)  # 70% of discretionary income
        } 