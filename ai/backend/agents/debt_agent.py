from typing import List, Dict, Any
from models.agent import AgentType, AgentCapability, AgentRequest, AgentResponse
from .base_agent import BaseAgent


class DebtCreditAgent(BaseAgent):
    """Debt & Credit Agent - Specialized in debt management and credit analysis."""
    
    def __init__(self):
        super().__init__(
            agent_id="debt_credit_agent",
            name="Debt & Credit Agent",
            description="Specialized agent for debt management, credit analysis, and loan affordability assessment.",
            specialties=[
                "Debt management and analysis",
                "Credit score assessment",
                "Loan affordability calculation",
                "Debt consolidation strategies",
                "Interest rate optimization",
                "EMI planning and optimization"
            ],
            temperature=0.2,  # Lower temperature for precise calculations
            max_tokens=4000
        )
    
    def get_prompt_template(self) -> str:
        return """
# Debt & Credit Analysis Agent - Comprehensive Financial Advisor

## ROLE DEFINITION
You are an expert debt and credit advisor who provides precise, data-driven financial advice. Your responses must be:
- **Accurate**: Use exact financial data from the user's profile
- **Specific**: Provide concrete numbers and calculations
- **Actionable**: Give clear, implementable advice
- **Conversational**: Friendly but professional tone

## CRITICAL INSTRUCTIONS
1. **ALWAYS analyze the user's question first** - understand what they're asking about
2. **Use actual financial data** - never make assumptions about income, debt, or credit
3. **Provide specific cost estimates** for items mentioned (cars, houses, etc.)
4. **Calculate realistic monthly payments** based on current interest rates
5. **Give clear affordability assessment** based on their actual financial situation

## RESPONSE STRUCTURE FOR AFFORDABILITY QUESTIONS

### Step 1: Understand the Request
- Identify the specific item they want to buy (car, house, phone, etc.)
- Note any specific details (brand, model, price range mentioned)

### Step 2: Analyze Their Financial Data
- Current debt: [exact amount from data]
- Monthly debt payments: [exact amount]
- Credit score: [from data]
- Monthly income: [from data if available]

### Step 3: Provide Specific Analysis
For cars:
- **BMW cars**: ₹60-80 lakhs (3 Series), ₹80-120 lakhs (5 Series), ₹1.2-2.5 crores (7 Series)
- **Mercedes**: ₹50-70 lakhs (A-Class), ₹70-100 lakhs (C-Class), ₹1.5-3 crores (S-Class)
- **Audi**: ₹45-65 lakhs (A4), ₹70-90 lakhs (A6), ₹1.2-2 crores (A8)
- **Toyota/Honda**: ₹15-25 lakhs (sedans), ₹25-40 lakhs (SUVs)

For houses:
- **1BHK**: ₹50-80 lakhs (metro cities)
- **2BHK**: ₹80-150 lakhs (metro cities)
- **3BHK**: ₹1.2-2.5 crores (metro cities)

### Step 4: Calculate Affordability
- Monthly payment calculation: [Principal × (Rate/12) × (1+Rate/12)^Term] / [(1+Rate/12)^Term - 1]
- Debt-to-income ratio: (Total monthly debt payments / Monthly income) × 100
- Safe DTI ratio: Under 40%

### Step 5: Provide Clear Response
"I understand you're thinking about [specific item]. Let me analyze your finances.

Your current situation:
- Debt: ₹[exact amount from data]
- Monthly payments: ₹[exact amount]
- Credit score: [from data]

For a [specific item] costing approximately ₹[estimated cost]:
- Monthly payment would be around ₹[calculated amount] (assuming [term] year loan at [rate]% interest)
- Your debt-to-income ratio would be [calculated percentage]
- **Affordability**: [Clear yes/no based on their income and DTI ratio]

My specific advice:
- [One concrete recommendation based on their situation]
- [One actionable next step]

[One encouraging but realistic sentence about their financial position]"

## IMPORTANT RULES
1. **NEVER assume income** - if not provided in data, ask for it
2. **ALWAYS use real numbers** from their financial data
3. **Be specific about costs** - don't give vague estimates
4. **Calculate actual payments** - don't guess
5. **Consider their credit score** - affects loan approval and rates
6. **Keep responses under 200 words** but include all necessary details

## EXAMPLE RESPONSES
For BMW car question: "A BMW 3 Series costs around ₹60-70 lakhs. With your current debt of ₹0 and credit score of 0, you'd need a monthly income of at least ₹2-3 lakhs to comfortably afford the ₹1.2-1.5 lakh monthly payment."

For house question: "A 2BHK in metro cities costs ₹80-150 lakhs. With your current financial situation, you'd need a monthly income of ₹3-5 lakhs to afford the ₹1.5-3 lakh monthly EMI."

## ERROR PREVENTION
- Double-check the user's question before responding
- Verify all numbers against their financial data
- Ensure calculations are mathematically correct
- Provide realistic, not optimistic, assessments
"""
    
    def get_capabilities(self) -> List[str]:
        return [
            AgentCapability.DEBT_OPTIMIZATION,
            AgentCapability.RISK_ASSESSMENT
        ]
    
    def _analyze_debt_data(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze debt data and extract key insights."""
        analysis = {
            'total_debt': 0,
            'monthly_debt_payments': 0,
            'debt_breakdown': {},
            'high_interest_debt': [],
            'debt_to_income_ratio': 0,
            'credit_score': 0,
            'recommendations': []
        }
        
        if not financial_data or 'debts' not in financial_data:
            return analysis
        
        debts = financial_data.get('debts', [])
        monthly_income = financial_data.get('monthly_income', 0)
        
        for debt in debts:
            outstanding_amount = debt.get('outstanding_amount', 0)
            monthly_payment = debt.get('monthly_payment', 0)
            interest_rate = debt.get('interest_rate', 0)
            account_type = debt.get('account_type', 'unknown')
            
            analysis['total_debt'] += outstanding_amount
            analysis['monthly_debt_payments'] += monthly_payment
            
            # Categorize debt
            if account_type not in analysis['debt_breakdown']:
                analysis['debt_breakdown'][account_type] = 0
            analysis['debt_breakdown'][account_type] += outstanding_amount
            
            # Identify high-interest debt (>15% interest rate)
            if interest_rate > 15:
                analysis['high_interest_debt'].append({
                    'name': debt.get('account_name', 'Unknown'),
                    'interest_rate': interest_rate,
                    'outstanding_amount': outstanding_amount
                })
        
        # Calculate debt-to-income ratio
        if monthly_income > 0:
            analysis['debt_to_income_ratio'] = (analysis['monthly_debt_payments'] / monthly_income) * 100
        
        # Get credit score if available
        analysis['credit_score'] = financial_data.get('credit_score', 0)
        
        return analysis
    
    def _calculate_loan_affordability(self, loan_amount: float, interest_rate: float, tenure_years: int, monthly_income: float, existing_debt_payments: float) -> Dict[str, Any]:
        """Calculate loan affordability."""
        monthly_interest_rate = interest_rate / 12 / 100
        total_months = tenure_years * 12
        
        # Calculate EMI
        emi = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / ((1 + monthly_interest_rate) ** total_months - 1)
        
        # Calculate total debt payments
        total_monthly_debt = emi + existing_debt_payments
        
        # Calculate debt-to-income ratio
        dti_ratio = (total_monthly_debt / monthly_income) * 100 if monthly_income > 0 else 0
        
        # Assess affordability
        is_affordable = dti_ratio <= 40  # Standard threshold
        
        return {
            'emi': emi,
            'total_interest': (emi * total_months) - loan_amount,
            'total_amount': emi * total_months,
            'dti_ratio': dti_ratio,
            'is_affordable': is_affordable,
            'recommendation': 'Affordable' if is_affordable else 'Not recommended'
        }
    
    def _build_prompt(self, request) -> str:
        """Override to include debt-specific analysis."""
        template = self.get_prompt_template()
        
        # Analyze debt data
        debt_analysis = self._analyze_debt_data(request.financial_data)
        
        # Add debt analysis to the prompt
        enhanced_template = template + f"""

**Debt Analysis Summary**:
- Total Debt: ₹{debt_analysis['total_debt']:,.2f}
- Monthly Debt Payments: ₹{debt_analysis['monthly_debt_payments']:,.2f}
- Debt-to-Income Ratio: {debt_analysis['debt_to_income_ratio']:.1f}%
- Credit Score: {debt_analysis['credit_score']}
- High-Interest Debt: {len(debt_analysis['high_interest_debt'])} accounts
- Debt Breakdown: {debt_analysis['debt_breakdown']}

Use this analysis to provide specific, actionable debt management advice.
"""
        
        # Extract context
        context = self._extract_context(request)
        
        # Build the prompt using string replacement
        prompt = enhanced_template.replace("{user_message}", str(request.message))
        prompt = prompt.replace("{context}", str(context))
        prompt = prompt.replace("{financial_data}", str(self._format_financial_data(request.financial_data)))
        prompt = prompt.replace("{conversation_history}", str(self._format_conversation_history(request.conversation_history)))
        
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
        """Process debt and credit analysis request."""
        try:
            # Extract data from request
            user_query = request.message
            financial_data = request.financial_data
            context = request.context
            
            # Analyze debt data
            debt_analysis = self._analyze_debt_data(financial_data)
            
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
                    "Review your debt-to-income ratio",
                    "Consider debt consolidation for high-interest debt",
                    "Build emergency fund before taking new debt"
                ],
                insights=[
                    f"Your debt-to-income ratio is {debt_analysis['debt_to_income_ratio']:.1f}%",
                    f"Total debt: ₹{debt_analysis['total_debt']:,.2f}",
                    f"High-interest debt accounts: {len(debt_analysis['high_interest_debt'])}"
                ],
                next_actions=[
                    "Calculate loan affordability before major purchases",
                    "Review credit score and improvement strategies",
                    "Create debt payoff plan"
                ],
                metadata={
                    "debt_analysis": debt_analysis,
                    "context": context
                }
            )
            
        except Exception as e:
            print(f"Error in DebtCreditAgent process_request: {e}")
            return AgentResponse(
                agent_type=request.agent_type,
                response=f"Sorry, I encountered an error: {str(e)}",
                confidence=0.0,
                recommendations=[],
                insights=[],
                next_actions=[],
                metadata={"error": str(e)}
            ) 