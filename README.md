# ClarityXR — Pneumonia Detection Workflow

ClarityXR is a full-stack educational application for chest X-ray research workflows. Patients can upload de-identified images, approved doctors can review results and add notes, and administrators control practitioner access. A TensorFlow CNN training pipeline and model adapter connect the workflow to a locally trained model.

> **Important:** This project is an educational demonstration. It is not a medical device and must not be used to diagnose, treat, or make clinical decisions.

## Features

- Patient, doctor, and administrator roles
- JWT authentication and administrator approval for doctor accounts
- X-ray upload, analysis history, confidence display, and model version tracking
- Approved-doctor review queue and notes
- Administrator user approval dashboard
- TensorFlow CNN training script with early stopping and test evaluation
- Explicit failure state when no trained model is configured—no fabricated predictions
- Responsive React and TypeScript interface

## Stack

React, TypeScript, Vite, Django, Django REST Framework, Simple JWT, SQLite, TensorFlow, Pillow.

## Local setup

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The seed command creates `patient_demo`, `doctor_demo`, and `admin_demo`. Their password comes from `DEMO_PASSWORD` in `.env`; never use the local demonstration password in production.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

The Docker frontend is available at `http://localhost:5174` and the API at `http://localhost:8000/api`.

## Train the model

Download the CC BY 4.0 Mendeley dataset (DOI: `10.17632/rscbjbr9sj.2`) and place the chest X-ray folders in `data/train` and `data/test`, each containing `NORMAL` and `PNEUMONIA`. The script creates a seeded 80/20 validation split from training data and leaves the test set untouched. Then run:

```bash
source .venv/bin/activate
cd backend
python train.py
```

The best checkpoint is written to `model_artifacts/pneumonia_cnn.keras`; test metrics and confusion-matrix counts are written to `model_artifacts/evaluation.json`. Report performance only from this generated evaluation, with dataset provenance and limitations.
