# Mental Stress Assessment and Recommendation System

A full-stack machine learning web application that predicts student mental stress levels and delivers personalized coping mechanism recommendations based on academic, lifestyle, and psychosocial inputs.

#Live URL: https://mental-stress-assessment.vercel.app/login

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Machine Learning Models](#machine-learning-models)
- [Input Features](#input-features)
- [API Endpoints](#api-endpoints)
- [Local Setup](#local-setup)
- [Deployment](#deployment)
- [Retraining Models](#retraining-models)
- [Database](#database)
- [Testing](#testing)

---

## Overview

This application accepts a student's academic and lifestyle data through a web form, runs it through a trained Random Forest classifier to predict a stress level (Low, Medium, or High), and then uses a k-Nearest Neighbors model to recommend coping strategies that worked best for similar individuals. Each assessment is stored per user profile, enabling longitudinal tracking.

---

## Features

- User registration, login, and session management via Flask-Login
- Multi-profile support per user account (e.g. track different individuals)
- Stress level classification with per-class probability scores
- Academic drop risk probability derived from classification output
- KNN-powered coping mechanism recommendations ranked by real-world success rate
- Full assessment history per profile
- REST endpoint for programmatic prediction
- Health check endpoint for uptime monitoring
- PostgreSQL support for production with automatic URI correction for Render
- SQLite fallback for local development

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Flask 3.0 |
| Production server | Gunicorn |
| Machine learning | scikit-learn, pandas, numpy, joblib |
| Authentication | Flask-Login, Werkzeug |
| Forms | Flask-WTF |
| Database ORM | Flask-SQLAlchemy |
| Database | SQLite (dev), PostgreSQL (prod) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Environment | python-dotenv |

---

## Project Structure

```
.
├── app.py                        # Main Flask application and all routes
├── models.py                     # SQLAlchemy models (User, Profile, Assessment)
├── forms.py                      # WTForms definitions for registration, login, profile
├── predict_classification.py     # Standalone batch classification utility
├── predict_recommendation.py     # Standalone recommendation utility
├── retrain_models.py             # Script to retrain all models from scratch
├── init_db.py                    # Database initialization helper
├── test_app.py                   # Application tests
├── requirements.txt              # Python dependencies
├── runtime.txt                   # Python version pin (3.11.7)
├── Procfile                      # Gunicorn start command for cloud platforms
├── build.sh                      # Build script
├── setup.sh                      # Environment setup script
│
├── models/                       # Trained model artifacts
│   ├── rf_model.joblib           # Random Forest classifier (~66 MB)
│   ├── knn_model.joblib          # k-NN model for recommendations (~631 KB)
│   ├── scaler.joblib             # StandardScaler
│   ├── imputer.joblib            # SimpleImputer (mean strategy)
│   ├── feature_columns.json      # Ordered list of classification features
│   ├── rec_feature_columns.json  # Feature list used by the KNN model
│   └── label_map.json            # Integer-to-label mapping (0=Low, 1=Medium, 2=High)
│
├── data/
│   └── train_recs.csv            # Training data used by the recommendation engine
│
├── templates/
│   ├── base.html                 # Base layout template
│   ├── index.html                # Landing / home page
│   ├── assess.html               # Assessment form
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── dashboard/
│       ├── dashboard.html
│       ├── profile.html
│       └── create_profile.html
│
├── PROJECT_SUMMARY.md
├── DEPLOYMENT.md
├── DEPLOYMENT_CHECKLIST.md
└── QUICKSTART.md
```

---

## Machine Learning Models

### Stress Classification (Random Forest)

- **Algorithm:** Random Forest Classifier
- **Input:** 20 engineered features
- **Output:** Stress level category — Low, Medium, or High — plus per-class probabilities
- **Accuracy:** ~65% on a 30% held-out test set, balanced across all three classes (F1 scores 0.57–0.69)
- **Artifact:** `models/rf_model.joblib`

### Coping Mechanism Recommendation (k-Nearest Neighbors)

- **Algorithm:** k-NN with k=50, Euclidean distance
- **Input:** Same 20 features
- **Output:** Top 5 coping mechanisms not already in use, ranked by success rate among similar individuals (where "success" means the neighbor ended up in the Low stress category)
- **Artifact:** `models/knn_model.joblib`

### Preprocessing

- **Imputer:** `SimpleImputer(strategy='mean')` to handle missing values
- **Scaler:** `StandardScaler` applied after imputation
- Both are fitted only on training data and serialized to `models/`

### Training Pipeline Summary

1. Load and clean the raw dataset
2. Reconstruct the target label from one-hot dummy columns
3. Consolidate minority gender categories into `Gender_Other`
4. Calculate `Stress_Ratio` as a derived feature
5. Remove outliers from Study Hours using the IQR method
6. Stratified 70/30 train-test split
7. Fit imputer and scaler on training data
8. Train Random Forest on scaled training data
9. Fit k-NN on the same scaled training features
10. Serialize all artifacts to `models/`

---

## Input Features

The following 20 features are collected through the assessment form and passed to both models.

| Feature | Type | Notes |
|---|---|---|
| Age | Numeric | |
| Academic Performance (GPA) | Numeric | |
| Study Hours Per Week | Numeric | |
| Social Media Usage (per week) | Numeric | Daily value multiplied by 7 |
| Sleep Duration (hours/night) | Numeric | |
| Physical Exercise (hours/week) | Numeric | |
| Family Support | Integer 1–5 | |
| Financial Stress | Integer 1–5 | |
| Peer Pressure | Integer 1–5 | |
| Relationship Stress | Integer 1–5 | |
| Counseling Attendance | Binary | Yes=1, No=0 |
| Diet Quality | Integer 1–5 | |
| Cognitive Distortions | Integer 1–5 | |
| Family Mental Health History | Binary | Yes=1, No=0 |
| Medical Condition | Binary | Yes=1, No=0 |
| Substance Use | Integer 0–5 | |
| Gender (Female / Male / Other) | One-hot encoded | |
| Stress Ratio | Derived | `(Financial + Peer + Relationship) / (Family Support + Diet + Exercise)` |

---

## API Endpoints

### POST `/predict`

Requires authentication. Accepts a JSON body and returns stress prediction, probability distribution, drop risk, and recommendations.

**Request body:**
```json
{
  "profile_id": 1,
  "age": 21,
  "gpa": 3.2,
  "study_hours": 20,
  "social_media": 3,
  "sleep": 6.5,
  "exercise": 2,
  "family_support": 3,
  "financial_stress": 4,
  "peer_pressure": 3,
  "relationship_stress": 2,
  "counseling": "No",
  "diet_quality": 3,
  "cognitive_distortions": 2,
  "family_mental_history": "No",
  "medical_condition": "No",
  "substance_use": 1,
  "gender": "Male",
  "current_mechanisms": ["Exercise", "Journaling"]
}
```

**Response:**
```json
{
  "prediction": "Medium",
  "probabilities": {
    "Low": 0.24,
    "Medium": 0.51,
    "High": 0.25
  },
  "drop_probability": 0.24,
  "recommendations": [
    {"mechanism": "Mindfulness Meditation", "success_rate": 0.68},
    ...
  ]
}
```

### GET `/health`

Returns `{"status": "healthy"}`. Used for uptime checks and platform health monitoring.

### GET `/init-db`

Creates all database tables. Run once on first deployment, then remove or restrict access.

---

## Local Setup

### Prerequisites

- Python 3.11
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mental-stress-assessment.git
cd mental-stress-assessment

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application starts at `http://localhost:5000`.

### Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///stress_assessment.db
```

For production with PostgreSQL:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/dbname
```

The application automatically converts `postgres://` URIs (used by Render) to `postgresql://` format.

---

## Deployment

### Render (Recommended)

1. Push the repository to GitHub, including all files in `models/` and `data/`.
2. Create a new Web Service on [render.com](https://render.com) connected to your repository.
3. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3
4. Add `SECRET_KEY` and `DATABASE_URL` environment variables in the Render dashboard.
5. After the first deploy, navigate to `/init-db` once to create the database tables.

**Note:** The Random Forest model file is approximately 66 MB. Ensure Git LFS is configured or models are committed directly before pushing. Free tier instances will sleep after inactivity and take 30–60 seconds to wake on the first request.

### Railway

1. Connect your GitHub repository at [railway.app](https://railway.app).
2. Set start command to `gunicorn app:app --bind 0.0.0.0:$PORT` in Settings.
3. Add environment variables under the Variables tab.

### Local production mode

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

---

## Retraining Models

To retrain all models from a new dataset:

```bash
python retrain_models.py
```

This script expects a file named `Mental_Stress_and_Coping_Mechanisms_processed_final.csv` in the working directory. It will overwrite all artifacts in `models/`.

To run batch classification on a CSV without the web interface:

```bash
python predict_classification.py
```

---

## Database

Three tables are created under the prefixed names `stress_users`, `stress_profiles`, and `stress_assessments`.

- **User** — stores credentials and owns multiple profiles
- **Profile** — a named subject (e.g. a student being assessed), linked to a user
- **Assessment** — a full snapshot of one prediction run, including all input values, the predicted stress level, probabilities, drop risk, and the recommended mechanisms stored as a JSON string

Cascade deletion is configured so that deleting a user removes all their profiles, and deleting a profile removes all its assessments.

---

## Testing

```bash
python test_app.py
```

This runs the test suite defined in `test_app.py` against a local instance of the application.
