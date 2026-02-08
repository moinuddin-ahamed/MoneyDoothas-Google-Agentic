from typing import List, Dict, Any
from models.agent import AgentType, AgentCapability, AgentRequest, AgentResponse
from .base_agent import BaseAgent


class FinancialHealthAgent(BaseAgent):
    """Financial Health Monitor Agent - Specialized in anomaly detection and financial health assessment."""
    
    def __init__(self):
        super().__init__(
            agent_id="financial_health_agent",
            name="Financial Health Monitor",
            description="Specialized agent for detecting financial anomalies, assessing risk, and monitoring financial health.",
            specialties=[
                "Anomaly detection in spending patterns",
                "Financial risk assessment",
                "Cash flow health monitoring",
                "Fraud detection indicators",
                "Financial stress indicators",
                "Early warning system for financial issues"
            ],
            temperature=0.2,  # Lower temperature for precise analysis
            max_tokens=4000
        )
    
    def get_prompt_template(self) -> str:
        return """
# Financial Health Monitor Agent - Comprehensive Health Analysis

## ROLE DEFINITION
You are an expert financial health advisor who provides detailed analysis of financial well-being. Your responses must be:
- **Data-driven**: Use exact financial data from the user's profile
- **Comprehensive**: Analyze all aspects of financial health
- **Actionable**: Provide specific improvement recommendations
- **Encouraging**: Positive but realistic assessment

## CRITICAL INSTRUCTIONS
1. **Analyze complete financial picture** - income, expenses, savings, debt, investments
2. **Calculate key health metrics** - emergency fund ratio, savings rate, debt-to-income ratio
3. **Identify potential risks** - spending patterns, debt levels, lack of savings
4. **Provide specific recommendations** - concrete steps to improve financial health
5. **Consider life stage** - different priorities for different ages

## FINANCIAL HEALTH METRICS TO CALCULATE

### Emergency Fund Ratio
- **Formula**: Emergency fund ÷ Monthly expenses
- **Target**: 3-6 months of expenses
- **Assessment**: [Excellent/Good/Fair/Poor] based on ratio

### Savings Rate
- **Formula**: (Monthly savings ÷ Monthly income) × 100
- **Target**: 10-20% of income
- **Assessment**: [Excellent/Good/Fair/Poor] based on percentage

### Debt-to-Income Ratio
- **Formula**: (Total monthly debt payments ÷ Monthly income) × 100
- **Target**: Under 40%
- **Assessment**: [Excellent/Good/Fair/Poor] based on percentage

### Credit Score Impact
- **Excellent**: 750+
- **Good**: 700-749
- **Fair**: 650-699
- **Poor**: Below 650

## RESPONSE STRUCTURE

### Step 1: Financial Data Analysis
- **Monthly income**: ₹[exact amount from data]
- **Monthly expenses**: ₹[calculated from data]
- **Emergency fund**: ₹[exact amount from data]
- **Total debt**: ₹[exact amount from data]
- **Credit score**: [from data]

### Step 2: Health Metrics Calculation
- **Emergency fund ratio**: [calculated months]
- **Savings rate**: [calculated percentage]
- **Debt-to-income ratio**: [calculated percentage]
- **Overall health score**: [1-10 scale]

### Step 3: Risk Assessment
- **Primary concerns**: [specific issues identified]
- **Positive indicators**: [strengths in their financial situation]
- **Immediate risks**: [urgent issues to address]

### Step 4: Comprehensive Response
"Looking at your financial health:

Your current situation:
- Monthly income: ₹[exact amount from data]
- Emergency fund: ₹[exact amount] ([calculated] months of expenses)
- Savings rate: [calculated percentage]
- Debt-to-income ratio: [calculated percentage]
- Credit score: [from data]

Financial health assessment:
- **Overall score**: [1-10] out of 10
- **Primary strength**: [best aspect of their finances]
- **Main concern**: [biggest issue to address]

My specific recommendations:
- [One immediate action to improve their situation]
- [One long-term strategy for financial health]

[One encouraging but realistic assessment of their financial position]"

## IMPORTANT RULES
1. **Use exact numbers from their financial data** - never estimate
2. **Calculate all metrics accurately** - don't guess
3. **Provide specific, actionable advice** - not generic suggestions
4. **Consider their age and life stage** - different priorities for different ages
5. **Keep responses under 250 words** but include all necessary details
6. **Be encouraging but realistic** - don't sugar-coat serious issues

## ERROR PREVENTION
- Verify all calculations against their financial data
- Ensure metrics are calculated correctly
- Provide realistic assessments, not optimistic ones
- Address the most critical issues first
"""
    
    def get_capabilities(self) -> List[str]:
        return [
            AgentCapability.ANOMALY_DETECTION,
            AgentCapability.RISK_ASSESSMENT
        ]
    
    def _analyze_financial_health(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial health and detect anomalies."""
        analysis = {
            'health_score': 0,
            'anomalies': [],
            'risks': [],
            'health_indicators': {},
            'recommendations': []
        }
        
        if not financial_data:
            return analysis
        
        # Calculate health indicators
        monthly_income = financial_data.get('monthly_income', 0)
        monthly_expenses = financial_data.get('monthly_expenses', 0)
        emergency_fund = financial_data.get('emergency_fund', 0)
        total_debt = financial_data.get('total_debt', 0)
        credit_score = financial_data.get('credit_score', 0)
        
        # Calculate health indicators
        emergency_fund_ratio = (emergency_fund / monthly_expenses) if monthly_expenses > 0 else 0
        debt_to_income_ratio = (total_debt / monthly_income) * 100 if monthly_income > 0 else 0
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income) * 100 if monthly_income > 0 else 0
        
        analysis['health_indicators'] = {
            'emergency_fund_ratio': emergency_fund_ratio,
            'debt_to_income_ratio': debt_to_income_ratio,
            'savings_rate': savings_rate,
            'credit_score': credit_score
        }
        
        # Detect anomalies and risks
        if emergency_fund_ratio < 3:
            analysis['anomalies'].append({
                'type': 'low_emergency_fund',
                'severity': 'high',
                'description': f'Emergency fund covers only {emergency_fund_ratio:.1f} months of expenses (recommended: 3-6 months)'
            })
        
        if debt_to_income_ratio > 40:
            analysis['risks'].append({
                'type': 'high_debt_ratio',
                'severity': 'high',
                'description': f'Debt-to-income ratio is {debt_to_income_ratio:.1f}% (recommended: under 40%)'
            })
        
        if savings_rate < 10:
            analysis['anomalies'].append({
                'type': 'low_savings_rate',
                'severity': 'medium',
                'description': f'Savings rate is {savings_rate:.1f}% (recommended: 10-20%)'
            })
        
        if credit_score < 650:
            analysis['risks'].append({
                'type': 'low_credit_score',
                'severity': 'medium',
                'description': f'Credit score is {credit_score} (recommended: 650+)'
            })
        
        # Calculate overall health score (1-10)
        score = 10
        
        # Deduct points for issues
        if emergency_fund_ratio < 3:
            score -= 3
        elif emergency_fund_ratio < 6:
            score -= 1
        
        if debt_to_income_ratio > 40:
            score -= 3
        elif debt_to_income_ratio > 30:
            score -= 1
        
        if savings_rate < 10:
            score -= 2
        elif savings_rate < 15:
            score -= 1
        
        if credit_score < 650:
            score -= 2
        elif credit_score < 700:
            score -= 1
        
        analysis['health_score'] = max(1, score)
        
        return analysis
    
    def _detect_spending_anomalies(self, financial_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalies in spending patterns."""
        anomalies = []
        
        # This would typically analyze historical spending data
        # For now, we'll use a simplified approach
        recent_transactions = financial_data.get('recent_transactions', [])
        
        if not recent_transactions:
            return anomalies
        
        # Calculate average transaction amount
        amounts = [t.get('amount', 0) for t in recent_transactions]
        avg_amount = sum(amounts) / len(amounts) if amounts else 0
        
        # Detect high-value transactions (2x average)
        for transaction in recent_transactions:
            amount = transaction.get('amount', 0)
            if amount > avg_amount * 2:
                anomalies.append({
                    'type': 'high_value_transaction',
                    'severity': 'medium',
                    'description': f'Unusually high transaction: ₹{amount:,.2f}',
                    'transaction': transaction
                })
        
        return anomalies
    
    def _build_prompt(self, request) -> str:
        """Override to include health-specific analysis."""
        template = self.get_prompt_template()
        
        # Analyze financial health
        health_analysis = self._analyze_financial_health(request.financial_data)
        
        # Detect spending anomalies
        spending_anomalies = self._detect_spending_anomalies(request.financial_data)
        
        # Add health analysis to the prompt
        enhanced_template = template + f"""

**Financial Health Analysis Summary**:
- Health Score: {health_analysis['health_score']}/10
- Emergency Fund Ratio: {health_analysis['health_indicators'].get('emergency_fund_ratio', 0):.1f} months
- Debt-to-Income Ratio: {health_analysis['health_indicators'].get('debt_to_income_ratio', 0):.1f}%
- Savings Rate: {health_analysis['health_indicators'].get('savings_rate', 0):.1f}%
- Credit Score: {health_analysis['health_indicators'].get('credit_score', 0)}

**Detected Issues**:
- Anomalies: {len(health_analysis['anomalies'])}
- Risks: {len(health_analysis['risks'])}
- Spending Anomalies: {len(spending_anomalies)}

**Health Status**: {'Good' if health_analysis['health_score'] >= 7 else 'Fair' if health_analysis['health_score'] >= 5 else 'Poor'}

Use this analysis to provide specific, actionable financial health advice.
"""
        
        # Extract context
        context = self._extract_context(request)
        
        # Build the prompt
        prompt = enhanced_template.format(
            user_message=request.message,
            context=context,
            financial_data=self._format_financial_data(request.financial_data),
            conversation_history=self._format_conversation_history(request.conversation_history)
        )
        
        return prompt
    
    def _extract_context(self, request) -> str:
        """Extract context from the request."""
        context_parts = []
        
        if hasattr(request, 'context') and request.context:
            context_parts.append(f"Context: {request.context}")
        
        if hasattr(request, 'session_id') and request.session_id:
            context_parts.append(f"Session: {request.session_id}")
        
        if hasattr(request, 'phone_number') and request.phone_number:
            context_parts.append(f"User: {request.phone_number}")
        
        return " | ".join(context_parts) if context_parts else "No additional context"
    
    def _format_financial_data(self, financial_data) -> str:
        """Format financial data for prompt inclusion."""
        if not financial_data:
            return "No financial data available"
        
        try:
            # Convert to string representation
            return str(financial_data)
        except Exception as e:
            return f"Financial data (error formatting: {e})"
    
    def _format_conversation_history(self, conversation_history) -> str:
        """Format conversation history for prompt inclusion."""
        if not conversation_history:
            return "No conversation history"
        
        try:
            # Convert to string representation
            return str(conversation_history)
        except Exception as e:
            return f"Conversation history (error formatting: {e})"
    
    async def process_request(
        self,
        request: AgentRequest
    ) -> AgentResponse:
        """Process financial health analysis request."""
        try:
            # Extract data from request
            user_query = request.message
            financial_data = request.financial_data
            context = request.context
            
            # Analyze financial health
            health_analysis = self._analyze_financial_health(financial_data)
            
            # Detect spending anomalies
            spending_anomalies = self._detect_spending_anomalies(financial_data)
            
            # Build analysis prompt
            prompt = self._build_prompt(request)
            
            # Generate response
            response_text = await self._generate_response(prompt)
            
            # Create AgentResponse
            return AgentResponse(
                agent_type=request.agent_type,
                response=response_text,
                confidence=0.85,
                recommendations=[
                    "Monitor spending patterns regularly",
                    "Build emergency fund to 3-6 months of expenses",
                    "Review insurance coverage adequacy"
                ],
                insights=[
                    f"Financial health score: {health_analysis['health_score']}/10",
                    f"Emergency fund ratio: {health_analysis['health_indicators'].get('emergency_fund_ratio', 0):.1f} months",
                    f"Detected anomalies: {len(health_analysis['anomalies'])}"
                ],
                next_actions=[
                    "Set up automated spending alerts",
                    "Create monthly financial health review",
                    "Establish emergency fund target"
                ],
                metadata={
                    "health_analysis": health_analysis,
                    "spending_anomalies": spending_anomalies,
                    "context": context
                }
            )
            
        except Exception as e:
            print(f"Error in FinancialHealthAgent process_request: {e}")
            return AgentResponse(
                agent_type=request.agent_type,
                response=f"Sorry, I encountered an error: {str(e)}",
                confidence=0.0,
                recommendations=[],
                insights=[],
                next_actions=[],
                metadata={"error": str(e)}
            ) 