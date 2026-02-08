#!/usr/bin/env python3
"""
Test script for ADK Agent System
Demonstrates agent interactions and collaboration patterns
"""

import asyncio
import json
from adk_agent_system import ADKAgentSystem


async def test_adk_system():
    """Test the ADK system with a sample financial query."""
    
    print("🚀 Testing ADK Agent System")
    print("=" * 50)
    
    # Initialize ADK system
    adk_system = ADKAgentSystem()
    
    # Sample financial data
    financial_data = {
        "net_worth": {
            "totalNetWorth": 658305,
            "assets": [
                {"type": "MUTUAL_FUNDS", "value": 84642},
                {"type": "EPF", "value": 211111},
                {"type": "SAVINGS", "value": 195297}
            ],
            "liabilities": [
                {"type": "HOME_LOAN", "value": 17000},
                {"type": "VEHICLE_LOAN", "value": 5000}
            ]
        },
        "bank_transactions": [
            {"amount": 80935, "type": "CREDIT", "narration": "SALARY"},
            {"amount": 65000, "type": "DEBIT", "narration": "EXPENSES"}
        ],
        "investments": {
            "mutual_funds": [
                {"scheme": "ICICI Prudential Nifty 50", "value": 20196, "return": 15.5},
                {"scheme": "Canara Robeco Gilt Fund", "value": 54117, "return": 129.6}
            ],
            "total_invested": 74313,
            "current_value": 84642
        }
    }
    
    # Test query
    user_query = "How can I improve my investment portfolio?"
    
    print(f"📝 User Query: {user_query}")
    print(f"💰 Financial Data: Net worth ₹{financial_data['net_worth']['totalNetWorth']:,}")
    print("\n" + "=" * 50)
    
    # Process query through ADK system
    session = await adk_system.process_query(
        user_query=user_query,
        financial_data=financial_data,
        phone_number="2222222222"
    )
    
    # Display results
    print("\n📊 ADK System Results")
    print("=" * 50)
    
    print(f"\n🎯 Final Response:")
    print(f"{session.final_response}")
    
    print(f"\n🤖 Individual Agent Responses:")
    print("-" * 30)
    
    for i, response in enumerate(session.agent_responses, 1):
        print(f"\n{i}. {response.agent_name}")
        print(f"   Confidence: {response.confidence:.2f}")
        print(f"   Response: {response.response[:200]}...")
        print(f"   Reasoning: {response.reasoning}")
    
    print(f"\n📋 Collaboration Log:")
    print("-" * 30)
    
    for i, log_entry in enumerate(session.collaboration_log, 1):
        print(f"\n{i}. {log_entry['step']}")
        print(f"   Agent: {log_entry.get('agent_name', 'N/A')}")
        print(f"   Timestamp: {log_entry['timestamp']}")
        if 'validation_status' in log_entry:
            print(f"   Validation: {log_entry['validation_status']}")
            print(f"   Critical Errors: {log_entry.get('critical_errors', 0)}")
            print(f"   Moderate Concerns: {log_entry.get('moderate_concerns', 0)}")
    
    # Get session summary
    summary = adk_system.get_session_summary(session)
    
    print(f"\n📈 Session Summary:")
    print("-" * 30)
    print(f"Session ID: {summary['session_id']}")
    print(f"Total Agents: {len(summary['agent_responses'])}")
    print(f"Collaboration Steps: {len(summary['collaboration_log'])}")
    print(f"Timestamp: {summary['timestamp']}")
    
    # Save detailed results to file
    with open("adk_test_results.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: adk_test_results.json")
    print("\n✅ ADK System Test Completed!")


if __name__ == "__main__":
    asyncio.run(test_adk_system()) 