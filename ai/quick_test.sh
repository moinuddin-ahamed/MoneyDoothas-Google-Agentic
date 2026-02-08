#!/bin/bash

# Quick Test Script for Multi-Agent Financial Analysis System
BASE_URL="http://localhost:8000"

echo "🚀 Quick Test for Multi-Agent System"
echo "===================================="

# Test 1: System Health
echo "🏥 Testing System Health..."
health_response=$(curl -s "$BASE_URL/health")
if echo "$health_response" | grep -q '"status":"healthy"'; then
    echo "✅ System Health: PASS"
else
    echo "❌ System Health: FAIL"
    echo "Response: $health_response"
fi

# Test 2: Collaborative Agents
echo "🤖 Testing Collaborative Agents..."
agents_response=$(curl -s "$BASE_URL/api/v1/collaborative/agents")
if echo "$agents_response" | grep -q '"total_agents"'; then
    echo "✅ Collaborative Agents: PASS"
else
    echo "❌ Collaborative Agents: FAIL"
    echo "Response: $agents_response"
fi

# Test 3: No Assets User
echo "📊 Testing No Assets User (1111111111)..."
response1=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative" \
    -H "Content-Type: application/json" \
    -d '{"phone_number": "1111111111", "message": "What is my current financial situation?"}')

if echo "$response1" | grep -q '"success": true'; then
    echo "✅ No Assets User: PASS"
    session_id=$(echo "$response1" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ No Assets User: FAIL"
    echo "Response: $response1"
fi

# Test 4: Full Portfolio User
echo "📊 Testing Full Portfolio User (2222222222)..."
response2=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative" \
    -H "Content-Type: application/json" \
    -d '{"phone_number": "2222222222", "message": "Can I buy a house based on my finances?"}')

if echo "$response2" | grep -q '"success": true'; then
    echo "✅ Full Portfolio User: PASS"
    session_id=$(echo "$response2" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ Full Portfolio User: FAIL"
    echo "Response: $response2"
fi

# Test 5: Debt-Heavy User
echo "📊 Testing Debt-Heavy User (7777777777)..."
response3=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative" \
    -H "Content-Type: application/json" \
    -d '{"phone_number": "7777777777", "message": "How can I reduce my debt burden?"}')

if echo "$response3" | grep -q '"success": true'; then
    echo "✅ Debt-Heavy User: PASS"
    session_id=$(echo "$response3" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ Debt-Heavy User: FAIL"
    echo "Response: $response3"
fi

echo "===================================="
echo "🎯 Quick Test Complete!" 