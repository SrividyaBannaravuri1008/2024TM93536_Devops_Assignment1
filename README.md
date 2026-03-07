# ACEest Fitness & Gym — DevOps CI/CD Pipeline

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-3.0.3-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

> **Assignment 1 — Introduction to DevOps (CSIZG514/SEZG514)**  
> Implementing Automated CI/CD Pipelines for ACEest Fitness & Gym

---

## 📋 Project Overview

This project demonstrates a complete DevOps workflow for the **ACEest Fitness & Gym** web application. The Flask REST API exposes endpoints for managing fitness programs, client profiles, calorie calculations, and BMI analysis. The project is containerised with Docker and ships with a fully automated CI/CD pipeline using GitHub Actions, with a secondary build gate via Jenkins.

---

## 🗂️ Repository Structure

```
aceest-devops/
├── app.py                        # Flask application (main source)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Multi-stage Docker image
├── Jenkinsfile                   # Jenkins pipeline (BUILD stage)
├── tests/
│   └── test_app.py               # Pytest test suite (30+ tests)
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD pipeline
└── README.md                     # This file
```

---

## 🚀 Local Setup & Execution

### Prerequisites
- Python 3.11+
- Docker (optional for container testing)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/aceest-devops.git
cd aceest-devops
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# or
venv\Scripts\activate          # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask application
```bash
python app.py
```
The app starts on **http://localhost:5000**

### 5. Test the API (example with curl)
```bash
# Health check
curl http://localhost:5000/health

# List programs
curl http://localhost:5000/programs

# Calculate calories
curl -X POST http://localhost:5000/calories \
  -H "Content-Type: application/json" \
  -d '{"weight": 70, "program": "Fat Loss (FL) - 3 day"}'

# Calculate BMI
curl -X POST http://localhost:5000/bmi \
  -H "Content-Type: application/json" \
  -d '{"weight": 70, "height": 175}'
```

---

## 🧪 Running Tests Manually

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage report
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Run a specific test
```bash
pytest tests/test_app.py::test_calculate_calories_valid -v
```

### Expected output (summary)
```
tests/test_app.py::test_index_returns_200 PASSED
tests/test_app.py::test_health_check PASSED
tests/test_app.py::test_get_programs_returns_list PASSED
...
========= 32 passed in 0.45s ==========
```

---

## 🐳 Docker

### Build the image
```bash
docker build -t aceest-fitness:latest .
```

### Run the container
```bash
docker run -p 5000:5000 aceest-fitness:latest
```

### Run tests inside the container
```bash
docker run --rm aceest-fitness:latest python -m pytest tests/ -v
```

### Key Dockerfile design decisions
- **Multi-stage build** — separates build dependencies from the runtime image, keeping the final image minimal.
- **Non-root user** — the application runs as `aceest` (not root) for security best practice.
- **Health check** — Docker monitors `/health` every 30 seconds to detect unhealthy containers automatically.
- **Layer caching** — `COPY requirements.txt` is done before `COPY app.py` so pip install is only re-run when dependencies change, not on every code change.

---

## ⚙️ Jenkins BUILD Integration

### Overview
Jenkins handles the primary **BUILD** stage. It acts as a quality gate — every time code is pushed, Jenkins:
1. Pulls the latest code from GitHub.
2. Sets up a clean Python virtual environment.
3. Runs `flake8` for syntax checking.
4. Executes the full Pytest suite, publishing JUnit XML results.
5. Builds the Docker image and runs tests inside the container.

### Jenkins Setup Steps
1. Install Jenkins (see [https://www.jenkins.io/doc/book/installing/](https://www.jenkins.io/doc/book/installing/))
2. Install plugins: **Git**, **Pipeline**, **Docker Pipeline**, **JUnit**
3. Create a new **Pipeline** project
4. Under *Pipeline Definition*, select **Pipeline script from SCM**
5. Set SCM to **Git** and enter your repository URL
6. Set *Script Path* to `Jenkinsfile`
7. Save and click **Build Now**

Jenkins reads the `Jenkinsfile` at the root of the repository and executes the `pipeline` block automatically on each build trigger.

---

## 🔄 GitHub Actions CI/CD Pipeline

The pipeline is defined in `.github/workflows/main.yml` and triggers on every `push` or `pull_request` to `main`.

### Pipeline Stages

```
Push / PR
   │
   ▼
┌──────────────────┐
│  Job 1           │
│  Build & Lint    │  ← pip install, flake8 syntax check
└──────────┬───────┘
           │ on success
           ▼
┌──────────────────────┐
│  Job 2               │
│  Docker Image Build  │  ← docker buildx, saves image as artifact
└──────────┬───────────┘
           │ on success
           ▼
┌───────────────────────────┐
│  Job 3                    │
│  Automated Tests (Pytest) │  ← loads Docker image, runs pytest inside container
└───────────────────────────┘
```

**Job 1 — Build & Lint:** Installs Python dependencies, runs `flake8` on `app.py` to catch syntax errors and undefined names. Hard-fails on critical errors; reports style warnings without blocking.

**Job 2 — Docker Image Assembly:** Uses `docker/build-push-action` with GitHub Actions cache to build the multi-stage Docker image. The image is saved as a build artifact and passed to the next job.

**Job 3 — Automated Testing:** Downloads the Docker artifact, loads the image, and executes `pytest` inside the containerised environment. This confirms the application works identically in Docker as it does locally. A coverage XML report is uploaded as an artifact.

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | App info |
| GET | `/health` | Health check |
| GET | `/programs` | List all programs |
| GET | `/programs/<name>` | Get program details |
| POST | `/calories` | Calculate daily calories |
| GET | `/clients` | List all clients |
| POST | `/clients` | Save a client |
| GET | `/clients/<name>` | Get client by name |
| POST | `/bmi` | Calculate BMI |

---

## 🔖 Git Commit Strategy

This repository follows conventional commit messages:

```
feat: add Flask REST API with calorie calculator endpoint
feat: add BMI calculation endpoint with category classification
test: add pytest suite covering all endpoints (30+ test cases)
chore: add Dockerfile with multi-stage build and non-root user
ci: add GitHub Actions pipeline with build, docker, and test jobs
ci: add Jenkinsfile with lint, test, and docker build stages
docs: add comprehensive README with setup and integration guide
```

---

## 👤 Author

BITS Pilani — Introduction to DevOps (S2-2025)
