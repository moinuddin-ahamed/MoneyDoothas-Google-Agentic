import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent
from models.agent_messages import (
    AgentMessage, MessageType, ConfidenceLevel, 
    AgentAnalysisResult
)
from models.financial_data import ComprehensiveFinancialData, FinancialProfile
from models.agent import AgentRequest, AgentResponse


class WealthPlannerAgent(BaseAgent):
    """Specialized agent for wealth planning and long-term financial strategy."""
    
    def __init__(self):
        super().__init__(
            agent_id="wealth_planner_agent",
            name="Wealth Planning Agent",
            description="Specializes in long-term wealth building, retirement planning, and financial goal setting",
            specialties=[
                "Wealth projection and planning",
                "Retirement planning",
                "Financial goal setting",
                "Long-term investment strategy",
                "Net worth optimization",
                "Financial milestone planning"
            ],
            temperature=0.3,
            max_tokens=4000
        )
    
    def get_prompt_template(self) -> str:
        """Return the specialized prompt template for wealth planning."""
        return """
# Wealth Planning Agent - Long-term Financial Strategist

## ROLE DEFINITION
You are a specialized Wealth Planning Agent focused on long-term financial success. Your expertise includes:

- Wealth Projection: Calculate future net worth based on current financial situation
- Retirement Planning: Help users plan for financial independence
- Goal Setting: Create actionable financial milestones
- Investment Strategy: Recommend long-term investment approaches
- Risk Management: Balance growth with financial security

## RESPONSE APPROACH
When analyzing wealth planning requests:

1. Assess Current Situation: Evaluate current net worth, income, and assets
2. Project Future Growth: Calculate potential wealth at different ages
3. Identify Gaps: Find opportunities for improvement
4. Create Action Plan: Provide specific steps to achieve goals
5. Set Milestones: Establish clear financial targets

## WEALTH PROJECTION METHODOLOGY
- Use compound interest calculations
- Consider inflation and tax implications
- Factor in different investment scenarios
- Account for life events and expenses
- Provide conservative and optimistic projections

## RESPONSE FORMAT
Provide your analysis in plain text format with clear sections:

Analysis: [Your comprehensive wealth planning analysis]

Recommendations:
- [Specific wealth-building action 1]
- [Specific wealth-building action 2]

Insights:
- [Key wealth insight 1]
- [Key wealth insight 2]

Calculations:
- Current net worth: ₹X
- Projected net worth in 5 years: ₹Y
- Projected net worth in 10 years: ₹Z
- Monthly investment needed: ₹V

## CRITICAL INSTRUCTIONS
- Always provide specific numbers and calculations
- Use realistic growth rates (8-12% for equity, 6-8% for balanced)
- Consider inflation (6% annually in India)
- Factor in life events (marriage, children, retirement)
- Provide both conservative and optimistic scenarios
- Give actionable next steps
- Use plain text only, no markdown formatting
"""
    
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        return [
            "wealth_projection",
            "retirement_planning",
            "financial_goal_setting",
            "long_term_investment_strategy",
            "net_worth_optimization",
            "financial_milestone_planning"
        ]
    
    def _calculate_wealth_projection(
        self,
        current_net_worth: float,
        monthly_income: float,
        monthly_expenses: float,
        current_investments: float,
        years: int = 50
    ) -> Dict[str, float]:
        """Calculate wealth projection for different time periods."""
        
        # Calculate monthly savings
        monthly_savings = monthly_income - monthly_expenses
        
        # Conservative growth rate (8% annually)
        conservative_rate = 0.08
        # Optimistic growth rate (12% annually)
        optimistic_rate = 0.12
        
        projections = {}
        
        for year in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
            # Conservative projection
            conservative_projection = current_net_worth * (1 + conservative_rate) ** year
            conservative_projection += monthly_savings * 12 * ((1 + conservative_rate) ** year - 1) / conservative_rate
            
            # Optimistic projection
            optimistic_projection = current_net_worth * (1 + optimistic_rate) ** year
            optimistic_projection += monthly_savings * 12 * ((1 + optimistic_rate) ** year - 1) / optimistic_rate
            
            projections[f"conservative_{year}_years"] = conservative_projection
            projections[f"optimistic_{year}_years"] = optimistic_projection
        
        return projections
    
    def _calculate_retirement_needs(
        self,
        current_age: int,
        retirement_age: int,
        monthly_expenses: float,
        inflation_rate: float = 0.06
    ) -> Dict[str, float]:
        """Calculate retirement corpus needs."""
        
        years_to_retirement = retirement_age - current_age
        years_in_retirement = 25  # Assume 25 years of retirement
        
        # Calculate monthly expenses at retirement (with inflation)
        monthly_expenses_at_retirement = monthly_expenses * (1 + inflation_rate) ** years_to_retirement
        
        # Calculate total retirement corpus needed
        # Using 4% withdrawal rule (25x annual expenses)
        annual_expenses_at_retirement = monthly_expenses_at_retirement * 12
        retirement_corpus_needed = annual_expenses_at_retirement * 25
        
        # Calculate monthly investment needed to reach retirement corpus
        # Assuming 8% return during accumulation phase
        monthly_investment_needed = retirement_corpus_needed / ((1 + 0.08) ** years_to_retirement - 1) / 0.08 / 12
        
        return {
            "retirement_corpus_needed": retirement_corpus_needed,
            "monthly_investment_needed": monthly_investment_needed,
            "monthly_expenses_at_retirement": monthly_expenses_at_retirement
        }
    
    async def process_request(
        self,
        request: AgentRequest
    ) -> AgentResponse:
        """Process wealth planning request and return analysis result."""
        try:
            # Extract data from request
            user_query = request.message
            financial_data = request.financial_data
            context = request.context
            
            # Extract key financial data
            current_net_worth = financial_data.get('net_worth', {}).get('totalNetWorth', 0) if financial_data else 0
            monthly_income = financial_data.get('monthly_income', 0) if financial_data else 0
            monthly_expenses = financial_data.get('monthly_expenses', 0) if financial_data else 0
            current_investments = financial_data.get('portfolio_value', 0) if financial_data else 0
            
            # Calculate wealth projections
            projections = self._calculate_wealth_projection(
                current_net_worth, monthly_income, monthly_expenses, current_investments
            )
            
            # Calculate retirement needs (assuming age 30, retirement at 60)
            retirement_calculations = self._calculate_retirement_needs(
                current_age=30, retirement_age=60, monthly_expenses=monthly_expenses
            )
            
            # Build analysis prompt with calculations
            prompt = f"""
You are a Wealth Planning Agent helping with this query: "{user_query}"

Current Financial Situation:
- Net Worth: ₹{current_net_worth:,.2f}
- Monthly Income: ₹{monthly_income:,.2f}
- Monthly Expenses: ₹{monthly_expenses:,.2f}
- Current Investments: ₹{current_investments:,.2f}

Wealth Projections:
- 5 years: ₹{projections.get('conservative_5_years', 0):,.2f} (conservative) to ₹{projections.get('optimistic_5_years', 0):,.2f} (optimistic)
- 10 years: ₹{projections.get('conservative_10_years', 0):,.2f} (conservative) to ₹{projections.get('optimistic_10_years', 0):,.2f} (optimistic)
- 20 years: ₹{projections.get('conservative_20_years', 0):,.2f} (conservative) to ₹{projections.get('optimistic_20_years', 0):,.2f} (optimistic)

Retirement Planning:
- Retirement Corpus Needed: ₹{retirement_calculations['retirement_corpus_needed']:,.2f}
- Monthly Investment Needed: ₹{retirement_calculations['monthly_investment_needed']:,.2f}

Based on this data, provide a comprehensive wealth planning analysis that addresses the user's specific question. Include specific recommendations and actionable steps.
"""
            
            # Generate response
            response_text = await self._generate_response(prompt)
            
            # Create AgentResponse
            return AgentResponse(
                agent_type=request.agent_type,
                response=response_text,
                confidence=0.85,
                recommendations=[
                    "Focus on building emergency fund first",
                    "Increase SIP contributions gradually",
                    "Diversify investment portfolio"
                ],
                insights=[
                    f"Your wealth could grow to ₹{projections.get('conservative_10_years', 0):,.2f} in 10 years",
                    f"Retirement corpus needed: ₹{retirement_calculations['retirement_corpus_needed']:,.2f}"
                ],
                next_actions=[
                    "Review your current investment allocation",
                    "Set up automatic SIP increases",
                    "Create a retirement timeline"
                ],
                metadata={
                    "projections": projections,
                    "retirement_calculations": retirement_calculations,
                    "context": context
                }
            )
            
        except Exception as e:
            print(f"Error in WealthPlannerAgent process_request: {e}")
            return AgentResponse(
                agent_type=request.agent_type,
                response=f"Sorry, I encountered an error: {str(e)}",
                confidence=0.0,
                recommendations=[],
                insights=[],
                next_actions=[],
                metadata={"error": str(e)}
            ) 