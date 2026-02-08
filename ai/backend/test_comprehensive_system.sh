#!/bin/bash

# Comprehensive Test Script for Multi-Agent Financial Analysis System
BASE_URL="http://localhost:8000"

echo "🚀 Comprehensive Test for Multi-Agent System"
echo "============================================"

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

# Test 3: No Assets User (1111111111)
echo "📊 Testing No Assets User (1111111111)..."
response1=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative?phone_number=1111111111&message=What%20is%20my%20current%20financial%20situation?")

if echo "$response1" | grep -q '"success":true'; then
    echo "✅ No Assets User: PASS"
    session_id=$(echo "$response1" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ No Assets User: FAIL"
    echo "Response: $response1"
fi

# Test 4: Full Portfolio User (2222222222)
echo "📊 Testing Full Portfolio User (2222222222)..."
response2=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative?phone_number=2222222222&message=Can%20I%20buy%20a%20house%20based%20on%20my%20finances?")

if echo "$response2" | grep -q '"success":true'; then
    echo "✅ Full Portfolio User: PASS"
    session_id=$(echo "$response2" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ Full Portfolio User: FAIL"
    echo "Response: $response2"
fi

# Test 5: Debt-Heavy User (7777777777)
echo "📊 Testing Debt-Heavy User (7777777777)..."
response3=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative?phone_number=7777777777&message=How%20can%20I%20reduce%20my%20debt%20burden?")

if echo "$response3" | grep -q '"success":true'; then
    echo "✅ Debt-Heavy User: PASS"
    session_id=$(echo "$response3" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ Debt-Heavy User: FAIL"
    echo "Response: $response3"
fi

# Test 6: SIP Samurai User (8888888888)
echo "📊 Testing SIP Samurai User (8888888888)..."
response4=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative?phone_number=8888888888&message=How%20are%20my%20SIPs%20performing?")

if echo "$response4" | grep -q '"success":true'; then
    echo "✅ SIP Samurai User: PASS"
    session_id=$(echo "$response4" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ SIP Samurai User: FAIL"
    echo "Response: $response4"
fi

# Test 7: Complex Query
echo "📊 Testing Complex Query..."
response5=$(curl -s -X POST "$BASE_URL/api/v1/chat/collaborative?phone_number=2222222222&message=I%20want%20to%20buy%20a%20house%20worth%20%E2%82%B950%20lakhs.%20Can%20I%20afford%20it?%20What%20should%20be%20my%20down%20payment%20strategy?")

if echo "$response5" | grep -q '"success":true'; then
    echo "✅ Complex Query: PASS"
    session_id=$(echo "$response5" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Session ID: $session_id"
else
    echo "❌ Complex Query: FAIL"
    echo "Response: $response5"
fi

echo "============================================"
echo "🎯 Comprehensive Test Complete!"
