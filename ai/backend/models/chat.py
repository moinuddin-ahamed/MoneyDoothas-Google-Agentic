from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """Message roles in the conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Types of messages in the conversation."""
    TEXT = "text"
    FINANCIAL_DATA = "financial_data"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"


class ChatMessage(BaseModel):
    """Individual chat message model."""
    
    id: str = Field(..., description="Unique message ID")
    session_id: str = Field(..., description="Chat session ID")
    phone_number: str = Field(..., description="User's phone number")
    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    message_type: MessageType = Field(default=MessageType.TEXT, description="Message type")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserContext(BaseModel):
    """User context and preferences."""
    
    phone_number: str = Field(..., description="User's phone number")
    financial_goals: List[str] = Field(default=[], description="User's financial goals")
    risk_tolerance: str = Field(default="moderate", description="User's risk tolerance")
    investment_horizon: str = Field(default="medium", description="Investment time horizon")
    preferred_currencies: List[str] = Field(default=["INR"], description="Preferred currencies")
    notification_preferences: Dict[str, bool] = Field(default={}, description="Notification settings")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Context creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ChatSession(BaseModel):
    """Chat session model."""
    
    session_id: str = Field(..., description="Unique session ID")
    phone_number: str = Field(..., description="User's phone number")
    title: str = Field(..., description="Session title")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    messages: List[ChatMessage] = Field(default=[], description="Session messages")
    context: Optional[UserContext] = Field(default=None, description="User context")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Session metadata")
    is_active: bool = Field(default=True, description="Whether session is active")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PhoneNumberUser(BaseModel):
    """User model based on phone number."""
    
    phone_number: str = Field(..., description="User's phone number")
    name: Optional[str] = Field(default=None, description="User's name")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="User creation time")
    last_active: datetime = Field(default_factory=datetime.utcnow, description="Last activity time")
    total_sessions: int = Field(default=0, description="Total number of sessions created")
    active_sessions: int = Field(default=0, description="Number of active sessions")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="User metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 