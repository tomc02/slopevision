#!/bin/bash

# Load environment variables from .env file
set -o allexport
source ../slopevision_django/.env
set +o allexport

# Check if --build flag is provided
if [[ "$1" == "--build" ]]; then
  # Build and push Docker image
  echo "Building Docker image..."
  gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/data-service .
else
  echo "Skipping Docker build (use --build to trigger build)."
fi

# Deploy to Google Cloud Run with all environment variables
echo "Deploying to Google Cloud Run..."
gcloud run deploy data-service \
  --image gcr.io/$GOOGLE_PROJECT_ID/data-service \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="$DATABASE_URL" \
  --port 8080 \
  --timeout=900 \