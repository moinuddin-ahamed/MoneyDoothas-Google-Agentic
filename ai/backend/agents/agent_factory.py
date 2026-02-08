from typing import Dict, Type
from models.agent import AgentType
from .base_agent import BaseAgent
from .coordinator_agent import CoordinatorAgent
from .investment_agent import InvestmentAgent
from .cash_flow_agent import CashFlowAgent
from .critic_agent import CriticAgent
from .wealth_planner_agent import WealthPlannerAgent
from .debt_agent import DebtCreditAgent
from .health_agent import FinancialHealthAgent


class AgentFactory:
    """Factory class for creating and managing different types of agents."""
    
    def __init__(self):
        self._agents: Dict[AgentType, BaseAgent] = {}
        self._agent_classes: Dict[AgentType, Type[BaseAgent]] = {
            AgentType.COORDINATOR: CoordinatorAgent,
            AgentType.INVESTMENT_ANALYST: InvestmentAgent,
            AgentType.WEALTH_PLANNER: WealthPlannerAgent,
            AgentType.DEBT_CREDIT_ANALYST: DebtCreditAgent,
            AgentType.FINANCIAL_HEALTH_MONITOR: FinancialHealthAgent,
            # Note: New agents are managed by CollaborationEngine
        }
    
    def get_agent(self, agent_type: AgentType) -> BaseAgent:
        """Get or create an agent of the specified type."""
        if agent_type not in self._agents:
            if agent_type not in self._agent_classes:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            # Create the agent
            agent_class = self._agent_classes[agent_type]
            self._agents[agent_type] = agent_class()
        
        return self._agents[agent_type]
    
    def get_all_agents(self) -> Dict[AgentType, BaseAgent]:
        """Get all available agents."""
        # Ensure all agents are created
        for agent_type in self._agent_classes.keys():
            if agent_type not in self._agents:
                self.get_agent(agent_type)
        
        return self._agents.copy()
    
    def get_agent_by_capability(self, capability: str) -> BaseAgent:
        """Get the best agent for a specific capability."""
        # Map capabilities to agent types
        capability_to_agent = {
            'portfolio_analysis': AgentType.INVESTMENT_ANALYST,
            'debt_optimization': AgentType.DEBT_CREDIT_ANALYST,
            'wealth_projection': AgentType.WEALTH_PLANNER,
            'risk_assessment': AgentType.FINANCIAL_HEALTH_MONITOR,
            'anomaly_detection': AgentType.FINANCIAL_HEALTH_MONITOR,
            'goal_planning': AgentType.WEALTH_PLANNER,
        }
        
        agent_type = capability_to_agent.get(capability, AgentType.COORDINATOR)
        return self.get_agent(agent_type)
    
    def determine_best_agent(self, user_message: str) -> AgentType:
        """Determine the best agent to handle a user message."""
        message_lower = user_message.lower()
        
        # Investment-related keywords
        investment_keywords = [
            'investment', 'portfolio', 'sip', 'mutual fund', 'stocks', 'returns',
            'underperformed', 'market', 'fund', 'equity', 'debt fund'
        ]
        
        # Debt-related keywords
        debt_keywords = [
            'loan', 'debt', 'credit', 'emi', 'interest', 'afford', 'borrow',
            'mortgage', 'home loan', 'personal loan', 'credit card'
        ]
        
        # Wealth planning keywords
        wealth_keywords = [
            'net worth', 'networth', 'wealth', 'retirement', 'savings', 'goals', 'future',
            'projection', 'planning', 'financial plan', 'wealth building', 'money at 40'
        ]
        
        # Financial health keywords
        health_keywords = [
            'anomaly', 'unusual', 'spending', 'pattern', 'risk', 'health',
            'monitor', 'alert', 'warning', 'issue', 'stress'
        ]
        
        # Check for keyword matches
        if any(keyword in message_lower for keyword in investment_keywords):
            return AgentType.INVESTMENT_ANALYST
        elif any(keyword in message_lower for keyword in debt_keywords):
            return AgentType.DEBT_CREDIT_ANALYST
        elif any(keyword in message_lower for keyword in wealth_keywords):
            return AgentType.WEALTH_PLANNER
        elif any(keyword in message_lower for keyword in health_keywords):
            return AgentType.FINANCIAL_HEALTH_MONITOR
        else:
            return AgentType.COORDINATOR
    
    def get_agent_info(self) -> Dict[str, Dict]:
        """Get information about all available agents."""
        agent_info = {}
        
        for agent_type, agent in self.get_all_agents().items():
            agent_info[agent_type.value] = {
                'name': agent.name,
                'description': agent.description,
                'capabilities': agent.get_capabilities(),
                'temperature': agent.temperature,
                'max_tokens': agent.max_tokens
            }
        
        return agent_info
    
    def reset_agents(self):
        """Reset all agents (useful for testing or reinitialization)."""
        self._agents.clear()
    
    def is_agent_available(self, agent_type: AgentType) -> bool:
        """Check if an agent type is available."""
        return agent_type in self._agent_classes 