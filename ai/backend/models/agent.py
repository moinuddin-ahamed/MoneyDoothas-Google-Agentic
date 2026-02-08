from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class AgentType(str, Enum):
    """Types of specialized agents."""
    COORDINATOR = "coordinator"
    INVESTMENT_ANALYST = "investment_analyst"
    DEBT_CREDIT_ANALYST = "debt_credit_analyst"
    WEALTH_PLANNER = "wealth_planner"
    FINANCIAL_HEALTH_MONITOR = "financial_health_monitor"


class AgentCapability(str, Enum):
    """Capabilities of different agents."""
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    DEBT_OPTIMIZATION = "debt_optimization"
    WEALTH_PROJECTION = "wealth_projection"
    RISK_ASSESSMENT = "risk_assessment"
    ANOMALY_DETECTION = "anomaly_detection"
    GOAL_PLANNING = "goal_planning"


class AgentRequest(BaseModel):
    """Request model for agent interactions."""
    
    user_id: str = Field(..., description="User identifier")
    session_id: str = Field(..., description="Chat session ID")
    message: str = Field(..., description="User message")
    agent_type: AgentType = Field(..., description="Type of agent to handle request")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    financial_data: Optional[Dict[str, Any]] = Field(default=None, description="Financial data")
    conversation_history: Optional[List[Dict[str, Any]]] = Field(default=None, description="Conversation history")
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class AgentResponse(BaseModel):
    """Response model for agent interactions."""
    
    agent_type: AgentType = Field(..., description="Type of agent that responded")
    response: str = Field(..., description="Agent response")
    confidence: float = Field(..., description="Confidence score (0-1)")
    recommendations: List[str] = Field(default=[], description="List of recommendations")
    insights: List[str] = Field(default=[], description="Key insights")
    data_points: Optional[Dict[str, Any]] = Field(default=None, description="Relevant data points")
    next_actions: List[str] = Field(default=[], description="Suggested next actions")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class AgentConfig(BaseModel):
    """Configuration for individual agents."""
    
    agent_type: AgentType = Field(..., description="Type of agent")
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    capabilities: List[AgentCapability] = Field(..., description="Agent capabilities")
    agent_model_config: Dict[str, Any] = Field(default={}, description="Model configuration")
    prompt_template: str = Field(..., description="Agent prompt template")
    temperature: float = Field(default=0.2, description="Model temperature")
    max_tokens: int = Field(default=4000, description="Maximum tokens")
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    } 