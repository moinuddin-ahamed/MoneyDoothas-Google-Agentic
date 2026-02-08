#!/usr/bin/env python3
"""
Test script for ADK integration
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.adk_agent_service import adk_agent_service
from services.adk_collaboration_engine import adk_collaboration_engine
from models.agent import AgentRequest, AgentType
from models.chat import ChatMessage, MessageRole


async def test_adk_agents():
    """Test the ADK agent service."""
    print("Testing ADK Agent Service...")
    
    # Test data
    test_financial_data = {
        "total_assets": "₹50,00,000",
        "total_debt": "₹0",
        "monthly_income": "₹1,50,000",
        "credit_score": "750"
    }
    
    test_request = AgentRequest(
        message="Can I afford a BMW car?",
        financial_data=test_financial_data,
        conversation_history=[]
    )
    
    # Test each agent type
    agent_types = [
        AgentType.COORDINATOR,
        AgentType.INVESTMENT,
        AgentType.DEBT_CREDIT,
        AgentType.WEALTH_PLANNER,
        AgentType.FINANCIAL_HEALTH
    ]
    
    for agent_type in agent_types:
        try:
            print(f"\n--- Testing {agent_type.value} ---")
            response = await adk_agent_service.process_request(agent_type, test_request)
            print(f"Response: {response.response}")
            print(f"Confidence: {response.confidence}")
            print(f"Metadata: {response.metadata}")
        except Exception as e:
            print(f"Error testing {agent_type.value}: {e}")


async def test_adk_collaboration():
    """Test the ADK collaboration engine."""
    print("\n\nTesting ADK Collaboration Engine...")
    
    # Test data
    test_financial_data = {
        "total_assets": "₹50,00,000",
        "total_debt": "₹0",
        "monthly_income": "₹1,50,000",
        "credit_score": "750"
    }
    
    test_message = "Can I afford a BMW car?"
    test_phone_number = "9999999999"
    
    try:
        response = await adk_collaboration_engine.process_collaborative_request(
            phone_number=test_phone_number,
            message=test_message,
            financial_data=test_financial_data,
            conversation_history=[]
        )
        
        print(f"Collaborative Response: {response}")
        
        if response.get("success"):
            print("✅ Collaboration test passed!")
        else:
            print("❌ Collaboration test failed!")
            
    except Exception as e:
        print(f"Error in collaboration test: {e}")


async def test_agent_status():
    """Test agent status and connectivity."""
    print("\n\nTesting Agent Status...")
    
    try:
        # Test agent service status
        agents_info = adk_agent_service.get_available_agents()
        print(f"Available agents: {len(agents_info)}")
        for agent in agents_info:
            print(f"  - {agent['type']}: {agent['display_name']}")
        
        # Test connectivity
        connectivity = await adk_agent_service.test_agent_connectivity()
        print(f"Connectivity status: {connectivity}")
        
        # Test collaboration engine status
        collaboration_status = await adk_collaboration_engine.get_agent_status()
        print(f"Collaboration status: {collaboration_status}")
        
    except Exception as e:
        print(f"Error testing agent status: {e}")


async def main():
    """Main test function."""
    print("🚀 Starting ADK Integration Tests...")
    
    try:
        await test_agent_status()
        await test_adk_agents()
        await test_adk_collaboration()
        
        print("\n✅ All ADK tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 