import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import AsyncClient

from models.chat import ChatMessage, ChatSession, UserContext, PhoneNumberUser, MessageRole


class FirestoreService:
    """Service for managing Firestore operations for phone number-based chat system."""
    
    def __init__(self):
        # Initialize Firestore client
        try:
            # Try to use existing app
            self.db = firestore.client()
        except ValueError:
            # Initialize new app if none exists
            cred = credentials.Certificate("service-account-key.json")
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        
        # Collection names
        self.users_collection = "users"
        self.sessions_collection = "sessions"
        self.messages_collection = "messages"
        self.contexts_collection = "contexts"
    
    def create_or_get_user(self, phone_number: str, name: Optional[str] = None) -> PhoneNumberUser:
        """Create a new user or get existing user by phone number."""
        try:
            user_ref = self.db.collection(self.users_collection).document(phone_number)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                # Update last active time
                user_data = user_doc.to_dict()
                user_data['last_active'] = datetime.utcnow()
                user_ref.update(user_data)
                return PhoneNumberUser(**user_data)
            else:
                # Create new user
                new_user = PhoneNumberUser(
                    phone_number=phone_number,
                    name=name,
                    created_at=datetime.utcnow(),
                    last_active=datetime.utcnow()
                )
                user_ref.set(new_user.dict())
                return new_user
                
        except Exception as e:
            print(f"Error creating/getting user: {e}")
            raise
    
    def create_session(self, phone_number: str, title: Optional[str] = None) -> ChatSession:
        """Create a new chat session for a user."""
        try:
            session_id = str(uuid.uuid4())
            session_title = title or f"Chat Session {session_id[:8]}"
            
            new_session = ChatSession(
                session_id=session_id,
                phone_number=phone_number,
                title=session_title,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=True
            )
            
            # Save session to Firestore
            session_ref = self.db.collection(self.sessions_collection).document(session_id)
            session_ref.set(new_session.dict())
            
            # Update user's session count
            user_ref = self.db.collection(self.users_collection).document(phone_number)
            user_ref.update({
                'total_sessions': firestore.Increment(1),
                'active_sessions': firestore.Increment(1),
                'last_active': datetime.utcnow()
            })
            
            return new_session
            
        except Exception as e:
            print(f"Error creating session: {e}")
            raise
    
    def get_user_sessions(self, phone_number: str, active_only: bool = True) -> List[ChatSession]:
        """Get all sessions for a user."""
        try:
            # Get all sessions for the user first
            query = self.db.collection(self.sessions_collection).where('phone_number', '==', phone_number)
            docs = query.stream()
            
            sessions = []
            for doc in docs:
                session_data = doc.to_dict()
                session = ChatSession(**session_data)
                
                # Filter by active status if requested
                if not active_only or session.is_active:
                    sessions.append(session)
            
            # Sort by updated_at descending
            sessions.sort(key=lambda x: x.updated_at, reverse=True)
            
            return sessions
            
        except Exception as e:
            print(f"Error getting user sessions: {e}")
            return []
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a specific session by ID."""
        try:
            session_ref = self.db.collection(self.sessions_collection).document(session_id)
            session_doc = session_ref.get()
            
            if session_doc.exists:
                session_data = session_doc.to_dict()
                return ChatSession(**session_data)
            else:
                return None
                
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def save_message(self, message: ChatMessage) -> bool:
        """Save a chat message to Firestore."""
        try:
            # Save message
            message_ref = self.db.collection(self.messages_collection).document(message.id)
            message_ref.set(message.dict())
            
            # Update session's updated_at timestamp
            session_ref = self.db.collection(self.sessions_collection).document(message.session_id)
            session_ref.update({
                'updated_at': datetime.utcnow()
            })
            
            return True
            
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get messages for a specific session."""
        try:
            # Get all messages and filter by session_id
            query = self.db.collection(self.messages_collection)
            docs = query.stream()
            
            messages = []
            for doc in docs:
                message_data = doc.to_dict()
                if message_data.get('session_id') == session_id:
                    messages.append(ChatMessage(**message_data))
            
            # Sort by timestamp and limit
            messages.sort(key=lambda x: x.timestamp)
            return messages[-limit:] if len(messages) > limit else messages
            
        except Exception as e:
            print(f"Error getting session messages: {e}")
            return []
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update a session with new data."""
        try:
            session_ref = self.db.collection(self.sessions_collection).document(session_id)
            updates['updated_at'] = datetime.utcnow()
            session_ref.update(updates)
            return True
            
        except Exception as e:
            print(f"Error updating session: {e}")
            return False
    
    def deactivate_session(self, session_id: str, phone_number: str) -> bool:
        """Deactivate a session."""
        try:
            # Update session
            session_ref = self.db.collection(self.sessions_collection).document(session_id)
            session_ref.update({
                'is_active': False,
                'updated_at': datetime.utcnow()
            })
            
            # Update user's active session count
            user_ref = self.db.collection(self.users_collection).document(phone_number)
            user_ref.update({
                'active_sessions': firestore.Increment(-1),
                'last_active': datetime.utcnow()
            })
            
            return True
            
        except Exception as e:
            print(f"Error deactivating session: {e}")
            return False
    
    def get_or_create_user_context(self, phone_number: str) -> UserContext:
        """Get or create user context."""
        try:
            context_ref = self.db.collection(self.contexts_collection).document(phone_number)
            context_doc = context_ref.get()
            
            if context_doc.exists:
                context_data = context_doc.to_dict()
                return UserContext(**context_data)
            else:
                # Create new context
                new_context = UserContext(
                    phone_number=phone_number,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                context_ref.set(new_context.dict())
                return new_context
                
        except Exception as e:
            print(f"Error getting/creating user context: {e}")
            raise
    
    def update_user_context(self, phone_number: str, updates: Dict[str, Any]) -> bool:
        """Update user context."""
        try:
            context_ref = self.db.collection(self.contexts_collection).document(phone_number)
            updates['updated_at'] = datetime.utcnow()
            context_ref.update(updates)
            return True
            
        except Exception as e:
            print(f"Error updating user context: {e}")
            return False
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for context."""
        try:
            messages = self.get_session_messages(session_id, limit)
            
            history = []
            for msg in messages:
                history.append({
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                })
            
            return history
            
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def get_user_stats(self, phone_number: str) -> Dict[str, Any]:
        """Get user statistics."""
        try:
            user_ref = self.db.collection(self.users_collection).document(phone_number)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                
                # Get active sessions count
                active_sessions_query = self.db.collection(self.sessions_collection).where(
                    'phone_number', '==', phone_number
                ).where('is_active', '==', True)
                
                active_sessions = len(list(active_sessions_query.stream()))
                
                return {
                    "phone_number": phone_number,
                    "name": user_data.get('name'),
                    "total_sessions": user_data.get('total_sessions', 0),
                    "active_sessions": active_sessions,
                    "created_at": user_data.get('created_at'),
                    "last_active": user_data.get('last_active')
                }
            else:
                return {
                    "phone_number": phone_number,
                    "error": "User not found"
                }
                
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {
                "phone_number": phone_number,
                "error": str(e)
            } 