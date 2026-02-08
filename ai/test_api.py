#!/usr/bin/env python3
"""
Test script for FiMoney AI Agent API
Tests the phone number-based chat system functionality
"""

import requests
import json
import time
from typing import Dict, Any

class FiMoneyAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_phone_number = "+1234567890"
        self.session_id = None
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint."""
        print("🔍 Testing health check...")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint."""
        print("🔍 Testing root endpoint...")
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint passed: {data['message']}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False
    
    def test_create_session(self) -> bool:
        """Test creating a new session."""
        print("🔍 Testing session creation...")
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/sessions",
                json={
                    "phone_number": self.test_phone_number,
                    "title": "Test Session"
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.session_id = data["session"]["session_id"]
                    print(f"✅ Session created: {self.session_id}")
                    return True
                else:
                    print(f"❌ Session creation failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Session creation failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Session creation error: {e}")
            return False
    
    def test_chat_message(self) -> bool:
        """Test sending a chat message."""
        print("🔍 Testing chat message...")
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat",
                json={
                    "phone_number": self.test_phone_number,
                    "message": "Hello, how are you?",
                    "session_id": self.session_id
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"✅ Chat message sent successfully")
                    print(f"   Response: {data['response']['message'][:100]}...")
                    return True
                else:
                    print(f"❌ Chat message failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Chat message failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Chat message error: {e}")
            return False
    
    def test_multi_agent_chat(self) -> bool:
        """Test multi-agent chat."""
        print("🔍 Testing multi-agent chat...")
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat/multi-agent",
                json={
                    "phone_number": self.test_phone_number,
                    "message": "Analyze my investment portfolio",
                    "session_id": self.session_id
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"✅ Multi-agent chat successful")
                    return True
                else:
                    print(f"❌ Multi-agent chat failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Multi-agent chat failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Multi-agent chat error: {e}")
            return False
    
    def test_get_user_sessions(self) -> bool:
        """Test getting user sessions."""
        print("🔍 Testing get user sessions...")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/sessions/{self.test_phone_number}"
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    sessions_count = data.get("total_sessions", 0)
                    print(f"✅ User sessions retrieved: {sessions_count} sessions")
                    return True
                else:
                    print(f"❌ Get user sessions failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Get user sessions failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Get user sessions error: {e}")
            return False
    
    def test_get_session_details(self) -> bool:
        """Test getting session details."""
        if not self.session_id:
            print("❌ No session ID available for testing")
            return False
        
        print("🔍 Testing get session details...")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/sessions/{self.test_phone_number}/{self.session_id}"
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    messages_count = len(data["session"]["messages"])
                    print(f"✅ Session details retrieved: {messages_count} messages")
                    return True
                else:
                    print(f"❌ Get session details failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Get session details failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Get session details error: {e}")
            return False
    
    def test_get_user_stats(self) -> bool:
        """Test getting user statistics."""
        print("🔍 Testing get user stats...")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/users/{self.test_phone_number}/stats"
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    stats = data.get("stats", {})
                    total_sessions = stats.get("total_sessions", 0)
                    active_sessions = stats.get("active_sessions", 0)
                    print(f"✅ User stats retrieved: {total_sessions} total, {active_sessions} active sessions")
                    return True
                else:
                    print(f"❌ Get user stats failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Get user stats failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Get user stats error: {e}")
            return False
    
    def test_financial_data(self) -> bool:
        """Test getting financial data."""
        print("🔍 Testing financial data endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/v1/financial-data")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Financial data retrieved successfully")
                return True
            else:
                print(f"❌ Financial data failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Financial data error: {e}")
            return False
    
    def test_agents_endpoint(self) -> bool:
        """Test getting available agents."""
        print("🔍 Testing agents endpoint...")
        try:
            response = requests.get(f"{self.base_url}/agents")
            if response.status_code == 200:
                data = response.json()
                agents_count = data.get("total_agents", 0)
                print(f"✅ Agents endpoint: {agents_count} agents available")
                return True
            else:
                print(f"❌ Agents endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Agents endpoint error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results."""
        print("🚀 Starting FiMoney AI Agent API Tests")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Root Endpoint", self.test_root_endpoint),
            ("Create Session", self.test_create_session),
            ("Chat Message", self.test_chat_message),
            ("Multi-Agent Chat", self.test_multi_agent_chat),
            ("Get User Sessions", self.test_get_user_sessions),
            ("Get Session Details", self.test_get_session_details),
            ("Get User Stats", self.test_get_user_stats),
            ("Financial Data", self.test_financial_data),
            ("Agents Endpoint", self.test_agents_endpoint),
        ]
        
        results = {}
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            try:
                result = test_func()
                results[test_name] = result
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                results[test_name] = False
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<25} {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Please check the implementation.")
        
        return results

def main():
    """Main function to run the tests."""
    import sys
    
    # Get base URL from command line argument or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Testing API at: {base_url}")
    
    # Create tester and run tests
    tester = FiMoneyAPITester(base_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 