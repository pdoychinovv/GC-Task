### URL Monitoring Service – Prometheus Exporter

A lightweight, Dockerized Python service that continuously monitors the status and response time of two external URLs, exposing this information in Prometheus format. The app can be run locally via Docker or deployed into a Kubernetes cluster using Helm.

---

#### Features

- Periodically checks the availability of:
    - `https://httpstat.us/200` (expected: HTTP 200, **UP**)
    - `https://httpstat.us/503` (expected: HTTP 503, **DOWN**)
- Measures response time in milliseconds
- Exposes Prometheus-compatible metrics at [http://localhost:8000](http://localhost:8000)

---

#### Sample Prometheus Metrics

```text
# HELP sample_external_url_up URL availability
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0
sample_external_url_up{url="https://httpstat.us/200"} 1

# HELP sample_external_url_response_ms URL response time in milliseconds
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 602.81
sample_external_url_response_ms{url="https://httpstat.us/200"} 610.16
```

---

#### Running Locally with Docker

```sh
# Build the Docker image
docker build -t url-monitor:latest .

# Run the container
docker run -d -p 8000:8000 --name url-monitor url-monitor:latest

# View the metrics
curl http://localhost:8000
```

---

#### Helm Chart Structure

```
helm/
├── Chart.yaml
├── values.yaml
└── templates/
        ├── deployment.yaml
        └── service.yaml
```

---

#### Deploying with Helm

```sh
# If using Minikube, load the image locally
minikube image load url-monitor:latest

# Install the chart
helm install url-monitor ./helm

# Access the service
kubectl port-forward svc/url-monitor 8000:80
curl http://localhost:8000
```

---

**Tip:** Customize the monitored URLs and scrape intervals in the configuration files as needed.
