### ACEest Fitness & Gym — DevOps CI/CD Pipeline

> **Assignment 1 — Srividya Bannaravuri(2024TM93536)**  
> Introduction to Devops - CI/CD Pipelines for ACEest Fitness & Gym

### 📋 Project Overview

This project demonstrates a complete DevOps workflow for the ACEest Fitness & Gym web application. The project is containerised with Docker and ships with a fully automated CI/CD pipeline using GitHub Actions, and Jenkins.

### Repository Structure

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

### GitHub Actions CI/CD Pipeline Stages

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

