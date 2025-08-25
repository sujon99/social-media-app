#!/bin/bash

# Social Media App Kubernetes Cleanup Script
# This script removes all resources created by the deployment

set -e

echo "🧹 Starting Social Media App Kubernetes Cleanup..."

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

# Confirm deletion
echo ""
print_warning "This will delete ALL resources for the social media application!"
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Cleanup cancelled."
    exit 0
fi

# Delete resources in reverse order of creation
print_status "Removing ingress..."
kubectl delete -f ingress.yaml --ignore-not-found=true

print_status "Removing HPA..."
kubectl delete -f hpa.yaml --ignore-not-found=true

print_status "Removing network policies..."
kubectl delete -f network-policy.yaml --ignore-not-found=true

print_status "Removing Nginx deployment..."
kubectl delete -f nginx-deployment.yaml --ignore-not-found=true

print_status "Removing Django application..."
kubectl delete -f app-deployment.yaml --ignore-not-found=true

print_status "Removing MinIO..."
kubectl delete -f minio-deployment.yaml --ignore-not-found=true

print_status "Removing Redis..."
kubectl delete -f redis-deployment.yaml --ignore-not-found=true

print_status "Removing MySQL..."
kubectl delete -f mysql-deployment.yaml --ignore-not-found=true

print_status "Removing secrets and configmaps..."
kubectl delete -f secret.yaml --ignore-not-found=true
kubectl delete -f configmap.yaml --ignore-not-found=true

print_status "Removing persistent volumes..."
kubectl delete -f persistent-volume.yaml --ignore-not-found=true

print_status "Removing namespaces..."
kubectl delete -f namespace.yaml --ignore-not-found=true

# Force delete any remaining resources
print_status "Cleaning up any remaining resources..."
kubectl delete namespace social-media --ignore-not-found=true --force --grace-period=0
kubectl delete namespace ingress-nginx --ignore-not-found=true --force --grace-period=0

print_status "🎉 Cleanup completed successfully!"
print_status "All social media application resources have been removed."
