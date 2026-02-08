#!/bin/bash

# FiMoney AI Agent Deployment Script
# This script deploys the phone number-based chat system with Firestore integration

set -e

echo "🚀 Starting FiMoney AI Agent deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
SERVICE_NAME="fi-money-ai-backend"
VERSION="2.0.0"

# Function to print colored output
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
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK is not installed. Please install it first."
        exit 1
    fi
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "You are not authenticated with Google Cloud. Please run 'gcloud auth login' first."
        exit 1
    fi
    
    # Check if project is set
    if [ "$PROJECT_ID" = "your-project-id" ]; then
        print_error "Please set GOOGLE_CLOUD_PROJECT environment variable or update the script."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Setup Google Cloud project
setup_project() {
    print_status "Setting up Google Cloud project..."
    
    # Set the project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    print_status "Enabling required APIs..."
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable firestore.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable cloudfunctions.googleapis.com
    
    print_success "Project setup completed"
}

# Setup Firestore
setup_firestore() {
    print_status "Setting up Firestore database..."
    
    # Check if Firestore database exists
    if ! gcloud firestore databases list --project=$PROJECT_ID --format="value(name)" | grep -q "default"; then
        print_status "Creating Firestore database..."
        gcloud firestore databases create --project=$PROJECT_ID --region=$REGION
    else
        print_status "Firestore database already exists"
    fi
    
    print_success "Firestore setup completed"
}

# Build and deploy the application
deploy_application() {
    print_status "Building and deploying application..."
    
    # Navigate to backend directory
    cd backend
    
    # Create Dockerfile if it doesn't exist
    if [ ! -f "Dockerfile" ]; then
        print_status "Creating Dockerfile..."
        cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
    fi
    
    # Deploy to Cloud Run
    print_status "Deploying to Cloud Run..."
    
    # Source environment variables from .env file
    if [ -f ".env" ]; then
        print_status "Loading environment variables from .env file..."
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    # Set default values if not provided
    GOOGLE_API_KEY=${GOOGLE_API_KEY:-"your-api-key"}
    MCP_FUNCTION_URL=${MCP_FUNCTION_URL:-"https://us-central1-hackathon-62355.cloudfunctions.net"}
    
    gcloud run deploy $SERVICE_NAME \
        --source . \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars="GOOGLE_API_KEY=$GOOGLE_API_KEY,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION,MCP_FUNCTION_URL=$MCP_FUNCTION_URL,PHONE_NUMBER=9999999999" \
        --memory 2Gi \
        --cpu 2 \
        --timeout 300 \
        --concurrency 80 \
        --max-instances 10
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    print_success "Application deployed successfully!"
    print_status "Service URL: $SERVICE_URL"
    
    cd ..
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    # Check if .env file exists in backend directory
    if [ -f "backend/.env" ]; then
        print_status "Found backend/.env file"
        # Copy to current directory for deployment
        cp backend/.env .env
    elif [ -f ".env" ]; then
        print_status "Found .env file in current directory"
    else
        print_warning "No .env file found. Please create one with the following variables:"
        echo "  - GOOGLE_API_KEY"
        echo "  - GOOGLE_CLOUD_PROJECT"
        echo "  - MCP_FUNCTION_URL"
        echo "  - Other required environment variables"
    fi
    
    print_success "Environment setup completed"
}

# Test the deployment
test_deployment() {
    print_status "Testing deployment..."
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    # Test health endpoint
    print_status "Testing health endpoint..."
    if curl -s "$SERVICE_URL/health" | grep -q "healthy"; then
        print_success "Health check passed"
    else
        print_error "Health check failed"
        exit 1
    fi
    
    # Test root endpoint
    print_status "Testing root endpoint..."
    if curl -s "$SERVICE_URL/" | grep -q "FiMoney AI Agent API"; then
        print_success "Root endpoint test passed"
    else
        print_error "Root endpoint test failed"
        exit 1
    fi
    
    print_success "Deployment test completed"
}

# Display deployment information
display_info() {
    print_status "Deployment completed successfully!"
    echo ""
    echo "📋 Deployment Information:"
    echo "  Project ID: $PROJECT_ID"
    echo "  Region: $REGION"
    echo "  Service Name: $SERVICE_NAME"
    echo "  Version: $VERSION"
    echo ""
    
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    echo "🌐 Service URL: $SERVICE_URL"
    echo ""
    
    echo "📚 API Documentation:"
    echo "  - Health Check: $SERVICE_URL/health"
    echo "  - API Docs: $SERVICE_URL/docs"
    echo "  - OpenAPI Spec: $SERVICE_URL/openapi.json"
    echo ""
    
    echo "🔧 Next Steps:"
    echo "  1. Update backend/.env with your configuration"
    echo "  2. Test the API endpoints"
    echo "  3. Integrate with your frontend application"
    echo "  4. Set up monitoring and logging"
    echo ""
    
    echo "📖 Documentation:"
    echo "  - API Documentation: API_DOCUMENTATION.md"
    echo "  - Integration Guide: INTEGRATION_GUIDE.md"
    echo "  - README: README.md"
    echo ""
}

# Main deployment process
main() {
    echo "🎯 FiMoney AI Agent Deployment"
    echo "================================"
    echo ""
    
    check_prerequisites
    setup_project
    setup_firestore
    setup_environment
    deploy_application
    test_deployment
    display_info
    
    print_success "Deployment completed successfully! 🎉"
}

# Run main function
main "$@" 