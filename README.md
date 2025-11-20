![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

[![Web App CI](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/web-app.yml/badge.svg)](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/web-app.yml)

[![Machine Learning Client CI](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/machine-learning-client.yml/badge.svg)](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/machine-learning-client.yml)



# 🧱 Containerized Hand Gesture Recognition System

A fully containerized machine-learning pipeline that captures a hand gesture from the browser, analyzes it with MediaPipe, stores results in MongoDB, and displays them in a clean Flask web interface.  
All services run seamlessly together using **Docker Compose** and are continuously validated by **GitHub Actions**.

---

## 📌 Overview

This repository contains a complete multi-container system with three main components:

### **🧠 Machine Learning Client**
- Receives base64-encoded images from the web app  
- Uses MediaPipe to detect hand landmarks and classify gestures  
- Stores gesture readings and analysis results in MongoDB  

### **🌐 Web App**
- Flask-based frontend  
- Displays the most recent gesture analysis  
- Sends captured images to the ML client  

### **🗄️ MongoDB Database**
- Stores gesture data and ML outputs  
- Shared and networked automatically inside Docker  

---

## 👥 Team Members
- **Conor Tiernan** — https://github.com/ct-04  
-  
-  
-  
-  

---

## 🚀 Getting Started

This guide explains how to run the entire system on **Windows, macOS, or Linux**.

---

## ✔ 1. Prerequisites

Install the following:

- **Docker Desktop**  
- **Git**

---

## ✔ 2. Clone the Repository


git clone https://github.com/nyu-software-engineering/4-containers-the-lego-movie.git
cd 4-containers-the-lego-movie

---

## ✔ 3. Create the Environment File
You can copy the example file:

- cp env.example .env
- Or create it manually:

- Use .env file provided in submission

---

## ✔ 4. Launch All Services
Build and start every container:


- docker compose up --build

---

## ✔ 5. Access the Web Interface
Once everything is running, open:

- http://localhost:5050

---

## ✔ 6. Running Tests Locally

Each subsystem has its own virtual environment managed with pipenv.

ML Client Tests
- cd machine-learning-client
- pipenv install --dev
- pipenv run pytest --cov

Web App Tests
- cd web-app
- pipenv install --dev
- pipenv run pytest --cov

---

## ✔ 7. Linting & Formatting

Both subsystems must satisfy PEP8 (Black + pylint).

Run Black
- pipenv run black .

Run Pylint
- pipenv run pylint app.py
- pipenv run pylint tests

---

## ✔ 8. Developer Local-Run Instructions (Without Docker)

Web App Only
- cd web-app
- pipenv install
- pipenv run flask run --port 5000

Machine Learning Client Only
- cd machine-learning-client
- pipenv install
- pipenv run flask run --port 5001


Make sure MongoDB is running locally on localhost:27017.

---



# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.
