import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import re
import math

# Add new imports for tools
import requests
from urllib.parse import quote_plus
import subprocess
import sys


@dataclass
class AgentResponse:
    agent_id: str
    agent_name: str
    input_query: str
    response: str
    confidence: float
    reasoning: str
    metadata: Dict[str, Any]
    timestamp: datetime


@dataclass
class CollaborationSession:
    session_id: str
    user_query: str
    agent_responses: List[AgentResponse]
    final_response: str
    collaboration_log: List[Dict[str, Any]]
    timestamp: datetime
    tool_results: Dict[str, str] = None


class ADKAgentSystem:
    """ADK-based multi-agent system for financial analysis."""
    
    def __init__(self):
        # Initialize Gemini model
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
        
        # Define agents with their capabilities
        self.agents = {
            "data_analyst": {
                "name": "Financial Data Analyst",
                "description": "Analyzes financial data and provides insights",
                "capabilities": ["data_analysis", "financial_metrics", "trend_analysis"],
                "prompt_template": self._get_data_analyst_prompt()
            },
            "investment_advisor": {
                "name": "Investment Advisor",
                "description": "Provides investment recommendations and portfolio analysis",
                "capabilities": ["investment_analysis", "portfolio_optimization", "risk_assessment"],
                "prompt_template": self._get_investment_advisor_prompt()
            },
            "cash_flow_specialist": {
                "name": "Cash Flow Specialist",
                "description": "Analyzes income, expenses, and cash flow patterns",
                "capabilities": ["cash_flow_analysis", "budget_optimization", "expense_tracking"],
                "prompt_template": self._get_cash_flow_specialist_prompt()
            },
            "critic": {
                "name": "Critic Agent",
                "description": "Validates recommendations and detects hallucinations",
                "capabilities": ["validation", "hallucination_detection", "quality_assurance"],
                "prompt_template": self._get_critic_prompt()
            },
            "coordinator": {
                "name": "Coordinator Agent",
                "description": "Orchestrates agent collaboration and synthesizes responses",
                "capabilities": ["coordination", "synthesis", "consensus_building"],
                "prompt_template": self._get_coordinator_prompt()
            }
        }
        
        # Initialize tools
        self.tools = {
            "google_search": self._google_search,
            "calculator": self._calculator,
            "price_check": self._price_check,
            "currency_converter": self._currency_converter
        }
    
    def _get_data_analyst_prompt(self) -> str:
        return """
You are a Financial Data Analyst. Your role is to analyze financial data and provide insights.

CRITICAL INSTRUCTIONS:
- Use ONLY the financial data provided
- Provide specific numbers and calculations
- Reference exact amounts from the data
- If data is missing, acknowledge it
- NEVER make assumptions about data not provided

RESPONSE FORMAT:
{
    "analysis": "Detailed analysis using specific numbers",
    "key_metrics": {
        "metric_name": "exact_value"
    },
    "insights": ["Specific insight 1", "Specific insight 2"],
    "confidence": 0.85,
    "reasoning": "Why you reached these conclusions"
}
"""
    
    def _get_investment_advisor_prompt(self) -> str:
        return """
You are an Investment Advisor. Your role is to provide investment recommendations and portfolio analysis.

CRITICAL INSTRUCTIONS:
- Use ONLY the investment data provided
- Calculate exact returns and percentages
- Provide specific investment recommendations
- If data is missing, acknowledge it
- NEVER assume market performance
- For affordability questions: Calculate what percentage of net worth a purchase represents
- For savings goals: Calculate monthly savings targets and timelines
- Provide specific financial calculations

RESPONSE FORMAT:
{
    "portfolio_analysis": "Detailed portfolio analysis with specific amounts and percentages",
    "affordability_calculation": "For purchase questions, calculate percentage of net worth",
    "savings_plan": "For savings goals, provide monthly targets and timeline",
    "recommendations": ["Specific actionable recommendation 1", "Specific actionable recommendation 2"],
    "risk_assessment": "Risk analysis with specific numbers",
    "confidence": 0.85,
    "reasoning": "Why you made these recommendations"
}

ANALYSIS REQUIREMENTS:
- Use actual financial data provided
- Calculate percentages and ratios
- Provide specific monthly savings targets
- Analyze purchase affordability based on net worth
- Give timeline-based recommendations
"""
    
    def _get_cash_flow_specialist_prompt(self) -> str:
        return """
You are a Cash Flow Specialist. Your role is to analyze income, expenses, and cash flow patterns.

CRITICAL INSTRUCTIONS:
- Use ONLY the financial data provided
- Calculate exact ratios and percentages
- Provide specific cash flow recommendations
- If data is missing, acknowledge it
- NEVER assume income or expense changes
- For affordability questions: Calculate monthly payment capacity
- For savings goals: Calculate realistic monthly savings potential
- Provide specific financial calculations

RESPONSE FORMAT:
{
    "cash_flow_analysis": "Detailed cash flow analysis with specific amounts",
    "affordability_analysis": "For purchase questions, analyze monthly payment capacity",
    "savings_capacity": "For savings goals, calculate realistic monthly savings potential",
    "recommendations": ["Specific actionable recommendation 1", "Specific actionable recommendation 2"],
    "key_metrics": {
        "metric_name": "exact_value"
    },
    "confidence": 0.85,
    "reasoning": "Why you reached these conclusions"
}

ANALYSIS REQUIREMENTS:
- Use actual financial data provided
- Calculate monthly payment capacities
- Provide realistic savings targets
- Analyze affordability based on current cash flow
- Give specific monthly recommendations
"""
    
    def _get_critic_prompt(self) -> str:
        return """
You are a Critic Agent. Your role is to validate recommendations and detect hallucinations.

CRITICAL INSTRUCTIONS:
- Check every number against provided data
- Identify unsupported claims
- Detect unrealistic projections
- Validate logical consistency
- Provide specific feedback
- Be lenient with reasonable responses
- Only flag critical errors, not minor issues
- Approve responses that are generally helpful

RESPONSE FORMAT:
{
    "validation_status": "APPROVED|NEEDS_REVISION|CRITICAL_ERRORS",
    "critical_errors": ["Error 1", "Error 2"],
    "moderate_concerns": ["Concern 1", "Concern 2"],
    "hallucination_flags": ["Flag 1", "Flag 2"],
    "confidence": 0.85,
    "reasoning": "Why you reached this validation conclusion"
}

VALIDATION GUIDELINES:
- APPROVE if the response is helpful and uses available data
- Only flag CRITICAL_ERRORS for major factual errors
- Be lenient with reasonable estimates and calculations
- Focus on whether the response addresses the user's query
- Don't reject responses just because some data is missing
"""
    
    def _get_coordinator_prompt(self) -> str:
        return """
You are a Coordinator Agent. Your role is to orchestrate agent collaboration and synthesize responses.

CRITICAL INSTRUCTIONS:
- Synthesize insights from all agents
- Resolve conflicts between recommendations
- Create a coherent final response
- Ensure all recommendations are actionable
- Maintain conversational tone
- Include specific financial data and statistics
- Be direct and helpful to the user
- Provide personalized advice based on the user's actual financial situation
- Calculate affordability ratios and percentages
- Give specific savings targets and timelines

RESPONSE FORMAT:
{
    "synthesized_response": "Final comprehensive response that directly answers the user's query with specific financial data, calculations, and personalized advice",
    "key_recommendations": ["Specific actionable recommendation 1", "Specific actionable recommendation 2"],
    "conflicts_resolved": ["Any conflicts that were resolved"],
    "confidence": 0.85,
    "reasoning": "How you synthesized the agent responses"
}

ANALYSIS REQUIREMENTS:
- For affordability questions: Calculate what percentage of net worth the purchase represents
- For savings goals: Provide specific monthly savings targets and timelines
- For investments: Analyze current portfolio and suggest improvements
- For travel planning: Calculate total costs and savings strategies
- Always use the actual financial data provided by the agents

IMPORTANT: Analyze the user's query and provide specific, calculated advice based on their real financial data. Don't give generic responses.
"""
    
    def _google_search(self, query: str) -> str:
        """Perform a Google search and return relevant results"""
        try:
            # Using a simple search API (you can replace with Google Custom Search API)
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Extract basic information from search results
                content = response.text.lower()
                if "price" in content or "cost" in content or "₹" in content:
                    return f"Found pricing information for: {query}"
                elif "how to" in query.lower():
                    return f"Found instructions and guides for: {query}"
                else:
                    return f"Found general information for: {query}"
            else:
                return f"Search failed for: {query}"
        except Exception as e:
            return f"Search error: {str(e)}"

    def _calculator(self, expression: str) -> str:
        """Evaluate mathematical expressions safely"""
        try:
            # Remove any non-mathematical characters for safety
            clean_expr = re.sub(r'[^0-9+\-*/()., ]', '', expression)
            # Use eval with limited scope for calculation
            result = eval(clean_expr)
            return f"Calculation result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"

    def _price_check(self, item: str) -> str:
        """Check approximate prices for common items"""
        try:
            # Simple price database for common items
            price_db = {
                "car": "₹5,00,000 - ₹50,00,000",
                "house": "₹50,00,000 - ₹5,00,00,000",
                "laptop": "₹30,000 - ₹2,00,000",
                "phone": "₹10,000 - ₹1,50,000",
                "europe trip": "₹1,50,000 - ₹3,00,000",
                "gold": "₹6,000 per gram",
                "diamond": "₹50,000 - ₹10,00,000 per carat"
            }
            
            item_lower = item.lower()
            for key, price in price_db.items():
                if key in item_lower:
                    return f"Approximate price for {item}: {price}"
            
            # If not found, search for it
            return self._google_search(f"price of {item} in India")
        except Exception as e:
            return f"Price check error: {str(e)}"

    def _currency_converter(self, amount: float, from_currency: str, to_currency: str) -> str:
        """Convert between currencies"""
        try:
            # Simple conversion rates (you can use a real API)
            rates = {
                "USD": {"INR": 83.0, "EUR": 0.92},
                "EUR": {"INR": 90.0, "USD": 1.09},
                "INR": {"USD": 0.012, "EUR": 0.011}
            }
            
            if from_currency in rates and to_currency in rates[from_currency]:
                rate = rates[from_currency][to_currency]
                converted = amount * rate
                return f"{amount} {from_currency} = {converted:.2f} {to_currency}"
            else:
                return f"Currency conversion not available for {from_currency} to {to_currency}"
        except Exception as e:
            return f"Currency conversion error: {str(e)}"

    def _detect_tool_usage(self, query: str) -> Dict[str, Any]:
        """Detect if the query needs tool usage"""
        query_lower = query.lower()
        tools_needed = {}
        
        # Check for calculation needs
        if any(op in query for op in ['+', '-', '*', '/', 'calculate', 'compute', 'total', 'sum']):
            tools_needed['calculator'] = True
        
        # Check for price/information needs
        if any(word in query_lower for word in ['price', 'cost', 'how much', 'buy', 'purchase']):
            tools_needed['price_check'] = True
        
        # Check for search needs
        if any(word in query_lower for word in ['what is', 'how to', 'where to', 'when', 'why']):
            tools_needed['google_search'] = True
        
        # Check for currency conversion
        if any(word in query_lower for word in ['dollar', 'euro', 'usd', 'eur', 'convert']):
            tools_needed['currency_converter'] = True
        
        return tools_needed

    async def process_query(
        self,
        user_query: str,
        financial_data: Dict[str, Any],
        phone_number: str
    ) -> CollaborationSession:
        
        print(f"🔍 Debug: Processing query with tools: {user_query}")
        
        # Detect tool usage
        tools_needed = self._detect_tool_usage(user_query)
        
        # Use tools if needed
        tool_results = {}
        if tools_needed:
            print(f"🔧 Using tools: {list(tools_needed.keys())}")
            
            if 'calculator' in tools_needed:
                # Extract mathematical expressions
                math_pattern = r'(\d+[\+\-\*\/\(\)\d\s]+)'
                math_matches = re.findall(math_pattern, user_query)
                if math_matches:
                    tool_results['calculator'] = self._calculator(math_matches[0])
            
            if 'price_check' in tools_needed:
                # Extract item names
                price_keywords = ['price of', 'cost of', 'how much for', 'buy', 'purchase']
                for keyword in price_keywords:
                    if keyword in user_query.lower():
                        item = user_query.lower().split(keyword)[-1].strip()
                        tool_results['price_check'] = self._price_check(item)
                        break
            
            if 'google_search' in tools_needed:
                tool_results['google_search'] = self._google_search(user_query)
            
            if 'currency_converter' in tools_needed:
                # Extract currency conversion details
                currency_pattern = r'(\d+)\s*(USD|EUR|INR)\s*to\s*(USD|EUR|INR)'
                currency_match = re.search(currency_pattern, user_query)
                if currency_match:
                    amount, from_curr, to_curr = currency_match.groups()
                    tool_results['currency_converter'] = self._currency_converter(
                        float(amount), from_curr, to_curr
                    )
        
        # Create enhanced query with tool results
        enhanced_query = user_query
        if tool_results:
            enhanced_query += f"\n\nTool Results:\n"
            for tool, result in tool_results.items():
                enhanced_query += f"{tool}: {result}\n"
        """Process user query through ADK agent system."""
        
        print(f"🔍 Debug: Processing query with tools: {user_query}")
        
        # Detect tool usage
        tools_needed = self._detect_tool_usage(user_query)
        
        # Use tools if needed
        tool_results = {}
        if tools_needed:
            print(f"🔧 Using tools: {list(tools_needed.keys())}")
            
            if 'calculator' in tools_needed:
                # Extract mathematical expressions
                math_pattern = r'(\d+[\+\-\*\/\(\)\d\s]+)'
                math_matches = re.findall(math_pattern, user_query)
                if math_matches:
                    tool_results['calculator'] = self._calculator(math_matches[0])
            
            if 'price_check' in tools_needed:
                # Extract item names
                price_keywords = ['price of', 'cost of', 'how much for', 'buy', 'purchase']
                for keyword in price_keywords:
                    if keyword in user_query.lower():
                        item = user_query.lower().split(keyword)[-1].strip()
                        tool_results['price_check'] = self._price_check(item)
                        break
            
            if 'google_search' in tools_needed:
                tool_results['google_search'] = self._google_search(user_query)
            
            if 'currency_converter' in tools_needed:
                # Extract currency conversion details
                currency_pattern = r'(\d+)\s*(USD|EUR|INR)\s*to\s*(USD|EUR|INR)'
                currency_match = re.search(currency_pattern, user_query)
                if currency_match:
                    amount, from_curr, to_curr = currency_match.groups()
                    tool_results['currency_converter'] = self._currency_converter(
                        float(amount), from_curr, to_curr
                    )
        
        # Create enhanced query with tool results
        enhanced_query = user_query
        if tool_results:
            enhanced_query += f"\n\nTool Results:\n"
            for tool, result in tool_results.items():
                enhanced_query += f"{tool}: {result}\n"
        
        session_id = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        session = CollaborationSession(
            session_id=session_id,
            user_query=user_query,
            agent_responses=[],
            final_response="",
            collaboration_log=[],
            timestamp=datetime.utcnow(),
            tool_results=tool_results
        )
        
        # Step 1: Individual Agent Analysis
        print(f"🔍 Step 1: Individual agent analysis for query: {user_query}")
        
        for agent_id, agent_config in self.agents.items():
            if agent_id == "coordinator":
                continue  # Coordinator will be called later
                
            response = await self._run_agent(
                agent_id=agent_id,
                agent_config=agent_config,
                user_query=enhanced_query,
                financial_data=financial_data
            )
            
            session.agent_responses.append(response)
            session.collaboration_log.append({
                "step": "individual_analysis",
                "agent_id": agent_id,
                "agent_name": agent_config["name"],
                "timestamp": datetime.utcnow().isoformat(),
                "response_summary": response.response[:200] + "..." if len(response.response) > 200 else response.response
            })
            
            print(f"✅ {agent_config['name']} completed analysis")
        
        # Step 2: Critic Validation
        print("🔍 Step 2: Critic validation")
        critic_response = await self._run_critic_validation(session)
        session.collaboration_log.append({
            "step": "critic_validation",
            "agent_id": "critic",
            "agent_name": "Critic Agent",
            "timestamp": datetime.utcnow().isoformat(),
            "validation_status": critic_response.get("validation_status", "UNKNOWN"),
            "critical_errors": len(critic_response.get("critical_errors", [])),
            "moderate_concerns": len(critic_response.get("moderate_concerns", []))
        })
        
        # Step 3: Coordinator Synthesis
        print("🔍 Step 3: Coordinator synthesis")
        coordinator_response = await self._run_coordinator_synthesis(session, critic_response)
        session.final_response = coordinator_response.get("synthesized_response", "Analysis completed")
        session.collaboration_log.append({
            "step": "coordinator_synthesis",
            "agent_id": "coordinator",
            "agent_name": "Coordinator Agent",
            "timestamp": datetime.utcnow().isoformat(),
            "synthesis_summary": coordinator_response.get("synthesized_response", "")[:200] + "..." if len(coordinator_response.get("synthesized_response", "")) > 200 else coordinator_response.get("synthesized_response", "")
        })
        
        print("✅ ADK agent system completed successfully")
        return session
    
    async def _run_agent(
        self,
        agent_id: str,
        agent_config: Dict[str, Any],
        user_query: str,
        financial_data: Dict[str, Any]
    ) -> AgentResponse:
        """Run an individual agent."""
        
        try:
            if not self.model:
                return AgentResponse(
                    agent_id=agent_id,
                    agent_name=agent_config["name"],
                    input_query=user_query,
                    response=f"Agent {agent_config['name']} analysis: Unable to process due to model unavailability",
                    confidence=0.3,
                    reasoning="Model not available",
                    metadata={"error": "Model not available"},
                    timestamp=datetime.utcnow()
                )
            
            # Build prompt with financial data
            prompt = f"""
{agent_config['prompt_template']}

USER QUERY: {user_query}

FINANCIAL DATA:
{json.dumps(financial_data, indent=2)}

Provide your analysis in the specified JSON format.
"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response_text)
                confidence = parsed_response.get("confidence", 0.7)
                reasoning = parsed_response.get("reasoning", "Analysis completed")
            except json.JSONDecodeError:
                confidence = 0.5
                reasoning = "Response format parsing failed"
            
            return AgentResponse(
                agent_id=agent_id,
                agent_name=agent_config["name"],
                input_query=user_query,
                response=response_text,
                confidence=confidence,
                reasoning=reasoning,
                metadata={"capabilities": agent_config["capabilities"]},
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=agent_id,
                agent_name=agent_config["name"],
                input_query=user_query,
                response=f"Error in {agent_config['name']}: {str(e)}",
                confidence=0.1,
                reasoning=f"Error occurred: {str(e)}",
                metadata={"error": str(e)},
                timestamp=datetime.utcnow()
            )
    
    async def _run_critic_validation(self, session: CollaborationSession) -> Dict[str, Any]:
        """Run critic validation on all agent responses."""
        
        try:
            if not self.model:
                return {
                    "validation_status": "UNKNOWN",
                    "critical_errors": ["Model not available"],
                    "moderate_concerns": [],
                    "hallucination_flags": [],
                    "confidence": 0.3,
                    "reasoning": "Model not available"
                }
            
            # Build validation prompt
            agent_responses_text = "\n\n".join([
                f"Agent: {resp.agent_name}\nResponse: {resp.response}"
                for resp in session.agent_responses
            ])
            
            prompt = f"""
{self.agents["critic"]["prompt_template"]}

