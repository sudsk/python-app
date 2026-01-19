# Python App - Kubernetes Deployment with KIND and CI/CD

This repository contains a simple Python Flask application and all the necessary infrastructure code to deploy it to a Kubernetes cluster (KIND) running on a GCP VM, with a full CI/CD pipeline using GitHub Actions.

## Project Structure

```bash
.
├── .github/workflows/    # GitHub Actions for CI and CD
│   ├── ci.yaml           # CI: Build and Push Docker Image
│   └── cd.yaml           # CD: Deploy to KIND via Helm
├── charts/               # Helm Charts
│   ├── python-app/       # Main application Helm chart
│   └── argocd/           # ArgoCD configuration (values-argo.yaml)
├── k8s/                  # Raw Kubernetes Manifests
│   ├── deployment.yaml   # App Deployment
│   ├── service.yaml      # App Service
│   ├── ingress.yaml      # Ingress (NGINX)
│   ├── pod.yaml          # Single Pod manifest
│   └── github-runner.yaml# Self-hosted GitHub Runner manifest
├── src/                  # Python Application source code
│   └── app.py            # Flask application
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
└── .gitignore            # Git ignore file
```

## Features

- **Flask API**: A simple Python API returning hostname, IP, and a "Hello World" message.
- **Dockerized**: Containerized using a lightweight Alpine base image.
- **Kubernetes Ready**: Manifests for Deployment, Service, and Ingress.
- **Helm Powered**: Packaged as a Helm chart for flexible deployments.
- **NGINX Ingress**: Configured for KIND with host-port mapping for external access.
- **CI/CD Pipeline**:
  - **CI**: Automatically builds and pushes Docker images to Docker Hub on every push to `main`.
  - **CD**: Automatically deploys the latest build to the KIND cluster using a self-hosted runner.
- **GitOps Ready**: ArgoCD configuration included for managed deployments.

## Setup Instructions

### 1. KIND Cluster Setup (GCP VM)

To expose the Ingress on the VM's external IP, KIND is initialized with host-port mapping:

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
```

Create the cluster:
`kind create cluster --config kind-config.yaml`

### 2. Ingress Controller

Install the NGINX Ingress controller for KIND:
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml`

### 3. CI/CD Setup

#### Docker Hub Configuration
Set these in your GitHub Repository Secrets/Variables:
- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: Your Docker Hub access token (Secret).

#### Self-Hosted Runner
Deploy the runner to your KIND cluster:
1. Create a GitHub PAT with `repo` scope.
2. Create the secret:
   `kubectl create secret generic github-token --from-literal=token=YOUR_PAT -n github-runner`
3. Apply the runner:
   `kubectl apply -f k8s/github-runner.yaml`

## Usage

Once deployed, the API is available at:
`http://<VM_EXTERNAL_IP>/api/v1/details`

Endpoints:
- `GET /api/v1/details`: System details and hello message.
- `GET /api/v1/healthz`: Health check endpoint.
