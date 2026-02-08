import asyncio
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

import google.generativeai as genai

from models.agent_messages import AgentMessage, MessageType, ConfidenceLevel, AgentAnalysisResult
from models.financial_data import ComprehensiveFinancialData, FinancialProfile


class BaseAgent(ABC):
    """Base class for all specialized financial agents."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str,
        specialties: List[str],
        temperature: float = 0.2,
        max_tokens: int = 4000
    ):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.specialties = specialties
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize Gemini model
        self.model = self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the Google Generative AI model for this agent."""
        try:
            # Use API key from environment variable
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                print(f"⚠️  No GOOGLE_API_KEY found for {self.name}. Using fallback responses.")
                return None
            
            # Configure with API key
            genai.configure(api_key=api_key)
            
            # Create model instance
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Test the model with a simple prompt
            try:
                test_response = model.generate_content("test")
                print(f"✅ Model initialized successfully for {self.name}")
                return model
            except Exception as e:
                print(f"❌ Model test failed for {self.name}: {e}")
                return None
                
        except Exception as e:
            print(f"Error initializing model for {self.name}: {e}")
            return None
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """Return the prompt template for this agent."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        pass
    
    async def analyze_financial_data(
        self,
        user_query: str,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile,
        context: Dict[str, Any] = None
    ) -> AgentAnalysisResult:
        """Analyze financial data and return structured analysis."""
        try:
            # Build the prompt
            prompt = self._build_analysis_prompt(user_query, financial_data, financial_profile, context)
            
            # Generate response
            response_text = await self._generate_response(prompt)
            
            # Parse and structure the response
            structured_response = self._parse_analysis_response(response_text, user_query)
            
            return structured_response
            
        except Exception as e:
            print(f"Error in {self.name} analysis: {e}")
            return self._create_error_response(str(e))
    
    def _build_analysis_prompt(
        self,
        user_query: str,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile,
        context: Dict[str, Any] = None
    ) -> str:
        """Build comprehensive analysis prompt with financial data."""
        
        # Get base prompt template
        base_prompt = self.get_prompt_template()
        
        # Format financial data for the prompt
        formatted_data = self._format_financial_data_for_prompt(financial_data, financial_profile)
        
        # Build the complete prompt
        prompt = f"""
{base_prompt}

## USER QUERY
{user_query}

## FINANCIAL PROFILE DATA
{formatted_data}

## CRITICAL INSTRUCTIONS FOR RESPONSE QUALITY

### 1. DATA-DRIVEN ANALYSIS
- Use ONLY the financial data provided above
- Reference specific numbers from the user's actual financial situation
- If data is missing, acknowledge it and suggest what information would help
- NEVER make assumptions about data not provided

### 2. PRECISE AND CLEAN RESPONSE
- Provide exact amounts with proper formatting (₹1,00,000 not ₹100000)
- Use percentages for ratios and returns (15.5% not 0.155)
- Include specific calculations where relevant
- Present information in clear, organized sections

### 3. FRIENDLY AND ENCOURAGING TONE
- Use conversational language ("I can see that..." "Here's what I recommend...")
- Be encouraging but realistic about financial challenges
- Acknowledge progress and positive financial behaviors
- Use "you" and "your" to make it personal

### 4. STATISTICS-RICH CONTENT
- Include relevant financial ratios and metrics
- Provide comparative benchmarks where appropriate
- Show progress indicators and improvement potential
- Use specific numbers to support recommendations

### 5. HALLUCINATION PREVENTION
- Base ALL recommendations on actual financial data provided
- If you don't have specific data, say "Based on the information available..."
- Don't assume market returns or investment performance
- Don't make claims about data not in the profile

### 6. FUNCTION USAGE REQUIREMENTS
- Use the exact financial data provided
- Calculate ratios and percentages accurately
- Reference specific transaction data when available
- Cross-reference different data sources for consistency

## ANALYSIS REQUIREMENTS
1. Analyze the user's financial situation from your specialized perspective
2. Provide specific, actionable recommendations with exact amounts
3. Include relevant calculations and supporting data from their profile
4. Identify risks and opportunities in your domain
5. Consider interdependencies with other financial domains
6. Provide confidence level for your analysis based on data completeness

## RESPONSE FORMAT
Provide your analysis in this exact JSON format:

{{
    "analysis": "Detailed analysis using specific numbers from their financial data",
    "recommendations": [
        "Specific, actionable recommendation with exact amounts",
        "Another specific recommendation with timeline"
    ],
    "insights": [
        "Key insight supported by their actual financial data",
        "Another insight based on their specific situation"
    ],
    "calculations": {{
        "calculation_name": "exact_calculation_value",
        "supporting_data": "specific_data_from_profile"
    }},
    "confidence_score": 0.85,
    "dependencies": ["other_domain_1", "other_domain_2"],
    "risks": [
        "Specific risk based on their actual financial situation",
        "Another risk with supporting data"
    ],
    "opportunities": [
        "Specific opportunity with exact potential impact",
        "Another opportunity with timeline"
    ],
    "statistics": {{
        "key_metric_1": "exact_value",
        "key_metric_2": "exact_value",
        "comparison_benchmark": "industry_average"
    }}
}}

## QUALITY CHECKLIST
Before providing your response, ensure:
- All numbers reference actual data from their profile
- Recommendations are specific and actionable
- Calculations are accurate and relevant
- Tone is friendly and encouraging
- No assumptions about missing data
- Statistics are properly formatted and meaningful
"""
        
        return prompt
    
    def _format_financial_data_for_prompt(
        self,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> str:
        """Format financial data for prompt inclusion."""
        
        return f"""
