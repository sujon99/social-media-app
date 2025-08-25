#!/bin/bash

# Social Media App Kubernetes Deployment Script
# This script deploys the entire social media application to Kubernetes

set -e

echo "🚀 Starting Social Media App Kubernetes Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if kubectl is connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    print_error "kubectl is not connected to a cluster. Please check your kubeconfig."
    exit 1
fi

print_status "Connected to Kubernetes cluster: $(kubectl cluster-info | head -n1)"

# Create namespaces
print_status "Creating namespaces..."
kubectl apply -f namespace.yaml

# Create storage classes and persistent volumes
print_status "Setting up storage..."
kubectl apply -f persistent-volume.yaml

# Create secrets and configmaps
print_status "Creating secrets and configmaps..."
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml

# Deploy database
print_status "Deploying MySQL database..."
kubectl apply -f mysql-deployment.yaml

# Deploy Redis
print_status "Deploying Redis cache..."
kubectl apply -f redis-deployment.yaml

# Deploy MinIO
print_status "Deploying MinIO storage..."
kubectl apply -f minio-deployment.yaml

# Wait for services to be ready
print_status "Waiting for infrastructure services to be ready..."
kubectl wait --for=condition=ready pod -l app=mysql -n social-media --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n social-media --timeout=300s
kubectl wait --for=condition=ready pod -l app=minio -n social-media --timeout=300s

# Deploy Django application
print_status "Deploying Django application..."
kubectl apply -f app-deployment.yaml

# Deploy Nginx
print_status "Deploying Nginx reverse proxy..."
kubectl apply -f nginx-deployment.yaml

# Wait for application pods to be ready
print_status "Waiting for application pods to be ready..."
kubectl wait --for=condition=ready pod -l app=social-media-app -n social-media --timeout=300s
kubectl wait --for=condition=ready pod -l app=nginx -n social-media --timeout=300s

# Deploy network policies
print_status "Applying network policies..."
kubectl apply -f network-policy.yaml

# Deploy HPA
print_status "Setting up autoscaling..."
kubectl apply -f hpa.yaml

# Deploy ingress
print_status "Setting up ingress..."
kubectl apply -f ingress.yaml

# Show deployment status
print_status "Deployment completed! Checking status..."
echo ""
kubectl get pods -n social-media
echo ""
kubectl get services -n social-media
echo ""
kubectl get ingress -n social-media

print_status "🎉 Social Media App has been deployed successfully!"
print_status "You can access the application through the ingress or NodePort services."
print_status "Check the status with: kubectl get all -n social-media"
