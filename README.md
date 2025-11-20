![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

[![Web App CI](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/web-app.yml/badge.svg)](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/web-app.yml)

[![Machine Learning Client CI](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/machine-learning-client.yml/badge.svg)](https://github.com/swe-students-fall2025/4-containers-the-lego-movie/actions/workflows/machine-learning-client.yml)


📌 Overview

This project is a fully containerized system that recognises hand gestures and displays an output image on the screen.
A browser captures a hand gesture, sends it to a Machine Learning Client, which analyzes the image using MediaPipe, stores the data in MongoDB, and displays the results through a Flask Web App.

This repo contains three fully integrated subsystems:

Machine Learning Client
Processes base64-encoded images, detects hand gestures, and stores results in MongoDB.

Web App
A Flask application that renders stored gesture results in a simple UI.

MongoDB Database
A database for storing gesture readings and analysis results.

All components run together using Docker Compose, and are built/tested via GitHub Actions.

👥 Team Members
- Conor Tiernan(https://github.com/ct-04)
-
-
-
-





# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.
