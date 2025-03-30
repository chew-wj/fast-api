# fast-api

## Architecture Overview

### High-Level Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Client        │     │   Ingress       │     │   FastAPI       │
│   (Browser/API) │────▶│   Controller    │────▶│   Application   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Prometheus    │     │   Grafana       │     │   MongoDB       │
│   (Metrics)     │◀───▶│   (Dashboard)   │◀───▶│   (Database)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘

Infrastructure Components:
- VPC with public and private subnets
- EKS cluster with managed node groups
- NAT Gateway for private subnet connectivity
- Security groups for cluster and node access
- IAM roles and policies for EKS
```

##Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Installation](#local-installation)  
3. [Running the Application Locally](#running-the-application-locally) 
   - [Kubernetes Deployment](#kubernetes-deployment)  
4. [Deploying to the Cloud](#deploying-to-the-cloud)  
   - [EKS Deployment](#EKS-deployment)  
5. [API Documentation](#api-documentation)  
6. [Testing](#testing)  
7. [Security Considerations](#security-considerations)  


## Prerequisites 

- **Python (>=3.8)** – for running FastAPI  
- **Pip** – Python package manager  
- **Virtualenv or Conda** (optional) – for managing Python environments  
- **Docker** – for containerized deployment  
- **Kubernetes CLI (kubectl)** – if deploying on Kubernetes  
- **Helm (>=3.0)** – for deploying Helm charts  
- **AWS CLI & Terraform** – if deploying on AWS

## Local Installation
Clone the repository:
```sh
git clone git@github.com:chew-wj/fast-api.git
cd crud-interface
```
Create a virtual environment:
```python
python -m venv venv
source venv/bin/activate
```
Install dependencies:
```python
pip install -r requirements.txt
```

## Running the application locally:
Export variables:
```
export MONGODB_URI=mongodb://localhost:27017/local
export MONGODB_USERNAME=username
export MONGODB_PASSWORD=password
```
Run a mongodb:
```docker
docker run -d --name mongodb -p 27017:27017 mongo
```
Run the FastAPI app:
```sh
uvicorn app.main:app --reload
```

Access the API documentations at:

Swagger UI: http://localhost:8000/docs <br>
ReDoc: http://localhost:8000/redoc

### Running on Minikube Locally

1. Start Minikube:
```sh
minikube start
```

2. Enable Minikube's Docker daemon:
```sh
eval $(minikube docker-env)
```

3. Install Nginx Ingress Controller:
```sh
# Add the ingress-nginx Helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --set controller.service.type=NodePort
```

4. Build the Docker image:
```sh
docker build -t fast-api:latest .
```

5. Export local variables and create kubernetes secrets
```sh
export MONGO_USERNAME=mongouser
export MONGO_PASSWORD=mongopassword
kubectl create secret generic mongodb-secrets --from-literal=username=$MONGO_USERNAME --from-literal=password=$MONGO_PASSWORD  --from-literal=mongodb-connection-string=mongodb://mongouser:mongopassword@mongodb-service:27017
```

6. Apply Kubernetes manifests:
```sh
kubectl apply -f kubernetes/
```

7. Check deployment status:
```sh
kubectl get pods
kubectl get services
```

8. Set up local DNS resolution:
```sh
# Add this line to /etc/hosts (requires sudo)
echo "127.0.0.1 fastapi.local" | sudo tee -a /etc/hosts
```

9. Start minikube tunnel in a separate terminal:
```sh
minikube tunnel
```

10. Access the application:
```sh
# The application will be available at:
curl http://fastapi.local
```

To stop the Minikube cluster:
```sh
minikube stop
```

To delete the Minikube cluster:
```sh
minikube delete
```

Note: Keep the `minikube tunnel` command running in a separate terminal while accessing the application. The tunnel provides a route to services deployed with type LoadBalancer.

## Deploying to the Cloud

### EKS Deployment

## API Documentation

### Available Endpoints

1. Authentication:
   - POST `/auth/token` - Get access token
   - GET `/auth/me` - Get current user info

2. User Management:
   - GET `/users` - List all users
   - GET `/users/{user_id}` - Get user details
   - POST `/users` - Create new user
   - PUT `/users/{user_id}` - Update user
   - DELETE `/users/{user_id}` - Delete user

3. Webhook/Callback:
   - POST `/webhook` - Receive webhook events
   - GET `/webhook/status` - Check webhook status

4. Health:
   - GET `/health` - Health check endpoint

### Webhook/Callback Implementation
The application implements a webhook system that allows external services to send events:
- Webhook endpoint accepts POST requests with JSON payload
- Events are validated and processed asynchronously
- Status endpoint provides real-time webhook processing status
- Failed events are retried automatically
- Webhook events are logged for audit purposes

## Monitoring and Observability

### Metrics Collection
- Prometheus collects application metrics
- Key metrics include:
  - Request latency
  - Error rates
  - Active users
  - Database connection status

### Logging
- Application logs are collected and stored
- Log levels: INFO, WARNING, ERROR
- Structured logging format for easy parsing

### Dashboards
- Grafana dashboards for:
  - Application performance
  - Error rates
  - User activity
  - System resources

## Troubleshooting Guide

### Common Issues
1. Database Connection
   - Check MongoDB service status
   - Verify connection string
   - Check network connectivity

2. Authentication Issues
   - Verify JWT token validity
   - Check user permissions
   - Validate credentials

3. Deployment Problems
   - Check pod status
   - Verify service configuration
   - Review ingress rules

### Debug Commands
```bash
# Check pod status
kubectl get pods -n fastapi-namespace

