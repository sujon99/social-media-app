# DevOps - Kubernetes Deployment

This folder contains all the necessary Kubernetes manifests and deployment scripts for the Social Media Application.

## 📁 File Structure

```
devops/
├── k8s/
│   ├── namespace.yaml           # Namespace definitions
│   ├── configmap.yaml           # Application configuration
│   ├── secret.yaml              # Sensitive data (credentials, keys)
│   ├── persistent-volume.yaml   # Storage configuration
│   ├── mysql-deployment.yaml    # MySQL database deployment
│   ├── redis-deployment.yaml    # Redis cache deployment
│   ├── minio-deployment.yaml    # MinIO object storage deployment
│   ├── app-deployment.yaml      # Django application deployment
│   ├── nginx-deployment.yaml    # Nginx reverse proxy deployment
│   ├── ingress.yaml             # Ingress configuration
│   ├── hpa.yaml                 # Horizontal Pod Autoscaler
│   ├── network-policy.yaml      # Network security policies
│   ├── deploy.sh                # Deployment script
│   └── cleanup.sh               # Cleanup script
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Kubernetes Cluster**: A running Kubernetes cluster (local or cloud)
2. **kubectl**: Kubernetes command-line tool
3. **Docker Image**: The `social-media-app:latest` image should be available

### Deployment

1. **Deploy the entire application:**
   ```bash
   cd devops/k8s
   chmod +x deploy.sh
   ./deploy.sh
   ```

2. **Deploy individual components:**
   ```bash
   # Create namespaces
   kubectl apply -f namespace.yaml
   
   # Deploy storage
   kubectl apply -f persistent-volume.yaml
   
   # Deploy configuration
   kubectl apply -f configmap.yaml
   kubectl apply -f secret.yaml
   
   # Deploy infrastructure
   kubectl apply -f mysql-deployment.yaml
   kubectl apply -f redis-deployment.yaml
   kubectl apply -f minio-deployment.yaml
   
   # Deploy application
   kubectl apply -f app-deployment.yaml
   kubectl apply -f nginx-deployment.yaml
   
   # Deploy networking
   kubectl apply -f ingress.yaml
   kubectl apply -f network-policy.yaml
   kubectl apply -f hpa.yaml
   ```

### Cleanup

To remove all resources:
```bash
cd devops/k8s
chmod +x cleanup.sh
./cleanup.sh
```

## 🏗️ Architecture

### Components

- **MySQL**: Primary database for user and post data
- **Redis**: Session management and caching
- **MinIO**: Object storage for images
- **Django App**: Main application backend
- **Nginx**: Reverse proxy and static file serving
- **Ingress**: External access and load balancing

### Networking

- **Namespaces**: `social-media` and `ingress-nginx`
- **Services**: Internal communication between components
- **Network Policies**: Restricted pod-to-pod communication
- **Ingress**: External access with host-based routing

### Storage

- **Persistent Volumes**: HostPath for local storage
- **Storage Classes**: Manual provisioning
- **Volume Claims**: Dynamic storage allocation

## ⚙️ Configuration

### Environment Variables

All configuration is managed through:
- **ConfigMaps**: Non-sensitive configuration
- **Secrets**: Sensitive data (base64 encoded)

### Key Configuration Areas

1. **Database**: MySQL connection settings
2. **Cache**: Redis connection and session settings
3. **Storage**: MinIO bucket and access settings
4. **Application**: Django settings and URLs
5. **Security**: CSRF and session cookie settings

## 📊 Monitoring & Scaling

### Autoscaling

- **HPA**: CPU and memory-based scaling
- **Scaling Range**: 2-10 replicas for app, 2-8 for Nginx
- **Target Utilization**: 70% CPU, 80% memory

### Health Checks

- **Liveness Probes**: Restart unhealthy pods
- **Readiness Probes**: Ensure pods are ready to serve traffic
- **Startup Probes**: Handle slow-starting containers

## 🔒 Security

### Network Policies

- **Pod Isolation**: Restricted communication between components
- **Service Access**: Only necessary ports are exposed
- **Namespace Isolation**: Components are isolated by namespace

### Secrets Management

- **Base64 Encoding**: All secrets are base64 encoded
- **Environment Variables**: Secrets are injected as environment variables
- **No Hardcoded Values**: All sensitive data is externalized

## 🚨 Troubleshooting

### Common Issues

1. **Image Pull Errors**: Ensure `social-media-app:latest` image exists
2. **Storage Issues**: Check persistent volume claims and storage classes
3. **Network Issues**: Verify network policies and service connectivity
4. **Resource Limits**: Monitor CPU and memory usage

### Debugging Commands

```bash
# Check pod status
kubectl get pods -n social-media

# View pod logs
kubectl logs -f <pod-name> -n social-media

# Describe resources
kubectl describe <resource-type> <resource-name> -n social-media

# Access pods
kubectl exec -it <pod-name> -n social-media -- /bin/bash

# Check services
kubectl get svc -n social-media

# Check ingress
kubectl get ingress -n social-media
```

## 🔄 Updates & Maintenance

### Rolling Updates

- **Deployment Strategy**: Rolling update with zero downtime
- **Update Process**: Update image tags and apply manifests
- **Rollback**: Use `kubectl rollout undo`

### Scaling

- **Manual Scaling**: `kubectl scale deployment <name> --replicas=<number>`
- **Auto Scaling**: HPA automatically adjusts based on metrics
- **Vertical Scaling**: Adjust resource requests/limits in manifests

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [MinIO Kubernetes](https://min.io/docs/minio/kubernetes/)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Kubernetes events and logs
3. Verify configuration and connectivity
4. Check resource availability and limits
