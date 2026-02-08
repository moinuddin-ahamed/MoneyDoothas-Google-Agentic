from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """Types of agent messages."""
    ANALYSIS = "analysis"
    CHALLENGE = "challenge"
    PROPOSAL = "proposal"
    CONSENSUS = "consensus"
    VALIDATION = "validation"
    REVISION_REQUEST = "revision_request"
    COORDINATION = "coordination"
    VISUAL_ENHANCEMENT = "visual_enhancement"


class ConfidenceLevel(str, Enum):
    """Confidence levels for agent responses."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationStatus(str, Enum):
    """Validation status for critic agent."""
    APPROVED = "APPROVED"
    REQUIRES_REVISION = "REQUIRES_REVISION"
    NEEDS_CLARIFICATION = "NEEDS_CLARIFICATION"


class AgentMessage(BaseModel):
    """Message structure for agent communication."""
    
    agent_id: str = Field(..., description="Agent identifier")
    message_type: MessageType = Field(..., description="Type of message")
    content: str = Field(..., description="Message content")
    supporting_data: Dict[str, Any] = Field(default={}, description="Supporting data and calculations")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence level")
    dependencies: List[str] = Field(default=[], description="Dependencies on other agents")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    validation_result: Optional[Dict[str, Any]] = Field(default=None, description="Validation result")
    iteration_round: Optional[int] = Field(default=None, description="Iteration round number")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ValidationError(BaseModel):
    """Validation error structure."""
    
    category: str = Field(..., description="Error category")
    description: str = Field(..., description="Error description")
    location: str = Field(..., description="Error location")
    impact: str = Field(..., description="Impact level (high/medium/low)")
    suggested_correction: str = Field(..., description="Suggested correction")


class HallucinationFlag(BaseModel):
    """Hallucination detection flag."""
    
    type: str = Field(..., description="Hallucination type")
    description: str = Field(..., description="Description of hallucination")
    severity: str = Field(..., description="Severity level (high/medium/low)")


class ValidationResult(BaseModel):
    """Validation result from critic agent."""
    
    validation_status: ValidationStatus = Field(..., description="Validation status")
    confidence_score: int = Field(..., description="Confidence score (0-100)")
    critical_errors: List[ValidationError] = Field(default=[], description="Critical errors")
    moderate_concerns: List[ValidationError] = Field(default=[], description="Moderate concerns")
    minor_suggestions: List[ValidationError] = Field(default=[], description="Minor suggestions")
    hallucination_flags: List[HallucinationFlag] = Field(default=[], description="Hallucination flags")
    overall_assessment: str = Field(..., description="Overall assessment")


class AgentCapability(str, Enum):
    """Agent capabilities."""
    CASH_FLOW_ANALYSIS = "cash_flow_analysis"
    INVESTMENT_ANALYSIS = "investment_analysis"
    DEBT_ANALYSIS = "debt_analysis"
    ASSET_ANALYSIS = "asset_analysis"
    RISK_ANALYSIS = "risk_analysis"
    DATA_AGGREGATION = "data_aggregation"
    PROFILE_COMPILATION = "profile_compilation"
    BUDGET_OPTIMIZATION = "budget_optimization"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    COORDINATION = "coordination"
    CONSENSUS_BUILDING = "consensus_building"
    VALIDATION = "validation"
    QUALITY_ASSURANCE = "quality_assurance"


class Agent(BaseModel):
    """Agent configuration model."""
    
    id: str = Field(..., description="Agent identifier")
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    capabilities: List[AgentCapability] = Field(..., description="Agent capabilities")
    specialties: List[str] = Field(..., description="Agent specialties")
    color: str = Field(..., description="Agent color for UI")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CollaborativeSession(BaseModel):
    """Collaborative session model."""
    
    session_id: str = Field(..., description="Session identifier")
    user_query: str = Field(..., description="User's original query")
    participating_agents: List[Agent] = Field(..., description="Participating agents")
    agent_messages: List[AgentMessage] = Field(default=[], description="Agent messages")
    phase: str = Field(..., description="Current phase")
    final_recommendation: Optional[str] = Field(default=None, description="Final recommendation")
    context: Dict[str, Any] = Field(default={}, description="Session context")
    current_iteration: int = Field(default=1, description="Current iteration")
    max_iterations: int = Field(default=4, description="Maximum iterations")
    validation_history: List[ValidationResult] = Field(default=[], description="Validation history")
    final_validation: Optional[ValidationResult] = Field(default=None, description="Final validation")
    visual_presentation: Optional[Dict[str, Any]] = Field(default=None, description="Visual presentation")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentAnalysisResult(BaseModel):
    """Result from agent analysis."""
    
    agent_id: str = Field(..., description="Agent identifier")
    analysis: str = Field(..., description="Analysis content")
    recommendations: List[str] = Field(default=[], description="Recommendations")
    insights: List[str] = Field(default=[], description="Key insights")
    calculations: Dict[str, Any] = Field(default={}, description="Supporting calculations")
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    dependencies: List[str] = Field(default=[], description="Dependencies on other domains")
    risks: List[str] = Field(default=[], description="Identified risks")
    opportunities: List[str] = Field(default=[], description="Identified opportunities")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ConsensusResult(BaseModel):
    """Result from consensus building."""
    
    consensus_achieved: bool = Field(..., description="Whether consensus was achieved")
    final_recommendation: str = Field(..., description="Final recommendation")
    action_plan: Dict[str, Any] = Field(..., description="Action plan")
    timeline: Dict[str, str] = Field(..., description="Timeline for actions")
    monitoring_metrics: List[str] = Field(default=[], description="Metrics to monitor")
    risk_assessment: str = Field(..., description="Overall risk assessment")
    confidence_level: ConfidenceLevel = Field(..., description="Overall confidence level")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 