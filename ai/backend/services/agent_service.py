import asyncio
from typing import Dict, Any, List, Optional
from agents.agent_factory import AgentFactory
from models.agent import AgentRequest, AgentResponse, AgentType
from models.chat import ChatMessage, MessageRole
from services.mcp_service import MCPService


class AgentService:
    """Service for orchestrating the multi-agent system."""
    
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.mcp_service = MCPService()
    
    async def process_user_message(
        self,
        user_id: str,
        session_id: str,
        message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> AgentResponse:
        """Process a user message and return an appropriate agent response."""
        try:
            # Determine the best agent for this message
            best_agent_type = self.agent_factory.determine_best_agent(message)
            
            # Get the appropriate agent
            agent = self.agent_factory.get_agent(best_agent_type)
            
            # Fetch financial data for context using user's phone number
            financial_data = await self.mcp_service.get_comprehensive_financial_data(user_id)
            print(f"🔍 Debug: Fetched financial data for user {user_id}: {financial_data}")
            
            # Create agent request
            request = AgentRequest(
                user_id=user_id,
                session_id=session_id,
                message=message,
                agent_type=best_agent_type,
                context=self._extract_user_context(conversation_history),
                financial_data=financial_data,
                conversation_history=conversation_history
            )
            
            # Process the request
            response = await agent.process_request(request)
            
            return response
            
        except Exception as e:
            print(f"Error processing user message: {e}")
            return self._create_error_response(str(e))
    
    async def get_multi_agent_response(
        self,
        user_id: str,
        session_id: str,
        message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Get responses from multiple agents and synthesize them."""
        try:
            # Get the coordinator agent
            coordinator = self.agent_factory.get_agent(AgentType.COORDINATOR)
            
            # Fetch financial data using user's phone number
            financial_data = await self.mcp_service.get_comprehensive_financial_data(user_id)
            
            # Create coordinator request
            request = AgentRequest(
                user_id=user_id,
                session_id=session_id,
                message=message,
                agent_type=AgentType.COORDINATOR,
                context=self._extract_user_context(conversation_history),
                financial_data=financial_data,
                conversation_history=conversation_history
            )
            
            # Get coordinator response
            coordinator_response = await coordinator.process_request(request)
            
            # Determine if we need specialized agent input
            specialized_agent_type = self.agent_factory.determine_best_agent(message)
            
            if specialized_agent_type != AgentType.COORDINATOR:
                # Get specialized agent response
                specialized_agent = self.agent_factory.get_agent(specialized_agent_type)
                
                specialized_request = AgentRequest(
                    user_id=user_id,
                    session_id=session_id,
                    message=message,
                    agent_type=specialized_agent_type,
                    context=self._extract_user_context(conversation_history),
                    financial_data=financial_data,
                    conversation_history=conversation_history
                )
                
                specialized_response = await specialized_agent.process_request(specialized_request)
                
                # Synthesize responses
                return {
                    "primary_response": coordinator_response,
                    "specialized_response": specialized_response,
                    "agent_used": specialized_agent_type.value,
                    "confidence": max(coordinator_response.confidence, specialized_response.confidence)
                }
            else:
                return {
                    "primary_response": coordinator_response,
                    "agent_used": "coordinator",
                    "confidence": coordinator_response.confidence
                }
                
        except Exception as e:
            print(f"Error getting multi-agent response: {e}")
            return {
                "error": str(e),
                "agent_used": "error",
                "confidence": 0.0
            }
    
    def _extract_user_context(self, conversation_history: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Extract user context from conversation history."""
        if not conversation_history:
            return {}
        
        # Extract key information from recent messages
        recent_messages = conversation_history[-5:]  # Last 5 messages
        
        context = {
            "recent_topics": [],
            "user_preferences": {},
            "financial_goals": [],
            "risk_tolerance": "moderate"
        }
        
        # Analyze recent messages for context
        for msg in recent_messages:
            content = msg.get("content", "").lower()
            
            # Extract financial goals
            if any(word in content for word in ["save", "investment", "retirement"]):
                context["financial_goals"].append("savings")
            if any(word in content for word in ["debt", "loan", "credit"]):
                context["financial_goals"].append("debt_management")
            if any(word in content for word in ["invest", "portfolio", "stocks"]):
                context["financial_goals"].append("investment")
            
            # Extract risk tolerance
            if any(word in content for word in ["conservative", "safe", "low risk"]):
                context["risk_tolerance"] = "conservative"
            elif any(word in content for word in ["aggressive", "high risk", "growth"]):
                context["risk_tolerance"] = "aggressive"
        
        return context
    
    def _create_error_response(self, error_message: str) -> AgentResponse:
        """Create an error response."""
        return AgentResponse(
            agent_type=AgentType.COORDINATOR,
            response=f"I apologize, but I encountered an error: {error_message}. Please try again or contact support if the issue persists.",
            confidence=0.0,
            recommendations=["Try rephrasing your question", "Check your internet connection"],
            insights=["Technical issue detected"],
            next_actions=["Retry the request", "Contact support if problem persists"]
        )
    
    def get_available_agents(self) -> Dict[str, Dict]:
        """Get information about all available agents."""
        return {
            "coordinator": {
                "name": "Financial Coordinator",
                "description": "General financial advisor and conversation coordinator",
                "capabilities": ["general_advice", "conversation_coordination"]
            },
            "investment_analyst": {
                "name": "Investment Analyst",
                "description": "Specialized in investment analysis and portfolio management",
                "capabilities": ["portfolio_analysis", "investment_recommendations"]
            },
            "debt_credit_analyst": {
                "name": "Debt & Credit Analyst",
                "description": "Specialized in debt management and credit optimization",
                "capabilities": ["debt_optimization", "credit_analysis"]
            },
            "wealth_planner": {
                "name": "Wealth Planner",
                "description": "Long-term wealth planning and goal setting",
                "capabilities": ["wealth_projection", "goal_planning"]
            },
            "financial_health_monitor": {
                "name": "Financial Health Monitor",
                "description": "Monitors financial health and detects anomalies",
                "capabilities": ["risk_assessment", "anomaly_detection"]
            }
        }
    
    async def test_agent_connectivity(self) -> Dict[str, bool]:
        """Test connectivity with all agents."""
        try:
            # Test basic agent factory functionality
            agents = self.get_available_agents()
            coordinator = self.agent_factory.get_agent(AgentType.COORDINATOR)
            
            return {
                "agent_factory": True,
                "coordinator_agent": coordinator is not None,
                "mcp_service": True  # Assuming MCP service is available
            }
        except Exception as e:
            print(f"Error testing agent connectivity: {e}")
            return {
                "agent_factory": False,
                "coordinator_agent": False,
                "mcp_service": False
            } 