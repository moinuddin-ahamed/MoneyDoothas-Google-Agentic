#!/bin/bash

# Set your Google Cloud project ID
PROJECT_ID="hackathon-62355"

# Set the region
REGION="us-central1"

# Set the service name
SERVICE_NAME="financial-app"

echo "🚀 Deploying Financial App to Google Cloud Run..."

# Build and deploy using gcloud
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --project $PROJECT_ID

echo "✅ Deployment completed!"
echo "🌐 Your app is now live at: https://financial-app-[hash]-uc.a.run.app" 