### INCOME ANALYSIS
- Monthly Income: ₹{financial_profile.monthly_income:,.2f}
- Income Stability: {financial_profile.income_stability}
- Income Source: {financial_profile.income_source}

### EXPENSE ANALYSIS
- Monthly Expenses: ₹{financial_profile.monthly_expenses:,.2f}
- Discretionary Income: ₹{financial_profile.discretionary_income:,.2f}
- Expense Categories: {financial_profile.expense_categories}

### ASSET ANALYSIS
- Total Assets: ₹{financial_profile.total_assets:,.2f}
- Liquid Savings: ₹{financial_profile.liquid_savings:,.2f}
- Investments: ₹{financial_profile.investments:,.2f}
- Retirement Savings: ₹{financial_profile.retirement_savings:,.2f}

### DEBT ANALYSIS
- Total Debt: ₹{financial_profile.total_debt:,.2f}
- Credit Score: {financial_profile.credit_score}
- Debt-to-Income Ratio: {financial_profile.debt_to_income_ratio:.2%}

### INVESTMENT ANALYSIS
- Portfolio Value: ₹{financial_profile.portfolio_value:,.2f}
- Investment Schemes: {financial_profile.investment_schemes}
- Portfolio Performance: {financial_profile.portfolio_performance}

### RISK ANALYSIS
- Emergency Fund Adequacy: {financial_profile.emergency_fund_adequacy}
- Insurance Coverage: {financial_profile.insurance_coverage}
- Financial Stability Score: {financial_profile.financial_stability_score:.2f}

### DETAILED TRANSACTION DATA
- Bank Transactions: {len(financial_data.bank_transactions)} transactions
- Credit Accounts: {len(financial_data.credit_report.accounts)} accounts
- Mutual Fund Schemes: {len(financial_data.mf_transactions)} schemes
- EPF Balance: ₹{financial_data.epf_details.totalBalance:,.2f}
- Net Worth: ₹{financial_data.net_worth.totalNetWorth:,.2f}
"""
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response using the AI model."""
        try:
            if self.model is None:
                return self._get_fallback_response()
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating response for {self.name}: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when model is not available."""
        return f"""
{{
    "analysis": "Unable to perform detailed analysis due to technical limitations. Please ensure all financial data is accurate and up-to-date.",
    "recommendations": ["Consult with a financial advisor for personalized advice"],
    "insights": ["Analysis requires complete financial data"],
    "calculations": {{}},
    "confidence_score": 0.3,
    "dependencies": [],
    "risks": ["Limited analysis capability"],
    "opportunities": ["Complete financial data review recommended"]
}}
"""
    
    def _parse_analysis_response(self, response_text: str, user_query: str) -> AgentAnalysisResult:
        """Parse the AI response into structured format."""
        try:
            # Try to extract JSON from response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
            else:
                # Fallback parsing
                data = self._parse_text_response(response_text)
            
            return AgentAnalysisResult(
                agent_id=self.agent_id,
                analysis=data.get("analysis", "Analysis not available"),
                recommendations=data.get("recommendations", []),
                insights=data.get("insights", []),
                calculations=data.get("calculations", {}),
                confidence_score=data.get("confidence_score", 0.5),
                dependencies=data.get("dependencies", []),
                risks=data.get("risks", []),
                opportunities=data.get("opportunities", [])
            )
            
        except Exception as e:
            print(f"Error parsing response for {self.name}: {e}")
            return self._create_error_response(str(e))
    
    def _parse_text_response(self, response_text: str) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails."""
        return {
            "analysis": response_text,
            "recommendations": ["Review financial data for accuracy"],
            "insights": ["Analysis completed with limitations"],
            "calculations": {},
            "confidence_score": 0.4,
            "dependencies": [],
            "risks": ["Limited analysis capability"],
            "opportunities": ["Complete financial review recommended"]
        }
    
    def _create_error_response(self, error_message: str) -> AgentAnalysisResult:
        """Create error response when analysis fails."""
        return AgentAnalysisResult(
            agent_id=self.agent_id,
            analysis=f"Error in analysis: {error_message}",
            recommendations=["Please try again or contact support"],
            insights=["Analysis could not be completed"],
            calculations={},
            confidence_score=0.1,
            dependencies=[],
            risks=["Analysis failure"],
            opportunities=["Retry analysis"]
        )
    
    async def create_agent_message(
        self,
        analysis_result: AgentAnalysisResult,
        message_type: MessageType = MessageType.ANALYSIS
    ) -> AgentMessage:
        """Create an agent message from analysis result."""
        
        return AgentMessage(
            agent_id=self.agent_id,
            message_type=message_type,
            content=analysis_result.analysis,
            supporting_data={
                "recommendations": analysis_result.recommendations,
                "insights": analysis_result.insights,
                "calculations": analysis_result.calculations,
                "confidence_score": analysis_result.confidence_score,
                "dependencies": analysis_result.dependencies,
                "risks": analysis_result.risks,
                "opportunities": analysis_result.opportunities
            },
            confidence_level=self._get_confidence_level(analysis_result.confidence_score),
            dependencies=analysis_result.dependencies,
            timestamp=datetime.utcnow()
        )
    
    def _get_confidence_level(self, confidence_score: float) -> ConfidenceLevel:
        """Convert confidence score to confidence level."""
        if confidence_score >= 0.7:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 0.4:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW 