from typing import List, Dict, Any
from models.agent import AgentType, AgentCapability
from .base_agent import BaseAgent


class WealthPlanningAgent(BaseAgent):
    """Wealth Planning Agent - Specialized in net worth analysis and long-term planning."""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.WEALTH_PLANNER,
            name="Wealth Planning Agent",
            description="Specialized agent for net worth analysis, wealth projections, and long-term financial planning.",
            temperature=0.3,  # Slightly higher for creative planning
            max_tokens=4000
        )
    
    def get_prompt_template(self) -> str:
        return """
You are a Wealth Planning Agent. Give short, specific wealth advice using the user's actual financial data.

When someone asks about wealth planning, respond like this:

"Looking at your wealth situation:
- Current net worth: [specific amount from data]
- Monthly income: [specific amount]
- Age: [from data]

For your wealth question:
- [Specific answer based on their data]
- [One clear projection or recommendation]

My advice:
- [One specific action step]

[One encouraging sentence]"

Keep responses under 150 words. Use actual numbers from their financial data. No bullet points or formatting."
"""
    
    def get_capabilities(self) -> List[str]:
        return [
            AgentCapability.WEALTH_PROJECTION,
            AgentCapability.GOAL_PLANNING
        ]
    
    def _analyze_net_worth_data(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze net worth data and extract key insights."""
        analysis = {
            'current_net_worth': 0,
            'total_assets': 0,
            'total_liabilities': 0,
            'asset_allocation': {},
            'wealth_growth_rate': 0,
            'projections': {},
            'recommendations': []
        }
        
        if not financial_data:
            return analysis
        
        # Extract net worth data from the actual API structure
        net_worth_data = financial_data.get('net_worth', {})
        if not net_worth_data:
            # Try to get from the root level (actual API structure)
            analysis['current_net_worth'] = financial_data.get('totalNetWorth', 0)
            analysis['total_assets'] = financial_data.get('totalNetWorth', 0)  # Assuming no liabilities for now
            analysis['total_liabilities'] = 0
            
            # Extract asset allocation from the assets array
            assets = financial_data.get('assets', [])
            asset_allocation = {}
            for asset in assets:
                asset_type = asset.get('type', 'UNKNOWN')
                value = asset.get('value', 0)
                if asset_type not in asset_allocation:
                    asset_allocation[asset_type] = 0
                asset_allocation[asset_type] += value
            
            analysis['asset_allocation'] = asset_allocation
        else:
            # Fallback to old structure
            analysis['current_net_worth'] = net_worth_data.get('net_worth', 0)
            analysis['total_assets'] = net_worth_data.get('total_assets', 0)
            analysis['total_liabilities'] = net_worth_data.get('total_liabilities', 0)
            analysis['asset_allocation'] = net_worth_data.get('assets_breakdown', {})
        
        # Calculate wealth growth rate (simplified - would need historical data for accurate calculation)
        analysis['wealth_growth_rate'] = 8.0  # Assumed 8% annual growth
        
        # Generate projections
        current_age = financial_data.get('user_age', 30)
        current_net_worth = analysis['current_net_worth']
        
        for target_age in [35, 40, 45, 50, 60]:
            years_to_target = target_age - current_age
            if years_to_target > 0:
                projected_net_worth = current_net_worth * (1.08 ** years_to_target)
                analysis['projections'][target_age] = projected_net_worth
        
        return analysis
    
    def _calculate_retirement_readiness(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate retirement readiness metrics."""
        current_age = financial_data.get('user_age', 30)
        
        # Get current net worth from the correct structure
        current_net_worth = 0
        if financial_data.get('totalNetWorth'):
            current_net_worth = financial_data.get('totalNetWorth', 0)
        else:
            current_net_worth = financial_data.get('net_worth', {}).get('net_worth', 0)
        
        monthly_income = financial_data.get('monthly_income', 0)
        
        # Simple retirement calculation
        retirement_age = 60
        years_to_retirement = retirement_age - current_age
        annual_income_needed = monthly_income * 12 * 0.8  # 80% of current income
        retirement_corpus_needed = annual_income_needed * 25  # 25x annual income rule
        
        # Project current savings to retirement
        projected_savings = current_net_worth * (1.08 ** years_to_retirement)
        
        # Calculate shortfall
        shortfall = max(0, retirement_corpus_needed - projected_savings)
        
        # Calculate readiness percentage safely
        readiness_percentage = 0
        if retirement_corpus_needed > 0:
            readiness_percentage = min(100, (projected_savings / retirement_corpus_needed) * 100)
        
        return {
            'retirement_age': retirement_age,
            'years_to_retirement': years_to_retirement,
            'annual_income_needed': annual_income_needed,
            'retirement_corpus_needed': retirement_corpus_needed,
            'projected_savings': projected_savings,
            'shortfall': shortfall,
            'readiness_percentage': readiness_percentage
        }
    
    def _build_prompt(self, request) -> str:
        """Override to include wealth-specific analysis."""
        template = self.get_prompt_template()
        
        # Analyze net worth data
        net_worth_analysis = self._analyze_net_worth_data(request.financial_data)
        
        # Calculate retirement readiness
        retirement_analysis = self._calculate_retirement_readiness(request.financial_data)
        
        # Add wealth analysis to the prompt
        enhanced_template = template + f"""

**Net Worth Analysis Summary**:
- Current Net Worth: ₹{net_worth_analysis['current_net_worth']:,.2f}
- Total Assets: ₹{net_worth_analysis['total_assets']:,.2f}
- Total Liabilities: ₹{net_worth_analysis['total_liabilities']:,.2f}
- Asset Allocation: {net_worth_analysis['asset_allocation']}
- Wealth Growth Rate: {net_worth_analysis['wealth_growth_rate']:.1f}%

**Wealth Projections**:
{chr(10).join([f"- Age {age}: ₹{amount:,.2f}" for age, amount in net_worth_analysis['projections'].items()])}

**Retirement Readiness**:
- Years to Retirement: {retirement_analysis['years_to_retirement']}
- Retirement Corpus Needed: ₹{retirement_analysis['retirement_corpus_needed']:,.2f}
- Projected Savings: ₹{retirement_analysis['projected_savings']:,.2f}
- Readiness: {retirement_analysis['readiness_percentage']:.1f}%

Use this analysis to provide specific, actionable wealth planning advice.
"""
        
        # Extract context
        context = self._extract_context(request)
        
        # Build the prompt using string replacement
        prompt = enhanced_template.replace("{user_message}", str(request.message))
        prompt = prompt.replace("{context}", str(context))
        prompt = prompt.replace("{financial_data}", str(self._format_financial_data(request.financial_data)))
        prompt = prompt.replace("{conversation_history}", str(self._format_conversation_history(request.conversation_history)))
        
        return prompt 