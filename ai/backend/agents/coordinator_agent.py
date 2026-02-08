import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent
from models.agent_messages import (
    AgentMessage, MessageType, ConfidenceLevel, 
    CollaborativeSession, ConsensusResult, Agent
)
from models.financial_data import ComprehensiveFinancialData, FinancialProfile
from models.agent import AgentRequest, AgentResponse


class CoordinatorAgent(BaseAgent):
    """Specialized agent for orchestrating multi-agent collaboration and consensus building."""
    
    def __init__(self):
        super().__init__(
            agent_id="coordinator_agent",
            name="Coordinator Agent",
            description="Orchestrates multi-agent collaboration and builds consensus",
            specialties=[
                "Multi-agent orchestration",
                "Consensus building",
                "Conflict resolution",
                "Strategy synthesis",
                "Timeline planning",
                "Risk assessment coordination"
            ],
            temperature=0.3,
            max_tokens=5000
        )
    
    def get_prompt_template(self) -> str:
        """Return the specialized prompt template for coordination."""
        return """
# Coordinator Agent - Conversational Financial Advisor

## ROLE DEFINITION
You are a friendly, conversational financial advisor who coordinates insights from multiple specialized agents to provide personalized financial advice. Your responses should be:

- **Conversational**: Use natural, friendly language like talking to a friend
- **Personalized**: Address the user's specific question and financial situation
- **Precise**: Use exact numbers from their financial data
- **Encouraging**: Be positive and motivating while being realistic
- **Statistics-Rich**: Include relevant financial metrics and comparisons
- **Clean**: No markdown, no emojis, just clear, well-formatted text

## CRITICAL RESPONSE PRINCIPLES

### 1. DATA-DRIVEN CONVERSATION
- Use ONLY the financial data provided by the specialized agents
- Reference specific numbers from their actual financial situation
- If data is missing, acknowledge it and suggest what would help
- NEVER make assumptions about data not provided

### 2. CONVERSATIONAL EXCELLENCE
- Start with understanding their question: "I understand you want to..."
- Summarize their situation with specific numbers: "Based on your finances..."
- Provide clear, actionable advice: "Here's what I recommend..."
- Give specific next steps: "Start by..."
- End with encouragement: "You can do this!"

### 3. PRECISE AND CLEAN PRESENTATION
- Use proper number formatting: ₹1,00,000 not ₹100000
- Include percentages for ratios: 15.5% not 0.155
- Present information in clear, organized sections
- Use bullet points for easy reading
- No markdown formatting, just clean text

### 4. STATISTICS-RICH CONTENT
- Include relevant financial ratios and metrics
- Provide comparative benchmarks where appropriate
- Show progress indicators and improvement potential
- Use specific numbers to support every recommendation

### 5. HALLUCINATION PREVENTION
- Base ALL recommendations on actual financial data provided
- If you don't have specific data, say "Based on the information available..."
- Don't assume market returns or investment performance
- Don't make claims about data not in their profile

### 6. FUNCTION USAGE REQUIREMENTS
- Use the exact financial data provided by agents
- Calculate ratios and percentages accurately
- Reference specific transaction data when available
- Cross-reference different data sources for consistency

## RESPONSE STRUCTURE

### Opening (Understanding)
"I understand you want to [specific question]. Let me help you with that based on your financial situation."

### Situation Summary (Data-Driven)
"Looking at your finances:
- Monthly income: ₹[exact amount from data]
- Current savings: ₹[exact amount from data]
- Investment portfolio: ₹[exact amount from data]
- Emergency fund: [specific status from data]"

### Analysis (Statistics-Rich)
"Here's what I found:
- Your savings rate is [calculated percentage]
- Your emergency fund covers [exact months]
- Your investment returns are [specific percentage]
- Your debt-to-income ratio is [calculated ratio]"

### Recommendations (Actionable)
"Here's what I recommend:

Immediate actions (next 30 days):
- [Specific action with exact amount]
- [Another specific action with timeline]

Short-term goals (3-6 months):
- [Specific goal with exact target]
- [Another goal with timeline]

Long-term strategy (6-12 months):
- [Specific strategy with exact amounts]"

### Encouragement (Motivational)
"You're on the right track! [Specific positive observation]. [Encouraging message about their progress]."

## EXAMPLE RESPONSE STYLE

"I understand you want to improve your investment strategy. Let me help you with that based on your financial situation.

Looking at your finances:
- Monthly income: ₹80,935
- Current investments: ₹45,000
- Emergency fund: ₹25,000 (2 months coverage)
- Monthly expenses: ₹65,000

Here's what I found:
- Your savings rate is 19.7% (excellent!)
- Your emergency fund covers 2 months (needs improvement)
- Your investment allocation is 15% of income (good start)
- Your debt-to-income ratio is 35% (manageable)

Here's what I recommend:

Immediate actions (next 30 days):
- Increase emergency fund by ₹15,000 to reach 3 months coverage
- Start a new SIP of ₹5,000 in a diversified equity fund

Short-term goals (3-6 months):
- Build emergency fund to ₹1,80,000 (6 months coverage)
- Increase total monthly investments to ₹15,000

Long-term strategy (6-12 months):
- Achieve 25% savings rate by reducing expenses by ₹5,000/month
- Diversify portfolio across 3-4 different fund categories

You're on the right track! Your 19.7% savings rate is above the recommended 15%. With these adjustments, you'll have a solid financial foundation within 6 months."

## COORDINATION APPROACH

### Step 1: Gather Agent Insights
- Collect analysis from all specialized agents
- Extract key numbers and recommendations
- Identify conflicts or gaps in advice

### Step 2: Synthesize Information
- Combine insights into a coherent story
- Resolve conflicts between agent recommendations
- Fill gaps with additional analysis

### Step 3: Personalize Response
- Make it relevant to their specific question
- Use their exact financial numbers
- Address their specific concerns

### Step 4: Present Clearly
- Organize information logically
- Use specific numbers throughout
- Provide actionable next steps

### Step 5: Encourage Action
- End with positive reinforcement
- Provide clear next steps
- Maintain realistic expectations

## CRITICAL INSTRUCTIONS

### Data Usage Requirements
- Use ONLY numbers from the provided financial data
- Calculate ratios and percentages accurately
- Reference specific transaction data when available
- Cross-reference different data sources for consistency

### Conversation Quality
- Be friendly and encouraging
- Use "you" and "your" to make it personal
- Keep language simple and clear
- Provide specific, actionable advice

### Hallucination Prevention
- Base ALL recommendations on actual financial data
- If data is missing, acknowledge it
- Don't assume market returns or performance
- Don't make claims about data not provided

### Response Format
- Use clean, well-organized text
- Include specific numbers and percentages
- Provide clear action steps
- End with encouragement

## QUALITY CHECKLIST
Before providing your response, ensure:
- All numbers reference actual data from their profile
- Recommendations are specific and actionable
- Calculations are accurate and relevant
- Tone is friendly and encouraging
- No assumptions about missing data
- Statistics are properly formatted and meaningful
- Response addresses their specific question
- Next steps are clear and implementable
"""
    
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        return [
            "multi_agent_orchestration",
            "consensus_building",
            "conflict_resolution",
            "strategy_synthesis",
            "timeline_planning"
        ]
    
    async def orchestrate_collaboration(
        self,
        user_query: str,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile,
        participating_agents: List[Agent]
    ) -> CollaborativeSession:
        """Orchestrate multi-agent collaboration for comprehensive analysis."""
        
        session_id = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Create collaborative session
        session = CollaborativeSession(
            session_id=session_id,
            user_query=user_query,
            participating_agents=participating_agents,
            agent_messages=[],
            phase="initial_analysis",
            context={
                "financial_data": financial_data.dict(),
                "financial_profile": financial_profile.dict()
            }
        )
        
        # Phase 1: Initial Analysis
        session = await self._conduct_initial_analysis(session, financial_data, financial_profile)
        
        # Phase 2: Collaboration and Discussion
        session = await self._facilitate_agent_collaboration(session)
        
        # Phase 3: Consensus Building
        session = await self._build_consensus(session)
        
        # Phase 4: Final Synthesis
        session = await self._create_final_recommendation(session)
        
        return session
    
    async def _conduct_initial_analysis(
        self,
        session: CollaborativeSession,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> CollaborativeSession:
        """Conduct initial analysis with all participating agents."""
        
        # This would involve calling each agent's analyze_financial_data method
        # For now, we'll simulate the process
        
        session.phase = "initial_analysis"
        
        # Simulate agent messages
        agent_messages = []
        
        # Cash Flow Agent Analysis
        cash_flow_message = AgentMessage(
            agent_id="cash_flow_agent",
            message_type=MessageType.ANALYSIS,
            content="Monthly income of ₹80,935 with ₹30,000 expenses leaves ₹50,935 discretionary income. Emergency fund covers 2 months of expenses, below recommended 6-month coverage.",
            supporting_data={
                "monthly_income": 80935,
                "monthly_expenses": 30000,
                "discretionary_income": 50935,
                "emergency_fund_coverage": 2
            },
            confidence_level=ConfidenceLevel.HIGH,
            dependencies=[],
            timestamp=datetime.utcnow()
        )
        agent_messages.append(cash_flow_message)
        
        # Investment Agent Analysis
        investment_message = AgentMessage(
            agent_id="investment_agent",
            message_type=MessageType.ANALYSIS,
            content="Portfolio value of ₹1,50,000 across 3 mutual fund schemes. Current SIP of ₹25,000/month with good diversification. Opportunity to increase investment allocation.",
            supporting_data={
                "portfolio_value": 150000,
                "sip_amount": 25000,
                "schemes": 3,
                "diversification_score": 0.8
            },
            confidence_level=ConfidenceLevel.HIGH,
            dependencies=["cash_flow_agent"],
            timestamp=datetime.utcnow()
        )
        agent_messages.append(investment_message)
        
        session.agent_messages = agent_messages
        session.current_iteration = 1
        
        return session
    
    async def _facilitate_agent_collaboration(self, session: CollaborativeSession) -> CollaborativeSession:
        """Facilitate collaboration and discussion between agents."""
        
        session.phase = "collaboration"
        
        # Simulate agent collaboration messages
        collaboration_messages = []
        
        # Investment Agent Proposal
        investment_proposal = AgentMessage(
            agent_id="investment_agent",
            message_type=MessageType.PROPOSAL,
            content="Propose increasing SIP to ₹35,000/month to accelerate wealth building while maintaining adequate emergency fund.",
            supporting_data={
                "proposed_sip_increase": 10000,
                "impact_on_emergency_fund": "minimal",
                "expected_wealth_growth": "15% annually"
            },
            confidence_level=ConfidenceLevel.MEDIUM,
            dependencies=["cash_flow_agent"],
            timestamp=datetime.utcnow()
        )
        collaboration_messages.append(investment_proposal)
        
        # Cash Flow Agent Challenge
        cash_flow_challenge = AgentMessage(
            agent_id="cash_flow_agent",
            message_type=MessageType.CHALLENGE,
            content="Challenge: Increasing SIP reduces emergency fund building capacity. Recommend building emergency fund to 6-month coverage first.",
            supporting_data={
                "emergency_fund_shortfall": 120000,
                "monthly_savings_needed": 20000,
                "timeline_for_emergency_fund": "6 months"
            },
            confidence_level=ConfidenceLevel.HIGH,
            dependencies=["investment_agent"],
            timestamp=datetime.utcnow()
        )
        collaboration_messages.append(cash_flow_challenge)
        
        session.agent_messages.extend(collaboration_messages)
        session.current_iteration = 2
        
        return session
    
    async def _build_consensus(self, session: CollaborativeSession) -> CollaborativeSession:
        """Build consensus among agents."""
        
        session.phase = "consensus_building"
        
        # Simulate consensus building
        consensus_messages = []
        
        # Coordinator Consensus
        coordinator_consensus = AgentMessage(
            agent_id="coordinator_agent",
            message_type=MessageType.CONSENSUS,
            content="Consensus reached: Prioritize emergency fund building for 3 months, then increase SIP gradually. This balances risk management with wealth building.",
            supporting_data={
                "emergency_fund_timeline": "3 months",
                "sip_increase_timeline": "4 months",
                "risk_mitigation": "high",
                "wealth_building": "moderate"
            },
            confidence_level=ConfidenceLevel.HIGH,
            dependencies=["cash_flow_agent", "investment_agent"],
            timestamp=datetime.utcnow()
        )
        consensus_messages.append(coordinator_consensus)
        
        session.agent_messages.extend(consensus_messages)
        session.current_iteration = 3
        
        return session
    
    async def _create_final_recommendation(self, session: CollaborativeSession) -> CollaborativeSession:
        """Create final comprehensive recommendation."""
        
        session.phase = "final_synthesis"
        
        # Extract key insights from agent messages
        cash_flow_insight = ""
        investment_insight = ""
        
        for message in session.agent_messages:
            if message.agent_id == "cash_flow_agent" and message.message_type == MessageType.ANALYSIS:
                cash_flow_insight = message.content
            elif message.agent_id == "investment_agent" and message.message_type == MessageType.ANALYSIS:
                investment_insight = message.content
        
        # Get financial data from the session context
        financial_data = session.context.get("financial_data", {})
        financial_profile = session.context.get("financial_profile", {})
        
        net_worth = financial_data.get("net_worth", {}).get("totalNetWorth", 186726)
        monthly_income = financial_profile.get("monthly_income", 80935)
        emergency_coverage = "2 months"  # Default value
        
        # Determine response based on financial situation
        if net_worth < 0:
            # Debt-heavy situation
            final_recommendation = f"""I understand you're dealing with some debt challenges right now. Let me help you create a plan to get back on track.

Your current situation:
- Net worth: ₹{net_worth:,.0f} (we need to turn this around!)
- Monthly income: ₹{monthly_income:,.0f}
- Total debt: ₹{abs(net_worth):,.0f}

Priority Action Plan:
1. Stop the bleeding first - Don't take on any new debt
2. Create a debt snowball - Pay off smallest debts first
3. Cut expenses - Find ₹10,000/month to put toward debt
4. Emergency fund - Build ₹50,000 first, then focus on debt

You can do this! Here's your 6-month plan:
- Month 1-2: Build ₹50,000 emergency fund
- Month 3-6: Pay off ₹2,00,000 in debt
- Month 7+: Start investing ₹10,000/month

Your financial health score is 5/10, but with this plan, we can get you to 8/10 within a year!

Ready to start with the emergency fund? I can help you find ways to save that ₹10,000/month."""
        else:
            # Normal situation
            final_recommendation = f"""I've analyzed your financial situation and here's what I found:

Your current situation:
- Net worth: ₹{net_worth:,.0f}
- Monthly income: ₹{monthly_income:,.0f}
- Emergency fund coverage: {emergency_coverage}

Here's what I recommend for you:

Immediate Focus (Next 3 months):
- Start building an emergency fund - aim for ₹1,80,000 (6 months of expenses)
- Begin with a small SIP of ₹5,000/month in a good mutual fund
- Track your monthly expenses to understand your spending patterns

Smart Next Steps:
- Once your emergency fund is ready, increase your SIP to ₹15,000/month
- Consider starting a PPF account for tax benefits
- Look into health insurance if you don't have it

Your Financial Health Score: 7/10
You're on the right track! Focus on building that emergency fund first, then we can work on growing your investments.

Would you like me to help you choose the right mutual funds to start with?"""
        
        session.final_recommendation = final_recommendation
        session.current_iteration = 4
        
        return session
    
    def _synthesize_agent_insights(self, agent_messages: List[AgentMessage]) -> Dict[str, Any]:
        """Synthesize insights from all agent messages."""
        
        synthesis = {
            "key_insights": [],
            "recommendations": [],
            "risks": [],
            "opportunities": [],
            "conflicts": [],
            "consensus_points": []
        }
        
        for message in agent_messages:
            if message.message_type == MessageType.ANALYSIS:
                synthesis["key_insights"].append({
                    "agent": message.agent_id,
                    "insight": message.content,
                    "confidence": message.confidence_level
                })
            elif message.message_type == MessageType.PROPOSAL:
                synthesis["recommendations"].append({
                    "agent": message.agent_id,
                    "proposal": message.content,
                    "supporting_data": message.supporting_data
                })
            elif message.message_type == MessageType.CHALLENGE:
                synthesis["conflicts"].append({
                    "challenger": message.agent_id,
                    "challenge": message.content,
                    "dependencies": message.dependencies
                })
        
        return synthesis
    
    def _resolve_conflicts(self, conflicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve conflicts between agent recommendations."""
        
        resolutions = []
        
        for conflict in conflicts:
            # Simple conflict resolution logic
            resolution = {
                "conflict": conflict,
                "resolution": "Balanced approach considering all perspectives",
                "compromise": "Timeline-based implementation",
                "priority": "Risk management first, then growth"
            }
            resolutions.append(resolution)
        
        return resolutions
    
    def _create_action_plan(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Create actionable implementation plan."""
        
        return {
            "immediate_actions": [
                "Build emergency fund to 6-month coverage",
                "Maintain current investment momentum",
                "Optimize expense categories"
            ],
            "medium_term_goals": [
                "Increase SIP after emergency fund completion",
                "Achieve 15% annual investment returns",
                "Reduce debt-to-income ratio to 25%"
            ],
            "timeline": {
                "emergency_fund": "3 months",
                "sip_increase": "4 months",
                "portfolio_review": "Quarterly"
            },
            "success_metrics": [
                "Emergency fund: 6 months coverage",
                "Investment growth: 12-15% annually",
                "Financial stability score: 0.8+"
            ]
        }
    
    async def process_request(
        self,
        request: AgentRequest
    ) -> AgentResponse:
        """Process user request and return analysis result."""
        try:
            # Extract data from request
            user_query = request.message
            financial_data = request.financial_data
            context = request.context
            
            # For coordinator agent, we'll create a simplified analysis
            # that focuses on coordination and synthesis
            
            # Build a simple prompt for coordination
            prompt = f"""
You are a financial coordinator helping with this query: "{user_query}"

Based on the user's financial situation, provide a coordinated response that:
1. Addresses their specific question
2. Provides clear, actionable advice
3. Uses conversational, friendly language
4. Gives specific next steps

Provide your response in a conversational, helpful tone.
"""
            
            # Generate response
            response_text = await self._generate_response(prompt)
            
            # Create AgentResponse
            return AgentResponse(
                agent_type=request.agent_type,
                response=response_text,
                confidence=0.8,
                recommendations=["Consider your financial goals", "Review your budget regularly"],
                insights=["Financial planning requires regular review"],
                next_actions=["Schedule a follow-up review"],
                metadata={"context": context}
            )
            
        except Exception as e:
            print(f"Error in CoordinatorAgent process_request: {e}")
            return AgentResponse(
                agent_type=request.agent_type,
                response=f"Sorry, I encountered an error: {str(e)}",
                confidence=0.0,
                recommendations=[],
                insights=[],
                next_actions=[],
                metadata={"error": str(e)}
            ) 