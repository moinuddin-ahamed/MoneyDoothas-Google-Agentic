#!/bin/bash

# FiMoneyAI Setup Script
# This script sets up the development environment for the FiMoneyAI project

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Python 3 is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    else
        print_error "pip3 is not installed. Please install pip3."
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment 'venv' already exists."
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Removing existing virtual environment..."
            rm -rf venv
        else
            print_status "Using existing virtual environment."
            return
        fi
    fi
    
    python3 -m venv venv
    print_success "Virtual environment created successfully"
}

# Activate virtual environment and install dependencies
install_dependencies() {
    print_status "Activating virtual environment and installing dependencies..."
    
    # Source the virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    print_status "Installing Python dependencies..."
    if [ -f "backend/requirements.txt" ]; then
        pip install -r backend/requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found in backend directory"
        exit 1
    fi
}

# Create .env file if it doesn't exist
setup_env() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f "backend/.env" ]; then
        print_status "Creating .env file template..."
        cat > backend/.env << EOF
# FiMoneyAI Environment Configuration

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Vertex AI Configuration
VERTEX_AI_LOCATION=us-central1
GEMINI_MODEL=gemini-pro
GEMINI_FLASH_MODEL=gemini-1.5-flash

# MCP Function Configuration
MCP_FUNCTION_URL=https://your-region-your-project.cloudfunctions.net/your-function-name

# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security Configuration
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
BACKEND_CORS_ORIGINS=http://localhost:3000,https://fi-money-ai.web.app

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
EOF
        print_success ".env file template created"
        print_warning "Please update backend/.env with your actual configuration values"
    else
        print_status ".env file already exists"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create logs directory if it doesn't exist
    mkdir -p backend/logs
    
    # Create data directory if it doesn't exist
    mkdir -p backend/data
    
    print_success "Directories created successfully"
}

# Display setup completion message
show_completion() {
    echo
    print_success "Setup completed successfully!"
    echo
    echo -e "${GREEN}Next steps:${NC}"
    echo "1. Update backend/.env with your actual configuration values"
    echo "2. Activate the virtual environment: source venv/bin/activate"
    echo "3. Run the application: cd backend && python main.py"
    echo "4. For development, install pre-commit hooks: pre-commit install"
    echo
    echo -e "${YELLOW}Note:${NC} Make sure to set up your Google Cloud credentials and Firebase configuration"
    echo
}

# Main setup function
main() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  FiMoneyAI Setup Script${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
    
    check_python
    check_pip
    create_venv
    install_dependencies
    setup_env
    create_directories
    show_completion
}

# Run main function
main "$@" 