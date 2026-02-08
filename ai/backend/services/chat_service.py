import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from models.chat import ChatMessage, ChatSession, UserContext, PhoneNumberUser, MessageRole
from models.agent import AgentResponse
from services.agent_service import AgentService
from services.mcp_service import MCPService
from services.firestore_service import FirestoreService


class ChatService:
    """Service for managing chat sessions and integrating with existing frontend."""
    
    def __init__(self):
        self.agent_service = AgentService()
        self.mcp_service = MCPService()
        self.firestore_service = FirestoreService()
    
    async def process_chat_message(
        self,
        phone_number: str,
        message: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a chat message and return response for your existing frontend."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Generate session ID if not provided
            if not session_id:
                session = self.firestore_service.create_session(phone_number)
                session_id = session.session_id
            else:
                # Verify session exists and belongs to user
                session = self.firestore_service.get_session(session_id)
                if not session or session.phone_number != phone_number:
                    # Create new session if invalid
                    session = self.firestore_service.create_session(phone_number)
                    session_id = session.session_id
            
            # Get conversation history
            conversation_history = self.firestore_service.get_conversation_history(session_id)
            
            # Process the message with the agent system
            agent_response = await self.agent_service.process_user_message(
                user_id=phone_number,  # Use phone number as user_id
                session_id=session_id,
                message=message,
                conversation_history=conversation_history
            )
            
            # Save the conversation
            await self._save_conversation(phone_number, session_id, message, agent_response)
            
            # Format response for your existing frontend
            return {
                "success": True,
                "session_id": session_id,
                "phone_number": phone_number,
                "response": {
                    "message": agent_response.response,
                    "agent_type": agent_response.agent_type.value,
                    "confidence": agent_response.confidence,
                    "recommendations": agent_response.recommendations,
                    "insights": agent_response.insights,
                    "next_actions": agent_response.next_actions,
                    "timestamp": agent_response.timestamp.isoformat()
                },
                "metadata": {
                    "agent_used": agent_response.agent_type.value,
                    "processing_time": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            print(f"Error processing chat message: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id,
                "phone_number": phone_number,
                "response": {
                    "message": "I apologize, but I encountered an error processing your request. Please try again.",
                    "agent_type": "coordinator",
                    "confidence": 0.0,
                    "recommendations": ["Please try again"],
                    "insights": [],
                    "next_actions": ["Retry the request"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
    
    async def get_multi_agent_response(
        self,
        phone_number: str,
        message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get response from multiple agents for complex queries."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Generate session ID if not provided
            if not session_id:
                session = self.firestore_service.create_session(phone_number)
                session_id = session.session_id
            else:
                # Verify session exists and belongs to user
                session = self.firestore_service.get_session(session_id)
                if not session or session.phone_number != phone_number:
                    # Create new session if invalid
                    session = self.firestore_service.create_session(phone_number)
                    session_id = session.session_id
            
            conversation_history = self.firestore_service.get_conversation_history(session_id)
            
            # Get multi-agent response
            response = await self.agent_service.get_multi_agent_response(
                user_id=phone_number,  # Use phone number as user_id
                session_id=session_id,
                message=message,
                conversation_history=conversation_history
            )
            
            # Save conversation
            if "primary_response" in response:
                await self._save_conversation(phone_number, session_id, message, response["primary_response"])
            
            return {
                "success": True,
                "session_id": session_id,
                "phone_number": phone_number,
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting multi-agent response: {e}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id,
                "phone_number": phone_number,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def create_new_session(self, phone_number: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Create a new chat session for a user."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Create new session
            session = self.firestore_service.create_session(phone_number, title)
            
            return {
                "success": True,
                "session": session.dict()
            }
            
        except Exception as e:
            print(f"Error creating session: {e}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number
            }
    
    async def get_user_sessions(self, phone_number: str, active_only: bool = True) -> Dict[str, Any]:
        """Get all chat sessions for a user."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Get user sessions
            sessions = self.firestore_service.get_user_sessions(phone_number, active_only)
            
            return {
                "success": True,
                "phone_number": phone_number,
                "sessions": [session.dict() for session in sessions],
                "total_sessions": len(sessions)
            }
            
        except Exception as e:
            print(f"Error getting user sessions: {e}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number
            }
    
    async def get_session_details(self, phone_number: str, session_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific chat session."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Get session
            session = self.firestore_service.get_session(session_id)
            
            if not session:
                return {
                    "success": False,
                    "error": "Session not found",
                    "phone_number": phone_number,
                    "session_id": session_id
                }
            
            # Verify session belongs to user
            if session.phone_number != phone_number:
                return {
                    "success": False,
                    "error": "Access denied",
                    "phone_number": phone_number,
                    "session_id": session_id
                }
            
            # Get session messages
            messages = self.firestore_service.get_session_messages(session_id)
            
            # Get user context
            context = self.firestore_service.get_or_create_user_context(phone_number)
            
            return {
                "success": True,
                "session": {
                    **session.dict(),
                    "messages": [msg.dict() for msg in messages],
                    "context": context.dict() if context else None,
                    "metadata": {
                        "total_messages": len(messages),
                        "last_updated": session.updated_at.isoformat()
                    }
                }
            }
            
        except Exception as e:
            print(f"Error getting session details: {e}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number,
                "session_id": session_id
            }
    
    async def deactivate_session(self, phone_number: str, session_id: str) -> Dict[str, Any]:
        """Deactivate a chat session."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Get session
            session = self.firestore_service.get_session(session_id)
            
            if not session:
                return {
                    "success": False,
                    "error": "Session not found",
                    "phone_number": phone_number,
                    "session_id": session_id
                }
            
            # Verify session belongs to user
            if session.phone_number != phone_number:
                return {
                    "success": False,
                    "error": "Access denied",
                    "phone_number": phone_number,
                    "session_id": session_id
                }
            
            # Deactivate session
            success = self.firestore_service.deactivate_session(session_id, phone_number)
            
            return {
                "success": success,
                "session_id": session_id,
                "phone_number": phone_number,
                "message": "Session deactivated successfully" if success else "Failed to deactivate session"
            }
            
        except Exception as e:
            print(f"Error deactivating session: {e}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number,
                "session_id": session_id
            }
    
    async def get_user_stats(self, phone_number: str) -> Dict[str, Any]:
        """Get user statistics."""
        try:
            # Create or get user
            user = self.firestore_service.create_or_get_user(phone_number)
            
            # Get user stats
            stats = self.firestore_service.get_user_stats(phone_number)
            
            return {
                "success": True,
                "stats": stats
            }
            
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number
            }
    
    async def _save_conversation(
        self,
        phone_number: str,
        session_id: str,
        user_message: str,
        agent_response: AgentResponse
    ):
        """Save conversation to Firestore."""
        try:
            # Create user message
            user_msg = ChatMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                phone_number=phone_number,
                role=MessageRole.USER,
                content=user_message
            )
            
            # Create agent message
            agent_msg = ChatMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                phone_number=phone_number,
                role=MessageRole.ASSISTANT,
                content=agent_response.response,
                message_type="analysis" if agent_response.insights else "text"
            )
            
            # Save messages to Firestore
            self.firestore_service.save_message(user_msg)
            self.firestore_service.save_message(agent_msg)
            
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    async def get_financial_context(self, phone_number: str) -> Dict[str, Any]:
        """Get financial context for the user."""
        try:
            financial_data = await self.mcp_service.get_comprehensive_financial_data()
            return {
                "success": True,
                "phone_number": phone_number,
                "financial_data": financial_data,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Error getting financial context: {e}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number,
                "timestamp": datetime.utcnow().isoformat()
            } 