# View application logs
kubectl logs -f deployment/fastapi-app

# Check service status
kubectl get svc -n fastapi-namespace

# Verify ingress configuration
kubectl get ingress -n fastapi-namespace
```

## Testing

Run tests locally:
```sh
cd crud-interface
export MONGODB_URI=mongodb://localhost:27017/local
export MONGODB_USERNAME=username
export MONGODB_PASSWORD=password
PYTHONPATH=app pytest
```

## Security Considerations

1. Authentication & Authorization:
- JWT-based authentication
- Role-based access control
- Secure password hashing

2. Data Security:
- MongoDB connection string stored as Kubernetes secrets
- Environment variables for sensitive data
- No hardcoded credentials in code

3. CI/CD Security:
- Automated secret scanning in CI pipeline
- Secure handling of AWS credentials
- ECR authentication for container registry

4. Kubernetes Security:
- Secrets management for sensitive data
- Network policies for pod communication
- RBAC for service accounts

5. Best Practices:
- Regular dependency updates
- Container image scanning
- Secure headers configuration
- Rate limiting implementation

## DevSecOps Compliance

This project implements comprehensive DevSecOps practices to ensure security and compliance throughout the development lifecycle:

### 1. Code Security
- **Secret Detection**: 
  - Automated scanning using truffleHog in CI pipeline
  - Pre-commit hooks for local secret detection
  - Regular manual audits of codebase
- **Dependency Management**:
  - Automated dependency updates via Dependabot
  - Regular security audits of dependencies
  - Version pinning for reproducible builds

### 2. Container Security
- **Image Scanning**:
  - Trivy vulnerability scanning in CI pipeline
  - Regular base image updates
  - Multi-stage builds to minimize attack surface
- **Runtime Security**:
  - Pod security policies
  - Read-only root filesystem
  - Non-root user execution

### 3. API Security
- **Authentication & Authorization**:
  - JWT-based authentication with short-lived tokens
  - OAuth2 integration for third-party services
  - Role-based access control (RBAC)
- **API Protection**:
  - Rate limiting with Redis
  - Request validation and sanitization
  - CORS policy enforcement

### 4. Infrastructure Security
- **Kubernetes Security**:
  - Network policies for pod isolation
  - Pod security contexts
  - Service account RBAC
- **Cloud Security**:
  - AWS IAM roles with least privilege
  - ECR image scanning
  - VPC security groups

### 5. Monitoring & Compliance
- **Logging & Monitoring**:
  - Centralized logging with ELK stack
  - Prometheus metrics collection
  - Grafana dashboards for visualization
- **Compliance Checks**:
  - Automated compliance scanning
  - Regular security assessments
  - Policy enforcement through OPA

### 6. CI/CD Security
- **Pipeline Security**:
  - Secure handling of secrets in GitHub Actions
  - Signed commits and tags
  - Automated security testing
- **Deployment Security**:
  - Immutable infrastructure
  - Blue-green deployments
  - Automated rollback capabilities

### 7. Documentation & Training
- **Security Documentation**:
  - Security policy documentation
  - Incident response procedures
  - Compliance requirements
- **Team Training**:
  - Regular security awareness training
  - DevSecOps best practices
  - Incident response drills

This DevSecOps implementation ensures continuous security and compliance throughout the development lifecycle, from code creation to deployment and operation.
