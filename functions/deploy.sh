#!/bin/bash

# Google Cloud Functions Deployment Script
# This script deploys all the MCP integration functions to Google Cloud

set -e

# Configuration
PROJECT_ID="hackathon-62355"  # Replace with your actual project ID
REGION="us-central1"
RUNTIME="nodejs18"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Deploying Fi MCP Google Cloud Functions...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Not authenticated with gcloud. Please run 'gcloud auth login' first.${NC}"
    exit 1
fi

# Set the project
echo -e "${YELLOW}📋 Setting project to ${PROJECT_ID}...${NC}"
gcloud config set project $PROJECT_ID

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install

# Deploy functions
echo -e "${YELLOW}🔧 Deploying functions...${NC}"

# Deploy each function
functions=(
    "getNetWorth"
    "getCreditReport"
    "getEPFDetails"
    "getMFTransactions"
    "getFinancialDashboard"
    "getPortfolioAnalytics"
    "healthCheck"
)

for func in "${functions[@]}"; do
    echo -e "${YELLOW}📤 Deploying ${func}...${NC}"
    
    gcloud functions deploy $func \
        --gen2 \
        --runtime=$RUNTIME \
        --region=$REGION \
        --source=. \
        --entry-point=$func \
        --trigger-http \
        --allow-unauthenticated \
        --memory=256MB \
        --timeout=60s \
        --set-env-vars="MCP_BASE_URL=https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully deployed ${func}${NC}"
    else
        echo -e "${RED}❌ Failed to deploy ${func}${NC}"
        exit 1
    fi
done

echo -e "${GREEN}🎉 All functions deployed successfully!${NC}"

# Get function URLs
echo -e "${YELLOW}🔗 Function URLs:${NC}"
for func in "${functions[@]}"; do
    URL=$(gcloud functions describe $func --region=$REGION --gen2 --format="value(serviceConfig.uri)")
    echo -e "${GREEN}${func}: ${URL}${NC}"
done

echo -e "${YELLOW}📝 Note: MCP server is deployed at https://fi-mcp-server-267132178774.us-central1.run.app/mcp/stream${NC}"
echo -e "${YELLOW}📝 The MCP_BASE_URL environment variable is set to the deployed server${NC}" 