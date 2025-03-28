# fast-api

docker run -d --name mongodb -p 27017:27017 mongo
#local
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx

echo "127.0.0.1 fastapi.local" | sudo tee -a /etc/hosts

minikube tunnel
