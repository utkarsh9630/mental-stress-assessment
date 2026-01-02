# Project Summary

## Mental Stress Assessment and Recommendation System

### Overview
This is a full-stack machine learning web application that predicts student mental stress levels and provides personalized coping mechanism recommendations.

### Technical Stack

**Backend:**
- Python 3.11
- Flask 3.0 (Web framework)
- Gunicorn (Production server)

**Machine Learning:**
- scikit-learn 1.3.2
- Random Forest Classifier (stress prediction)
- k-Nearest Neighbors (recommendations)
- pandas, numpy (data processing)

**Frontend:**
- HTML5
- CSS3 (with gradient backgrounds and animations)
- Vanilla JavaScript (no frameworks)

### System Architecture

```
User Browser
     |
     | HTTP Request
     v
Flask Application (app.py)
     |
     |-- Load Models (startup)
     |      - Random Forest Classifier
     |      - k-NN Model
     |      - Scaler & Imputer
     |
     |-- Process Input
     |      - Feature engineering
     |      - Data validation
     |
     |-- Make Predictions
     |      - Stress level classification
     |      - Probability distribution
     |
     |-- Generate Recommendations
     |      - Find similar individuals (k-NN)
     |      - Calculate success rates
     |      - Filter current mechanisms
     |
     v
JSON Response to User
```

### Models

#### 1. Classification Model
- **File:** models/rf_model.joblib (66MB)
- **Algorithm:** Random Forest Classifier
- **Input:** 20 features
- **Output:** Stress level (Low/Medium/High) + probabilities
- **Performance:** ~65% accuracy on test set

#### 2. Recommendation Model
- **File:** models/knn_model.joblib (631KB)
- **Algorithm:** k-Nearest Neighbors (k=50)
- **Input:** Same 20 features
- **Output:** Top 5 recommended coping mechanisms
- **Logic:** Find similar individuals, calculate success rates

### Features Used

1. Age
2. Academic Performance (GPA)
3. Study Hours Per Week
4. Social Media Usage (weekly)
5. Sleep Duration (hours/night)
6. Physical Exercise (hours/week)
7. Family Support (1-5)
8. Financial Stress (1-5)
9. Peer Pressure (1-5)
10. Relationship Stress (1-5)
11. Counseling Attendance (Yes/No)
12. Diet Quality (1-5)
13. Cognitive Distortions (1-5)
14. Family Mental Health History (Yes/No)
15. Medical Condition (Yes/No)
16. Substance Use (0-5)
17. Gender (Female/Male/Other - one-hot encoded)
18. Stress Ratio (calculated feature)

### API Endpoints

**POST /predict**
- Accepts user input
- Returns stress prediction and recommendations

**GET /health**
- Health check endpoint
- Returns {"status": "healthy"}

**GET /**
- Serves the web interface

### File Structure

```
stress_app/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version
├── Procfile                        # Heroku deployment config
├── setup.sh                        # Setup script
├── test_app.py                     # Testing script
├── .gitignore                      # Git ignore rules
│
├── templates/
│   └── index.html                  # Web interface
│
├── models/
│   ├── rf_model.joblib            # Random Forest model
│   ├── knn_model.joblib           # k-NN model
│   ├── scaler.joblib              # Feature scaler
│   ├── imputer.joblib             # Missing value imputer
│   ├── feature_columns.json       # Feature list
│   ├── rec_feature_columns.json   # Recommendation features
│   └── label_map.json             # Label encoding
│
├── data/
│   └── train_recs.csv             # Training data for recommendations
│
├── .github/workflows/
│   └── ci.yml                     # GitHub Actions CI
│
└── Documentation/
    ├── README.md                  # Project overview
    ├── DEPLOYMENT.md              # Deployment guide
    └── QUICKSTART.md              # Quick start guide
```

### Key Features

1. **User-Friendly Interface**
   - Clean, modern design
   - Gradient background
   - Interactive sliders
   - Real-time visual feedback

2. **Intelligent Predictions**
   - Multi-class stress classification
   - Probability distributions
   - Confidence scores

3. **Personalized Recommendations**
   - Based on similar individuals
   - Filters already-used mechanisms
   - Shows success rates
   - Top 5 suggestions

4. **Production Ready**
   - Error handling
   - Input validation
   - Health check endpoint
   - Gunicorn for production
   - CI/CD with GitHub Actions

### Deployment Options

1. **Render** (Recommended)
   - Free tier available
   - Handles large model files well
   - Automatic HTTPS

2. **Railway**
   - Fast deployments
   - Auto-detects Python
   - Good free tier

3. **Heroku**
   - Requires paid plan
   - Industry standard
   - Good documentation

### Security Considerations

- Input validation on all form fields
- No user data storage (currently)
- HTTPS enforced on cloud platforms
- No hardcoded credentials
- Environment variable support ready

### Performance

- Model loading: ~2-3 seconds on startup
- Prediction time: <100ms
- Recommendation generation: ~200ms
- Total response time: <500ms

### Limitations

1. No user authentication (yet)
2. No result history storage
3. Limited to 10 predefined coping mechanisms
4. No mobile app version
5. Free tier may sleep after inactivity

### Future Enhancements

1. User accounts and authentication
2. Result history and tracking
3. Progress monitoring over time
4. More coping mechanisms
5. Mobile responsive improvements
6. Database integration (PostgreSQL)
7. Email notifications
8. Export results as PDF
9. Multi-language support
10. Admin dashboard

### Data Flow

1. User fills form → JavaScript collects data
2. POST to /predict → Flask receives JSON
3. Feature engineering → Stress Ratio calculation
4. Imputation → Handle missing values
5. Scaling → Standardize features
6. RF Classification → Get stress level + probabilities
7. k-NN Search → Find similar individuals
8. Calculate success rates → Rank mechanisms
9. Return JSON → JavaScript displays results

### Model Training Pipeline (Original)

1. Load raw data (Mental_Stress_and_Coping_Mechanisms_processed.csv)
2. Feature engineering (Gender consolidation, Stress_Ratio)
3. Outlier removal (IQR method on Study Hours)
4. Train-test split (70-30, stratified)
5. SMOTE oversampling (handle class imbalance)
6. StandardScaler (feature scaling)
7. Random Forest training (with hyperparameter tuning)
8. k-NN fitting (on training features)
9. Model evaluation and saving

### Metrics

**Classification:**
- Accuracy: 65%
- Balanced across Low/Medium/High classes
- F1-scores: 0.57-0.69 per class

**Recommendations:**
- Success rate: 62-63%
- Based on "Low stress" outcome
- Average 5 recommendations per user

### Technologies & Libraries

- Flask==3.0.0
- pandas==2.1.3
- numpy==1.26.2
- scikit-learn==1.3.2
- joblib==1.3.2
- gunicorn==21.2.0

### License
MIT License

### Contact
GitHub repository: (add your repo URL)

### Acknowledgments
- Dataset: Mental Stress and Coping Mechanisms dataset
- Model architecture: Random Forest + k-NN hybrid approach
- UI inspiration: Modern gradient designs
