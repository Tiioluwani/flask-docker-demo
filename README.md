# flask-docker-demo

A minimal Flask REST API containerised with Docker. Exposes a health-check endpoint and a `/predict` endpoint powered by a scikit-learn linear regression model trained at startup.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with the Docker engine running)
- Python 3.13 (only needed for local development outside Docker)

---

## Build & Run

**Build the image:**
```bash
docker build -t flask-sklearn-demo .
```

**Run the container:**
```bash
docker run -p 5000:5000 -e APP_ENV=production flask-sklearn-demo
```

**If port 5000 is already in use, map to 5001 instead:**
```bash
docker run -p 5001:5000 -e APP_ENV=production flask-sklearn-demo
```
Then replace `5000` with `5001` in all requests below.

---

## Endpoints

### GET `/` — health check

**Command Prompt:**
```cmd
curl http://localhost:5000/
```

**PowerShell:**
```powershell
curl http://localhost:5000/
```

**Response:**
```json
{"app": "flask-sklearn-demo", "status": "ok", "version": "1.0.0"}
```

---

### POST `/predict` — run a prediction

Accepts a JSON body with a `features` list of exactly 2 numbers.

**Command Prompt:**
```cmd
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"features\": [4.0, 2.5]}"
```

**PowerShell:**
```powershell
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"features": [4.0, 2.5]}'
```

**Response:**
```json
{"prediction": 17.0}
```

---

## Project Structure

```
flask-docker-demo/
├── app.py              # Flask app and model training
├── Dockerfile          # Container definition (python:3.13-slim + gunicorn)
├── requirements.txt    # Pinned dependencies
└── .dockerignore       # Files excluded from the Docker build context
```
