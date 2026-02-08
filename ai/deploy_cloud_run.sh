#!/bin/bash

# FiMoney AI Agent - Cloud Run Deployment Script
set -e

echo "🚀 Deploying FiMoney AI Agent to Google Cloud Run..."

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"hackathon-62355"}
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
SERVICE_NAME="fi-money-ai-backend"
VERSION="2.0.0"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK is not installed. Please install it first."
        exit 1
    fi
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "You are not authenticated with Google Cloud. Please run 'gcloud auth login' first."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Setup project
setup_project() {
    print_status "Setting up Google Cloud project..."
    
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    print_status "Enabling required APIs..."
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable firestore.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    
    print_success "Project setup completed"
}

# Deploy to Cloud Run
deploy_application() {
    print_status "Deploying to Cloud Run..."
    
    cd backend
    
    # Deploy using gcloud run deploy
    gcloud run deploy $SERVICE_NAME \
        --source . \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION" \
        --memory 2Gi \
        --cpu 2 \
        --timeout 300 \
        --concurrency 80 \
        --max-instances 10 \
        --port 8000
    
    cd ..
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    print_success "Application deployed successfully!"
    print_status "Service URL: $SERVICE_URL"
}

# Test deployment
test_deployment() {
    print_status "Testing deployment..."
    
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    # Wait a moment for the service to be ready
    sleep 10
    
    # Test health endpoint
    print_status "Testing health endpoint..."
    if curl -s "$SERVICE_URL/health" | grep -q "healthy"; then
        print_success "Health check passed"
    else
        print_error "Health check failed"
        exit 1
    fi
    
    print_success "Deployment test completed"
}

# Display deployment info
display_info() {
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📋 Deployment Information:"
    echo "  Project ID: $PROJECT_ID"
    echo "  Region: $REGION"
    echo "  Service Name: $SERVICE_NAME"
    echo "  Version: $VERSION"
    echo ""
    echo "🌐 Service URL: $SERVICE_URL"
    echo ""
    echo "📚 API Endpoints:"
    echo "  - Health Check: $SERVICE_URL/health"
    echo "  - API Documentation: $SERVICE_URL/docs"
    echo "  - Chat: $SERVICE_URL/api/v1/chat"
    echo "  - Multi-Agent Chat: $SERVICE_URL/api/v1/chat/multi-agent"
    echo "  - Sessions: $SERVICE_URL/api/v1/sessions"
    echo ""
    echo "🔧 Environment Variables:"
    echo "  - GOOGLE_CLOUD_PROJECT: $PROJECT_ID"
    echo "  - GOOGLE_CLOUD_REGION: $REGION"
    echo ""
    echo "📖 Next Steps:"
    echo "  1. Test the API endpoints using the URLs above"
    echo "  2. Integrate with your frontend application"
    echo "  3. Set up monitoring and logging"
    echo ""
}

# Main deployment process
main() {
    echo "🎯 FiMoney AI Agent - Cloud Run Deployment"
    echo "=========================================="
    echo ""
    
    check_prerequisites
    setup_project
    deploy_application
    test_deployment
    display_info
    
    print_success "Deployment completed successfully! 🎉"
}

# Run main function
main "$@" 