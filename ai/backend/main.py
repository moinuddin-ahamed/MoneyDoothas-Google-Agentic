import asyncio
import uuid
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.chat import ChatMessage, ChatSession, UserContext, MessageRole, MessageType
from models.agent import AgentRequest, AgentResponse, AgentType
from services.agent_service import AgentService
from services.mcp_service import MCPService
from services.chat_service import ChatService
from services.collaboration_engine import CollaborationEngine
from services.firestore_service import FirestoreService
from adk_agent_system import ADKAgentSystem

from firebase_admin import firestore

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="FiMoney AI Agent API",
    description="Multi-agent AI system for personalized financial insights with phone number-based user management",
    version="2.0.0"
)

# Initialize services
agent_service = AgentService()
mcp_service = MCPService()
chat_service = ChatService()
collaboration_engine = CollaborationEngine()

# Initialize ADK system
adk_system = ADKAgentSystem()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "FiMoney AI Agent API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Phone number-based user management",
            "Multiple chat sessions per user",
            "Firestore data persistence",
            "Multi-agent financial analysis",
            "Context-aware conversations",
            "Collaborative agent coordination"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test agent connectivity
        connectivity = await agent_service.test_agent_connectivity()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "connectivity": connectivity
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@app.get("/agents")
async def get_agents():
    """Get information about all available agents."""
    try:
        agents = agent_service.get_available_agents()
        return {
            "agents": agents,
            "total_agents": len(agents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agents: {str(e)}")


@app.get("/api/v1/collaborative/agents")
async def get_collaborative_agents():
    """Get information about all collaborative ADK agents."""
    try:
        agents_status = await collaboration_engine.get_agent_status()
        return {
            "success": True,
            "agents": agents_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting collaborative agents: {str(e)}")


@app.get("/api/v1/collaborative/health")
async def collaborative_health_check():
    """Health check for the collaborative system."""
    try:
        health_status = await collaboration_engine.test_collaboration()
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "details": health_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking collaborative health: {str(e)}")


@app.post("/api/v1/chat")
async def chat_endpoint(
    phone_number: str,
    message: str,
    session_id: Optional[str] = None
):
    """Process a chat message and return agent response."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Check if it's a simple greeting
        simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if message.lower().strip() in simple_greetings:
            # Provide a simple, friendly response for greetings
            return {
                "success": True,
                "session_id": session_id,
                "phone_number": phone_number,
                "response": {
                    "message": "Hi there! I'm your financial assistant. How can I help you today? You can ask me about your investments, savings, budgeting, or any financial questions you have.",
                    "agent_type": "assistant",
                    "confidence": 1.0,
                    "recommendations": [],
                    "insights": [],
                    "next_actions": [],
                    "timestamp": datetime.utcnow().isoformat()
                },
                "metadata": {
                    "processing_type": "simple_greeting",
                    "confidence_score": 1.0,
                    "processing_timestamp": datetime.utcnow().isoformat()
                }
            }
        
        # Use the improved collaboration engine for financial queries
        response = await collaboration_engine.process_user_query(
            user_query=message,
            phone_number=phone_number
        )
        
        if response["success"]:
            # Format response for frontend compatibility
            formatted_response = {
                "success": True,
                "session_id": response.get("metadata", {}).get("session_id", session_id),
                "phone_number": phone_number,
                "response": {
                    "message": response["response"],
                    "agent_type": "coordinator",
                    "confidence": response.get("metadata", {}).get("confidence_score", 0.8),
                    "recommendations": response.get("recommendations", []),
                    "insights": response.get("agent_insights", []),
                    "next_actions": [],
                    "timestamp": response.get("metadata", {}).get("processing_timestamp", datetime.utcnow().isoformat())
                },
                "metadata": response.get("metadata", {}),
                "validation": response.get("validation", {}),
                "statistics": response.get("statistics", {}),
                "risks_and_opportunities": response.get("risks_and_opportunities", {})
            }
            return formatted_response
        else:
            raise HTTPException(status_code=500, detail=response.get("error", "Unknown error"))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/api/v1/chat/multi-agent")
async def multi_agent_chat(
    phone_number: str,
    message: str,
    session_id: Optional[str] = None
):
    """Process a chat message with multiple agents and return synthesized response."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Use the improved collaboration engine for better responses
        response = await collaboration_engine.process_user_query(
            user_query=message,
            phone_number=phone_number
        )
        
        if response["success"]:
            # Format response for frontend compatibility
            formatted_response = {
                "success": True,
                "session_id": response.get("metadata", {}).get("session_id", session_id),
                "phone_number": phone_number,
                "primary_response": {
                    "message": response["response"],
                    "agent_type": "multi_agent",
                    "confidence": response.get("metadata", {}).get("confidence_score", 0.8),
                    "recommendations": response.get("recommendations", []),
                    "insights": response.get("agent_insights", []),
                    "next_actions": [],
                    "timestamp": response.get("metadata", {}).get("processing_timestamp", datetime.utcnow().isoformat())
                },
                "metadata": response.get("metadata", {}),
                "validation": response.get("validation", {}),
                "statistics": response.get("statistics", {}),
                "risks_and_opportunities": response.get("risks_and_opportunities", {})
            }
            return formatted_response
        else:
            raise HTTPException(status_code=500, detail=response.get("error", "Unknown error"))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing multi-agent chat: {str(e)}")


@app.post("/api/v1/chat/collaborative")
async def collaborative_chat(
    phone_number: str,
    message: str,
    session_id: Optional[str] = None
):
    """Process a chat message using the new collaborative multi-agent system."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Check if it's a simple greeting
        simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if message.lower().strip() in simple_greetings:
            # Provide a simple, friendly response for greetings
            return {
                "success": True,
                "session_id": session_id,
                "phone_number": phone_number,
                "final_recommendation": "Hi there! I'm your financial assistant. How can I help you today? You can ask me about your investments, savings, budgeting, or any financial questions you have.",
                "metadata": {
                    "processing_type": "simple_greeting",
                    "confidence_score": 1.0,
                    "processing_timestamp": datetime.utcnow().isoformat()
                },
                "validation": {
                    "status": "APPROVED",
                    "confidence_score": 100,
                    "critical_errors": 0,
                    "moderate_concerns": 0,
                    "minor_suggestions": 0,
                    "hallucination_flags": 0,
                    "overall_assessment": "Simple greeting handled appropriately"
                },
                "statistics": {},
                "agent_insights": [],
                "recommendations": [],
                "risks_and_opportunities": {"risks": [], "opportunities": []}
            }
        
        # Use the improved collaboration engine for financial queries
        response = await collaboration_engine.process_user_query(
            user_query=message,
            phone_number=phone_number
        )
        
        if response["success"]:
            # Format response for frontend compatibility
            formatted_response = {
                "success": True,
                "session_id": response.get("metadata", {}).get("session_id", session_id),
                "phone_number": phone_number,
                "final_recommendation": response["response"],
                "metadata": response.get("metadata", {}),
                "validation": response.get("validation", {}),
                "statistics": response.get("statistics", {}),
                "agent_insights": response.get("agent_insights", []),
                "recommendations": response.get("recommendations", []),
                "risks_and_opportunities": response.get("risks_and_opportunities", {})
            }
            return formatted_response
        else:
            raise HTTPException(status_code=500, detail=response.get("error", "Unknown error"))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing collaborative chat: {str(e)}")


@app.post("/api/v1/sessions")
async def create_session(
    phone_number: str,
    title: Optional[str] = None
):
    """Create a new chat session for a user."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        response = await chat_service.create_new_session(
            phone_number=phone_number,
            title=title
        )
        
        if response["success"]:
            return response
        else:
            raise HTTPException(status_code=500, detail=response["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")


@app.get("/api/v1/sessions/{phone_number}")
async def get_user_sessions(
    phone_number: str,
    active_only: bool = True
):
    """Get all chat sessions for a user."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        response = await chat_service.get_user_sessions(
            phone_number=phone_number,
            active_only=active_only
        )
        
        if response["success"]:
            return response
        else:
            raise HTTPException(status_code=500, detail=response["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sessions: {str(e)}")


@app.get("/api/v1/sessions/{phone_number}/{session_id}")
async def get_session_details(
    phone_number: str,
    session_id: str
):
    """Get detailed information about a specific chat session."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        
        response = await chat_service.get_session_details(
            phone_number=phone_number,
            session_id=session_id
        )
        
        if response["success"]:
            return response
        else:
            raise HTTPException(status_code=500, detail=response["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session details: {str(e)}")


@app.delete("/api/v1/sessions/{phone_number}/{session_id}")
async def deactivate_session(
    phone_number: str,
    session_id: str
):
    """Deactivate a chat session."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        
        response = await chat_service.deactivate_session(
            phone_number=phone_number,
            session_id=session_id
        )
        
        if response["success"]:
            return response
        else:
            raise HTTPException(status_code=500, detail=response["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating session: {str(e)}")


@app.get("/api/v1/users/{phone_number}/stats")
async def get_user_stats(phone_number: str):
    """Get user statistics."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        response = await chat_service.get_user_stats(phone_number=phone_number)
        
        if response["success"]:
            return response
        else:
            raise HTTPException(status_code=500, detail=response["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user stats: {str(e)}")


@app.websocket("/ws/chat/{phone_number}")
async def websocket_chat(websocket: WebSocket, phone_number: str):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")
            session_id = data.get("session_id", None)
            
            if not message:
                await websocket.send_json({
                    "error": "Message is required",
                    "timestamp": datetime.utcnow().isoformat()
                })
                continue
            
            # Process the message
            response = await chat_service.process_chat_message(
                phone_number=phone_number,
                message=message,
                session_id=session_id
            )
            
            # Send response back to client
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for phone number {phone_number}")
    except Exception as e:
        print(f"Error in WebSocket chat: {e}")
        await websocket.send_json({
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })


@app.get("/api/v1/financial-data")
async def get_financial_data():
    """Get comprehensive financial data for the configured phone number."""
    try:
        financial_data = await mcp_service.get_comprehensive_financial_data()
        return {
            "financial_data": financial_data,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching financial data: {str(e)}")


# Legacy endpoints for backward compatibility
@app.post("/chat")
async def legacy_chat_endpoint(
    user_id: str,
    message: str,
    session_id: Optional[str] = None
):
    """Legacy chat endpoint - redirects to phone number-based endpoint."""
    return await chat_endpoint(
        phone_number=user_id,  # Treat user_id as phone_number for backward compatibility
        message=message,
        session_id=session_id
    )


@app.post("/chat/multi-agent")
async def legacy_multi_agent_chat(
    user_id: str,
    message: str,
    session_id: Optional[str] = None
):
    """Legacy multi-agent chat endpoint - redirects to phone number-based endpoint."""
    return await multi_agent_chat(
        phone_number=user_id,  # Treat user_id as phone_number for backward compatibility
        message=message,
        session_id=session_id
    )


@app.get("/sessions/{user_id}")
async def legacy_get_user_sessions(user_id: str):
    """Legacy sessions endpoint - redirects to phone number-based endpoint."""
    return await get_user_sessions(phone_number=user_id)


@app.get("/sessions/{user_id}/{session_id}")
async def legacy_get_session_details(user_id: str, session_id: str):
    """Legacy session details endpoint - redirects to phone number-based endpoint."""
    return await get_session_details(phone_number=user_id, session_id=session_id)


@app.post("/api/v1/chat/adk")
async def adk_chat(
    phone_number: str,
    message: str,
    session_id: Optional[str] = None
):
    """Process a chat message using the ADK agent system with full visibility."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Check if it's a simple greeting
        simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if message.lower().strip() in simple_greetings:
            return {
                "success": True,
                "session_id": session_id,
                "phone_number": phone_number,
                "response": {
                    "message": "Hi there! I'm your financial assistant. How can I help you today? You can ask me about your investments, savings, budgeting, or any financial questions you have.",
                    "agent_type": "assistant",
                    "confidence": 1.0,
                    "recommendations": [],
                    "insights": [],
                    "next_actions": [],
                    "timestamp": datetime.utcnow().isoformat()
                },
                "metadata": {
                    "processing_type": "simple_greeting",
                    "confidence_score": 1.0,
                    "processing_timestamp": datetime.utcnow().isoformat()
                }
            }
        
        # Fetch financial data
        financial_data = await mcp_service.get_comprehensive_financial_data(phone_number)
        
        # Process with ADK system
        session = await adk_system.process_query(
            user_query=message,
            financial_data=financial_data,
            phone_number=phone_number
        )
        
        # Get session summary
        session_summary = adk_system.get_session_summary(session)
        
        return {
            "success": True,
            "session_id": session.session_id,
            "phone_number": phone_number,
            "response": {
                "message": session.final_response,
                "agent_type": "adk_coordinator",
                "confidence": 0.8,
                "recommendations": [],
                "insights": [],
                "next_actions": [],
                "timestamp": session.timestamp.isoformat()
            },
            "metadata": {
                "processing_type": "adk_multi_agent",
                "confidence_score": 0.8,
                "processing_timestamp": session.timestamp.isoformat(),
                "total_agents": len(session.agent_responses),
                "collaboration_steps": len(session.collaboration_log)
            },
            "adk_session": session_summary,
            "agent_interactions": [
                {
                    "agent_id": resp.agent_id,
                    "agent_name": resp.agent_name,
                    "input_query": resp.input_query,
                    "response": resp.response,
                    "confidence": resp.confidence,
                    "reasoning": resp.reasoning,
                    "timestamp": resp.timestamp.isoformat()
                }
                for resp in session.agent_responses
            ],
            "collaboration_log": session.collaboration_log
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing ADK chat: {str(e)}")


@app.post("/api/v1/chat/simple")
async def simple_chat(
    phone_number: str,
    message: str,
    session_id: Optional[str] = None
):
    """Process a chat message and return only the response message with Firestore storage."""
    try:
        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Initialize Firestore service
        firestore_service = FirestoreService()
        
        # Create or get user
        user = firestore_service.create_or_get_user(phone_number)
        
        # Create session if not provided
        if not session_id:
            chat_session = firestore_service.create_session(phone_number)
            session_id = chat_session.session_id
        else:
            # Get existing session
            chat_session = firestore_service.get_session(session_id)
            if not chat_session:
                chat_session = firestore_service.create_session(phone_number)
                session_id = chat_session.session_id
        
        # Save user message to Firestore
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            phone_number=phone_number,
            role=MessageRole.USER,
            content=message,
            message_type=MessageType.TEXT,
            timestamp=datetime.utcnow(),
            metadata=None
        )
        firestore_service.save_message(user_message)
        
        # Get conversation history for context
        conversation_history = firestore_service.get_conversation_history(session_id, limit=5)
        
        # Check if it's a simple greeting
        simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if message.lower().strip() in simple_greetings:
            ai_response = "Hi there! I'm your financial assistant. How can I help you today? You can ask me about your investments, savings, budgeting, or any financial questions you have."
        else:
            # Fetch financial data
            financial_data = await mcp_service.get_comprehensive_financial_data(phone_number)
            
            # Enhance query with conversation history
            enhanced_query = message
            if conversation_history:
                context = "Previous conversation:\n"
                for msg in conversation_history:
                    context += f"{msg['role']}: {msg['content']}\n"
                enhanced_query = f"{context}\n\nCurrent question: {message}"
            
            # Process with ADK system
            session = await adk_system.process_query(
                user_query=enhanced_query,
                financial_data=financial_data,
                phone_number=phone_number
            )
            
            ai_response = session.final_response
        
        # Save AI response to Firestore
        ai_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            phone_number=phone_number,
            role=MessageRole.ASSISTANT,
            content=ai_response,
            message_type=MessageType.TEXT,
            timestamp=datetime.utcnow(),
            metadata={
                "agent_type": "financial_assistant",
                "confidence": 0.8
            }
        )
        firestore_service.save_message(ai_message)
        
        # Update session
        firestore_service.update_session(session_id, {
            "updated_at": datetime.utcnow(),
            "message_count": firestore.Increment(2)  # User + AI message
        })
        
        return {
            "message": ai_response,
            "session_id": session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.get("/api/v1/adk/agents")
async def get_adk_agents():
    """Get information about ADK agents."""
    try:
        agents_info = []
        for agent_id, agent_config in adk_system.agents.items():
            agents_info.append({
                "agent_id": agent_id,
                "name": agent_config["name"],
                "description": agent_config["description"],
                "capabilities": agent_config["capabilities"]
            })
        
        return {
            "success": True,
            "agents": agents_info,
            "total_agents": len(agents_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ADK agents: {str(e)}")


@app.get("/api/v1/adk/session/{session_id}")
async def get_adk_session(session_id: str):
    """Get detailed information about an ADK session."""
    try:
        # This would typically fetch from a database
        # For now, return a placeholder
        return {
            "success": True,
            "session_id": session_id,
            "message": "Session details would be retrieved from database"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ADK session: {str(e)}")


@app.get("/api/v1/chat/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a specific session."""
    try:
        firestore_service = FirestoreService()
        messages = firestore_service.get_session_messages(session_id, limit=limit)
        
        return {
            "session_id": session_id,
            "messages": [
                {
                    "message_id": msg.id,
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata
                }
                for msg in messages
            ],
            "total_messages": len(messages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chat history: {str(e)}")


@app.get("/api/v1/chat/sessions/{phone_number}")
async def get_user_chat_sessions(phone_number: str, active_only: bool = True):
    """Get all chat sessions for a user."""
    try:
        firestore_service = FirestoreService()
        sessions = firestore_service.get_user_sessions(phone_number, active_only=active_only)
        
        return {
            "phone_number": phone_number,
            "sessions": [
                {
                    "session_id": session.session_id,
                    "title": session.title,
                    "created_at": session.created_at.isoformat(),
                    "updated_at": session.updated_at.isoformat(),
                    "is_active": session.is_active,
                    "message_count": getattr(session, 'message_count', 0)
                }
                for session in sessions
            ],
            "total_sessions": len(sessions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user sessions: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 