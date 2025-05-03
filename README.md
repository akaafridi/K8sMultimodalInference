# GPU-Enabled Containerized Microservice for Model Inference

A Kubernetes-deployable microservice for running BLIP image captioning model inference with GPU support.

## Overview

This project implements a Flask API server that uses the BLIP (Bootstrapping Language-Image Pre-training) model from Salesforce for image captioning. The service is containerized using Docker and configured for deployment on Kubernetes with GPU support.

## Features

- **GPU-accelerated inference**: Uses NVIDIA CUDA for fast model inference
- **Kubernetes-ready**: Includes deployment manifests, service configuration, and horizontal pod autoscaling
- **Health checks**: Built-in health check endpoint for Kubernetes liveness and readiness probes
- **Containerized**: Packaged in a Docker container based on NVIDIA CUDA image
- **CI/CD pipeline**: GitHub Actions workflow for building and publishing Docker images
- **Observability**: Prometheus metrics for monitoring request count, latency, and resource usage

## API Endpoints

- **GET /**: Homepage with information about the API
- **GET /health**: Health check endpoint
- **GET /metrics**: Prometheus metrics endpoint
- **POST /infer**: Model inference endpoint for image captioning

### Image Captioning Endpoint

The `/infer` endpoint accepts POST requests with JSON payloads containing either an image URL or a base64-encoded image.

**Example Request:**
```json
{
  "image": "https://example.com/image.jpg"
}
```

**Example Response:**
```json
{
  "predictions": "a woman holding a cat in her arms",
  "model_version": "Salesforce/blip-image-captioning-base"
}
```

## Deployment

### Prerequisites

- Kubernetes cluster with NVIDIA GPU support
- kubectl configured for your cluster
- Docker registry credentials

### Deploying to Kubernetes

1. Apply the Kubernetes manifests:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

2. Check the deployment status:

```bash
kubectl get pods -l app=model-inference-service
kubectl get svc model-inference-service
```

## Local Development

### Requirements

- Python 3.8+
- NVIDIA GPU with CUDA support (for full model)

### Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the Flask application:

```bash
python main.py
```

The API server will be available at http://localhost:5000.

## Docker Build

```bash
docker build -t model-inference-service:latest .
docker run -p 5000:5000 --gpus all model-inference-service:latest
```

## Architecture

The application is designed as a microservice architecture:

- **Flask API Server**: Handles HTTP requests and serves the model
- **BLIP Model**: Responsible for image captioning
- **Kubernetes Deployment**: Manages container lifecycle and scaling
- **LoadBalancer Service**: Exposes the API to external traffic
- **HPA**: Automatically scales based on CPU utilization
- **Prometheus Metrics**: Collects performance and operational metrics

## Monitoring

The application includes built-in monitoring capabilities through Prometheus metrics:

### Available Metrics

- `infer_requests_total`: Counter tracking the total number of inference requests
- `infer_latency_seconds`: Histogram measuring inference request latency

### Example Metrics Output

```
# HELP infer_requests_total Total inference requests
# TYPE infer_requests_total counter
infer_requests_total 42.0
# HELP infer_latency_seconds Inference latency
# TYPE infer_latency_seconds histogram
infer_latency_seconds_bucket{le="0.005"} 0.0
infer_latency_seconds_bucket{le="0.01"} 0.0
infer_latency_seconds_bucket{le="0.025"} 0.0
infer_latency_seconds_bucket{le="0.05"} 0.0
infer_latency_seconds_bucket{le="0.075"} 0.0
infer_latency_seconds_bucket{le="0.1"} 0.0
infer_latency_seconds_bucket{le="0.25"} 8.0
infer_latency_seconds_bucket{le="0.5"} 29.0
infer_latency_seconds_bucket{le="0.75"} 37.0
infer_latency_seconds_bucket{le="1.0"} 39.0
infer_latency_seconds_bucket{le="2.5"} 42.0
infer_latency_seconds_bucket{le="5.0"} 42.0
infer_latency_seconds_bucket{le="7.5"} 42.0
infer_latency_seconds_bucket{le="10.0"} 42.0
infer_latency_seconds_bucket{le="+Inf"} 42.0
infer_latency_seconds_count 42.0
infer_latency_seconds_sum 15.98261260986328
```

### Setting Up Monitoring

To monitor your application in a Kubernetes environment:

1. Deploy Prometheus and Grafana using the Prometheus Operator:
```bash
kubectl apply -f https://github.com/prometheus-operator/kube-prometheus/releases/latest/download/kube-prometheus.yaml
```

2. Wait for all monitoring components to be running:
```bash
kubectl wait --for=condition=Ready pods -n monitoring --all
```

3. Apply the ServiceMonitor and PrometheusRule custom resources:
```bash
kubectl apply -f k8s/prometheus/service-monitor.yaml
kubectl apply -f k8s/prometheus/alert-rules.yaml
```

4. Access Grafana dashboards to visualize metrics:
```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

5. Import the provided Grafana dashboard:
   - Navigate to Grafana UI (http://localhost:3000)
   - Go to Dashboards > Import
   - Upload the JSON file from `k8s/prometheus/grafana-dashboard.json`
   - Select the Prometheus data source and click Import

### Monitoring Dashboard

The included Grafana dashboard provides:

- Inference Request Rate: Tracks the number of inference requests per second
- Inference Latency: Shows p50, p95, and p99 latency metrics
- Total Inferences: Counts the total number of inferences over 24 hours
- P95 Latency: Highlights the 95th percentile latency
- GPU Utilization: Monitor GPU usage with NVIDIA DCGM exporter
- Memory and CPU Usage: Track system resource consumption

### Alerting

The service includes preconfigured alert rules (`k8s/prometheus/alert-rules.yaml`):

1. **HighInferLatency**: Triggers when 95th percentile latency exceeds 1 second
2. **HighErrorRate**: Alerts when HTTP error rate exceeds 5%
3. **ServiceDown**: Fires when the service is unavailable for more than 1 minute

## License

MIT