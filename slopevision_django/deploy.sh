#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# Check if --build flag is provided
if [[ "$1" == "--build" ]]; then
  # Build and push Docker image
  echo "Building Docker image..."
  gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/django-api .
else
  echo "Skipping Docker build (use --build to trigger build)."
fi

# Deploy to Google Cloud Run with all environment variables
echo "Deploying to Google Cloud Run..."
gcloud run deploy django-api \
  --image gcr.io/$GOOGLE_PROJECT_ID/django-api \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="$DATABASE_URL",SECRET_KEY="$SECRET_KEY",DEBUG="$DEBUG",FRONTEND_URL="$FRONTEND_URL",GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_APPLICATION_CREDENTIALS" \
  --port 8000 \
  --service-account $SERVICE_ACCOUNT_EMAIL \
  --timeout=900 \