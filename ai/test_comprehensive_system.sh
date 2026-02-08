#!/bin/bash

# Comprehensive Test Script for Multi-Agent Financial Analysis System
# Tests all user profiles with different types of financial queries

BASE_URL="http://localhost:8000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print test results
print_result() {
    local test_name="$1"
    local status="$2"
    local response="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $test_name"
        echo -e "${RED}Error:${NC} $response"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to make API call
make_api_call() {
    local phone_number="$1"
    local message="$2"
    local test_name="$3"
    
    echo -e "${BLUE}🧪 Testing:${NC} $test_name"
    echo -e "${CYAN}Phone:${NC} $phone_number"
    echo -e "${CYAN}Query:${NC} $message"
    
    response=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative" \
        -H "Content-Type: application/json" \
        -d "{
            \"phone_number\": \"$phone_number\",
            \"message\": \"$message\"
        }")
    
    # Check if response contains success
    if echo "$response" | grep -q '"success": true'; then
        print_result "$test_name" "PASS" "$response"
        
        # Extract key information
        session_id=$(echo "$response" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
        response_quality=$(echo "$response" | grep -o '"response_quality":"[^"]*"' | cut -d'"' -f4)
        confidence_score=$(echo "$response" | grep -o '"confidence_score":[0-9]*' | cut -d':' -f2)
        
        echo -e "${GREEN}Session ID:${NC} $session_id"
        echo -e "${GREEN}Response Quality:${NC} $response_quality"
        echo -e "${GREEN}Confidence Score:${NC} $confidence_score"
        
        # Check for agent insights
        agent_count=$(echo "$response" | grep -o '"agent_insights"' | wc -l)
        if [ "$agent_count" -gt 0 ]; then
            echo -e "${GREEN}Agent Insights:${NC} Found $agent_count agent(s) participated"
        fi
        
    else
        print_result "$test_name" "FAIL" "$response"
    fi
    
    echo "----------------------------------------"
}

# Function to test system health
test_system_health() {
    echo -e "${PURPLE}🏥 Testing System Health...${NC}"
    
    # Test health endpoint
    health_response=$(curl -s "$BASE_URL/health")
    if echo "$health_response" | grep -q '"status":"healthy"'; then
        echo -e "${GREEN}✅ System Health: PASS${NC}"
    else
        echo -e "${RED}❌ System Health: FAIL${NC}"
    fi
    
    # Test collaborative agents endpoint
    agents_response=$(curl -s "$BASE_URL/api/v1/collaborative/agents")
    if echo "$agents_response" | grep -q '"total_agents"'; then
        echo -e "${GREEN}✅ Collaborative Agents: PASS${NC}"
    else
        echo -e "${RED}❌ Collaborative Agents: FAIL${NC}"
    fi
    
    echo "----------------------------------------"
}

# Main test execution
echo -e "${PURPLE}🚀 Starting Comprehensive Multi-Agent System Tests${NC}"
echo "========================================"

# Test 1: System Health
test_system_health

# Test 2: No Assets User (1111111111)
echo -e "${YELLOW}📊 Testing No Assets User (1111111111)${NC}"
make_api_call "1111111111" "What is my current financial situation?" "No Assets - Basic Financial Assessment"
make_api_call "1111111111" "Should I start investing?" "No Assets - Investment Advice"

# Test 3: Full Portfolio User (2222222222)
echo -e "${YELLOW}📊 Testing Full Portfolio User (2222222222)${NC}"
make_api_call "2222222222" "Can I buy a house based on my finances?" "Full Portfolio - House Purchase Analysis"
make_api_call "2222222222" "How is my investment portfolio performing?" "Full Portfolio - Portfolio Performance"

# Test 4: Debt-Heavy User (7777777777)
echo -e "${YELLOW}📊 Testing Debt-Heavy User (7777777777)${NC}"
make_api_call "7777777777" "How can I reduce my debt burden?" "Debt-Heavy - Debt Reduction"
make_api_call "7777777777" "What's my financial risk level?" "Debt-Heavy - Risk Assessment"

# Test 5: SIP Samurai User (8888888888)
echo -e "${YELLOW}📊 Testing SIP Samurai User (8888888888)${NC}"
make_api_call "8888888888" "How are my SIPs performing?" "SIP Samurai - SIP Performance"
make_api_call "8888888888" "Should I increase my SIP amounts?" "SIP Samurai - SIP Optimization"

# Test 6: Complex Queries
echo -e "${YELLOW}📊 Testing Complex Financial Queries${NC}"
make_api_call "2222222222" "I want to buy a house worth ₹50 lakhs. Can I afford it? What should be my down payment strategy?" "Complex - House Purchase Planning"
make_api_call "8888888888" "I'm planning for early retirement at 45. How should I adjust my SIP strategy?" "Complex - Early Retirement Planning"

# Final Results
echo -e "${PURPLE}🎯 Test Results Summary${NC}"
echo "========================================"
echo -e "${GREEN}Total Tests:${NC} $TOTAL_TESTS"
echo -e "${GREEN}Passed:${NC} $PASSED_TESTS"
echo -e "${RED}Failed:${NC} $FAILED_TESTS"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! System is working perfectly.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please check the system.${NC}"
    exit 1
fi 