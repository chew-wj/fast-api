# fast-api

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

To deploy the application to EKS manually using existing manifests:

1. Configure AWS CLI and kubectl:
```sh
# Configure AWS CLI with your credentials
aws configure

# Update kubeconfig for your EKS cluster
aws eks update-kubeconfig --region ap-southeast-1 --name my-eks-cluster
```

2. Create the namespace and verify:
```sh
kubectl create namespace fastapi-app
kubectl get namespace
```

3. Create MongoDB secrets:
```sh
# Replace with your actual MongoDB credentials
export MONGO_USERNAME=your_username
export MONGO_PASSWORD=your_password
export MONGO_CONNECTION_STRING=mongodb://mongouser:mongopassword@mongodb-service:27017

kubectl create secret generic mongodb-secrets \
  --from-literal=username=$MONGO_USERNAME \
  --from-literal=password=$MONGO_PASSWORD \
  --from-literal=mongodb-connection-string=$MONGO_CONNECTION_STRING \
  -n fastapi-app
```

4. Deploy MongoDB:
```sh
kubectl apply -f kubernetes/mongodb.yaml -n fastapi-app
```

5. Build and push Docker image to ECR:
```sh
# Login to ECR
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin $(aws ecr describe-repositories --query "repositories[?repositoryName=='fastapi-app'].repositoryUri" --output text)

# Build and tag image
docker build -t fast-api:latest .
docker tag fast-api:latest $(aws ecr describe-repositories --query "repositories[?repositoryName=='fastapi-app'].repositoryUri" --output text):latest

# Push to ECR
docker push $(aws ecr describe-repositories --query "repositories[?repositoryName=='fastapi-app'].repositoryUri" --output text):latest
```

6. Deploy the FastAPI application:
```sh
kubectl apply -f kubernetes/fast-api.yaml -n fastapi-app
```

7. Verify the deployment:
```sh
# Check pods
kubectl get pods -n fastapi-app

# Check services
kubectl get svc -n fastapi-app

# Check ingress
kubectl get ingress -n fastapi-app
```

8. Access the application:
```sh
# Get the external IP/hostname of your ingress controller
kubectl get svc -n ingress-nginx

# Access the application using the external IP/hostname
curl http://<external-ip>
```

Troubleshooting:
- Check pod logs: `kubectl logs -f deployment/fastapi-app -n fastapi-app`
- Check pod status: `kubectl describe pod <pod-name> -n fastapi-app`
- Verify secrets: `kubectl get secrets mongodb-secrets -n fastapi-app -o yaml`
- Check ingress configuration: `kubectl describe ingress fastapi-ingress -n fastapi-app`

To clean up:
```sh
# Delete the application
kubectl delete -f kubernetes/fast-api.yaml -n fastapi-app

# Delete MongoDB
kubectl delete -f kubernetes/mongodb.yaml -n fastapi-app

# Delete secrets
kubectl delete secret mongodb-secrets -n fastapi-app

# Delete namespace
kubectl delete namespace fastapi-app
```

## API Documentation

Swagger UI: http://localhost:8000/docs <br>
ReDoc: http://localhost:8000/redoc


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


### 5. CI/CD Security
- **Pipeline Security**:
  - Secure handling of secrets in GitHub Actions
  - Signed commits and tags
  - Automated security testing
- **Deployment Security**:
  - Immutable infrastructure
  - Blue-green deployments
  - Automated rollback capabilities

### 6. Documentation & Training
- **Security Documentation**:
  - Security policy documentation
  - Incident response procedures
  - Compliance requirements
- **Team Training**:
  - Regular security awareness training
  - DevSecOps best practices
  - Incident response drills

This DevSecOps implementation ensures continuous security and compliance throughout the development lifecycle, from code creation to deployment and operation.
