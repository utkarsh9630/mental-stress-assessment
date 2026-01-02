# Mental Stress Assessment and Recommendation System

A machine learning-powered web application that predicts stress levels and provides personalized coping mechanism recommendations.

## Features

- Stress level prediction (Low/Medium/High)
- Probability distribution across stress categories
- Personalized coping mechanism recommendations based on k-NN similarity
- User-friendly web interface
- REST API endpoints

## Project Structure

```
stress_app/
├── app.py                      # Flask application
├── templates/
│   └── index.html             # Web interface
├── models/                     # ML models and artifacts
│   ├── rf_model.joblib        # Random Forest classifier
│   ├── knn_model.joblib       # k-NN recommendation model
│   ├── scaler.joblib          # Feature scaler
│   ├── imputer.joblib         # Missing value imputer
│   ├── feature_columns.json   # Feature list
│   ├── rec_feature_columns.json
│   └── label_map.json         # Label encoding map
├── data/
│   └── train_recs.csv         # Training data for recommendations
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Local Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd stress_app
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Open browser and navigate to `http://localhost:5000`

## Deployment

### Deploy to Render

1. Create a new account at [render.com](https://render.com)

2. Create a new Web Service

3. Connect your GitHub repository

4. Configure the service:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

5. Add environment variables (if needed)

6. Deploy

### Deploy to Heroku

1. Install Heroku CLI

2. Login to Heroku
```bash
heroku login
```

3. Create a Procfile in the root directory:
```
web: gunicorn app:app
```

4. Create a new Heroku app
```bash
heroku create your-app-name
```

5. Push to Heroku
```bash
git push heroku main
```

6. Open the app
```bash
heroku open
```

### Deploy to Railway

1. Create account at [railway.app](https://railway.app)

2. Create new project from GitHub repo

3. Railway will auto-detect the Python app

4. Set start command: `gunicorn app:app`

5. Deploy

## API Usage

### Predict Endpoint

**POST /predict**

Request body:
```json
{
  "age": 22,
  "gpa": 3.5,
  "study_hours": 25,
  "social_media": 3,
  "sleep": 7,
  "exercise": 5,
  "family_support": 4,
  "financial_stress": 2,
  "peer_pressure": 3,
  "relationship_stress": 2,
  "counseling": "No",
  "diet_quality": 4,
  "cognitive_distortions": 2,
  "family_mental_history": "No",
  "medical_condition": "No",
  "substance_use": 1,
  "gender": "Female",
  "current_mechanisms": ["Exercise", "Reading"]
}
```

Response:
```json
{
  "prediction": "Low",
  "probabilities": {
    "Low": 0.65,
    "Medium": 0.25,
    "High": 0.10
  },
  "drop_probability": 0.0,
  "recommendations": [
    {
      "mechanism": "Meditation",
      "success_rate": 0.78
    },
    {
      "mechanism": "Yoga",
      "success_rate": 0.72
    }
  ]
}
```

## Model Information

### Classification Model
- Algorithm: Random Forest Classifier
- Features: 20 features including demographics, academic, lifestyle, and health factors
- Target: Stress Level (Low/Medium/High)
- Accuracy: ~65% on test set

### Recommendation Model
- Algorithm: k-Nearest Neighbors (k=50)
- Returns top 5 coping mechanisms based on success rate in similar individuals
- Success defined as achieving "Low" stress level

## License

MIT License

## Contact

For questions or issues, please open an issue on GitHub.
