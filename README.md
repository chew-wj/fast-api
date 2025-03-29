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

3. Build the Docker image:
```sh
docker build -t fast-api:latest .
```

4. Apply Kubernetes manifests:
```sh
kubectl apply -f kubernetes/
```

5. Check deployment status:
```sh
kubectl get pods
kubectl get services
```

6. Set up local DNS resolution:
```sh
# Add this line to /etc/hosts (requires sudo)
echo "$(minikube ip) fastapi.local" | sudo tee -a /etc/hosts
```

7. Start minikube tunnel in a separate terminal:
```sh
minikube tunnel
```

8. Access the application:
```sh
# The application will be available at:
curl http://fastapi.local:8000
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

## Testing

## Security Considerations




