# Shopping App: Monolith → Docker → Compose → Kubernetes → Microservices

A practical lab project that starts as a **single Flask monolith** and then evolves into three independently deployable Flask services:
1. Login service
2. Cart service
3. Checkout service

The app is intentionally small and uses in-memory data so it runs without a database or internet after dependencies/images are available. **Demo only:** credentials are hardcoded, cart data resets on restart, and checkout accepts items from the client. Do not use this as a production payment or authentication system.

## Project structure

```text
shopping_app_monolith_to_services/
├── monolith/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── services/
│   ├── login/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── cart/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── checkout/
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
├── compose.monolith.yaml
├── compose.services.yaml
├── .dockerignore
├── k8s/
│   ├── monolith.yaml
│   └── services.yaml
└── README.md
```

## Requirements

- Python 3.10+ for running without Docker
- Docker Engine/Desktop and Docker Compose
- `kubectl` and Minikube for local Kubernetes
- `curl` or Postman for testing APIs

---

# Phase 1 — Run the monolith locally

The monolith has all three features in one Flask application and one process.

From the project root:

```bash
python -m venv .venv
```

Activate the environment:
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows CMD: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Install and run:

```bash
pip install -r monolith/requirements.txt
python monolith/app.py
```

Test endpoints in a second terminal:

```bash
curl http://localhost:5000/
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"1234\"}"
curl -X POST http://localhost:5000/cart -H "Content-Type: application/json" -d "{\"item\":\"Laptop\",\"price\":50000}"
curl http://localhost:5000/cart
curl -X POST http://localhost:5000/checkout -H "Content-Type: application/json" -d "{\"items\":[{\"item\":\"Laptop\",\"price\":50000}]}"
```

Expected:
- `/` returns the service list.
- Login with `admin` / `1234` succeeds.
- Cart POST adds an item; cart GET lists items.
- Checkout returns a confirmed order and total.

Stop the local server with `Ctrl+C`.

## Monolith API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| POST | `/login` | Demo login |
| GET | `/cart` | List in-memory cart |
| POST | `/cart` | Add an item |
| POST | `/checkout` | Calculate total and confirm demo order |

---

# Phase 2 — Build and run the monolith with Docker

Build image:

```bash
docker build -t shopping-monolith:1.0 ./monolith
```

Run container:

```bash
docker run -d --name shopping-monolith -p 5000:5000 shopping-monolith:1.0
```

Check:

```bash
docker ps
docker logs shopping-monolith
curl http://localhost:5000/health
```

Stop and remove:

```bash
docker rm -f shopping-monolith
```

## Run the monolith with Docker Compose

```bash
docker compose -f compose.monolith.yaml up --build -d
docker compose -f compose.monolith.yaml ps
docker compose -f compose.monolith.yaml logs -f
```

Test at `http://localhost:5000`. Stop:

```bash
docker compose -f compose.monolith.yaml down
```

---

# Phase 3 — Run three independent services with Docker Compose

The three service versions are in `services/`. Each has its own Flask app and Dockerfile. For this minimal teaching example, the services are independently deployable but do not automatically call each other; checkout receives the item list from the client.

Build and start:

```bash
docker compose -f compose.services.yaml up --build -d
```

Check status and logs:

```bash
docker compose -f compose.services.yaml ps
docker compose -f compose.services.yaml logs
docker compose -f compose.services.yaml logs login
docker compose -f compose.services.yaml logs cart
docker compose -f compose.services.yaml logs checkout
```

Endpoints:
- Login: `http://localhost:5001`
- Cart: `http://localhost:5002`
- Checkout: `http://localhost:5003`

Test login:

```bash
curl -X POST http://localhost:5001/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"1234\"}"
```

Add and view cart items:

```bash
curl -X POST http://localhost:5002/cart -H "Content-Type: application/json" -d "{\"item\":\"Laptop\",\"price\":50000}"
curl http://localhost:5002/cart
```

Checkout:

```bash
curl -X POST http://localhost:5003/checkout -H "Content-Type: application/json" -d "{\"items\":[{\"item\":\"Laptop\",\"price\":50000},{\"item\":\"Mouse\",\"price\":500}]}"
```

Stop services:

```bash
docker compose -f compose.services.yaml down
```

---

# Phase 4 — Kubernetes

## Option A: Deploy the monolith

Build image:

```bash
docker build -t shopping-monolith:1.0 ./monolith
```

Start Minikube and load the image:

```bash
minikube start
minikube image load shopping-monolith:1.0
```

Deploy and verify:

```bash
kubectl apply -f k8s/monolith.yaml
kubectl get deployments
kubectl get pods
kubectl get services
kubectl rollout status deployment/shopping-monolith
```

Access it:

```bash
kubectl port-forward service/shopping-monolith-service 5000:5000
```

Use a second terminal to test `http://localhost:5000/health`.

Delete:

```bash
kubectl delete -f k8s/monolith.yaml
```

## Option B: Deploy three services

Build the service images:

```bash
docker build -t shopping-login:1.0 ./services/login
docker build -t shopping-cart:1.0 ./services/cart
docker build -t shopping-checkout:1.0 ./services/checkout
```

Load into Minikube:

```bash
minikube image load shopping-login:1.0
minikube image load shopping-cart:1.0
minikube image load shopping-checkout:1.0
```

Deploy:

```bash
kubectl apply -f k8s/services.yaml
kubectl get deployments
kubectl get pods
kubectl get services
```

Wait for rollout:

```bash
kubectl rollout status deployment/login
kubectl rollout status deployment/cart
kubectl rollout status deployment/checkout
```

Port-forward each service in a separate terminal:

```bash
kubectl port-forward service/login-service 5001:5000
kubectl port-forward service/cart-service 5002:5000
kubectl port-forward service/checkout-service 5003:5000
```

Delete:

```bash
kubectl delete -f k8s/services.yaml
```

## Kubernetes troubleshooting

```bash
kubectl get pods -o wide
kubectl describe pod POD_NAME
kubectl logs POD_NAME
kubectl get events --sort-by=.metadata.creationTimestamp
```

If the pod shows `ImagePullBackOff`, ensure the image is built and loaded into the cluster and that the image name/tag in YAML matches exactly.

---

# Common Docker commands

```bash
docker --version
docker images
docker ps
docker ps -a
docker stop CONTAINER
docker start CONTAINER
docker logs CONTAINER
docker exec -it CONTAINER sh
docker rm -f CONTAINER
docker rmi IMAGE
docker compose config
docker compose down
```

# Common Kubernetes commands

```bash
kubectl version --client
kubectl cluster-info
kubectl get nodes
kubectl apply -f FILE.yaml
kubectl get pods
kubectl get deployments
kubectl get services
kubectl describe pod POD_NAME
kubectl logs POD_NAME
kubectl scale deployment/cart --replicas=3
kubectl rollout undo deployment/NAME
kubectl port-forward service/SERVICE_NAME LOCAL_PORT:REMOTE_PORT
kubectl delete -f FILE.yaml
```

# Notes and limitations

- This project is designed for lab learning, not production.
- `admin` / `1234` are hardcoded demo credentials.
- Cart state is stored in process memory and disappears when the process restarts. Multiple replicas do not share cart state.
- Checkout totals items supplied by the client; it does not retrieve them from the cart service or process payments.
- A real system would use secure authentication, shared persistent storage, validated prices from a trusted catalogue, and a proper order/payment workflow.
- If using Kubernetes without internet, ensure the Python base image and any required images are already cached locally before building/loading images.