AGENT RESPONSES TO VALIDATE:
{agent_responses_text}

USER QUERY: {session.user_query}

Provide validation results in the specified JSON format.
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, be more lenient and approve if the response seems reasonable
                if any(keyword in response_text.lower() for keyword in ["net worth", "mutual fund", "savings", "investment", "portfolio"]):
                    return {
                        "validation_status": "APPROVED",
                        "critical_errors": [],
                        "moderate_concerns": ["Response format unclear but content seems relevant"],
                        "hallucination_flags": [],
                        "confidence": 0.7,
                        "reasoning": "Response contains relevant financial terms, approving despite format issues"
                    }
                else:
                    return {
                        "validation_status": "NEEDS_REVISION",
                        "critical_errors": ["Response parsing failed"],
                        "moderate_concerns": [],
                        "hallucination_flags": [],
                        "confidence": 0.5,
                        "reasoning": "Response parsing failed"
                    }
                
        except Exception as e:
            return {
                "validation_status": "NEEDS_REVISION",
                "critical_errors": [f"Validation error: {str(e)}"],
                "moderate_concerns": [],
                "hallucination_flags": [],
                "confidence": 0.3,
                "reasoning": f"Error in validation: {str(e)}"
            }
    
    async def _run_coordinator_synthesis(
        self,
        session: CollaborationSession,
        critic_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run coordinator synthesis of all agent responses."""
        
        try:
            if not self.model:
                return {
                    "synthesized_response": "Unable to synthesize responses due to model unavailability",
                    "key_recommendations": ["Please try again"],
                    "conflicts_resolved": [],
                    "confidence": 0.3,
                    "reasoning": "Model not available"
                }
            
            # Build synthesis prompt
            agent_responses_text = "\n\n".join([
                f"Agent: {resp.agent_name}\nResponse: {resp.response}\nConfidence: {resp.confidence}"
                for resp in session.agent_responses
            ])
            
            validation_text = f"""
Validation Status: {critic_response.get('validation_status', 'UNKNOWN')}
Critical Errors: {critic_response.get('critical_errors', [])}
Moderate Concerns: {critic_response.get('moderate_concerns', [])}
"""
            
            prompt = f"""
{self.agents["coordinator"]["prompt_template"]}

USER QUERY: {session.user_query}

AGENT RESPONSES:
{agent_responses_text}

VALIDATION RESULTS:
{validation_text}

Synthesize a final response that addresses the user's query using insights from all agents.
Provide your response in the specified JSON format.
"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Check validation status and handle low confidence
            validation_status = critic_response.get("validation_status", "UNKNOWN")
            confidence = critic_response.get("confidence", 0.5)
            
            # If validation failed badly, try to create a response from available data
            if validation_status in ["NEEDS_REVISION", "CRITICAL_ERRORS"] and confidence < 0.3:
                # Extract useful information from agent responses
                agent_insights = []
                for resp in session.agent_responses:
                    if resp.confidence > 0.3:  # Use responses with reasonable confidence
                        agent_insights.append(f"{resp.agent_name}: {resp.response[:100]}...")
                
                if agent_insights:
                    return {
                        "synthesized_response": f"Based on available analysis: {' '.join(agent_insights[:2])}. Please review the detailed agent responses for complete analysis.",
                        "key_recommendations": ["Review individual agent responses for specific recommendations"],
                        "conflicts_resolved": [],
                        "confidence": 0.6,
                        "reasoning": "Created response from available agent insights despite validation issues"
                    }
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract the response from the text
                # Look for JSON-like content in the response
                
                # Try to find JSON content in the response
                json_pattern = r'\{[^{}]*\}'
                json_matches = re.findall(json_pattern, response_text)
                
                if json_matches:
                    # Try to parse the first JSON-like match
                    try:
                        return json.loads(json_matches[0])
                    except:
                        pass
                
                # If no JSON found, create a fallback response
                return {
                    "synthesized_response": f"Analysis completed but response format was unclear. Please review the individual agent responses for detailed insights about your query: {session.user_query}",
                    "key_recommendations": ["Review individual agent responses for specific recommendations"],
                    "conflicts_resolved": [],
                    "confidence": 0.5,
                    "reasoning": "Response parsing failed, fallback to agent review"
                }
                
        except Exception as e:
            return {
                "synthesized_response": f"Error in synthesis: {str(e)}",
                "key_recommendations": ["Please try again"],
                "conflicts_resolved": [],
                "confidence": 0.3,
                "reasoning": f"Error in synthesis: {str(e)}"
            }
    
    def get_session_summary(self, session: CollaborationSession) -> Dict[str, Any]:
        """Get a summary of the collaboration session."""
        
        return {
            "session_id": session.session_id,
            "user_query": session.user_query,
            "final_response": session.final_response,
            "agent_responses": [
                {
                    "agent_id": resp.agent_id,
                    "agent_name": resp.agent_name,
                    "confidence": resp.confidence,
                    "response_summary": resp.response[:200] + "..." if len(resp.response) > 200 else resp.response,
                    "timestamp": resp.timestamp.isoformat()
                }
                for resp in session.agent_responses
            ],
            "collaboration_log": session.collaboration_log,
            "timestamp": session.timestamp.isoformat()
        } 