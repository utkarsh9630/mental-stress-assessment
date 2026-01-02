# Mental Stress Assessment System

AI-powered web application for predicting student mental stress levels and providing personalized coping mechanism recommendations.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Live Demo

🔗 **[Try it live on Render](https://mental-stress-assessment-ut.onrender.com/login)**

## Features

- **User Authentication** - Secure registration and login system
- **Multi-Profile Management** - Create and manage multiple user profiles
- **AI Predictions** - Random Forest classifier for stress level prediction
- **Personalized Recommendations** - k-NN based coping mechanism suggestions
- **Assessment History** - Track stress levels over time
- **Beautiful UI** - Modern, responsive interface

## Tech Stack

**Backend:**
- Flask 3.0 (Python web framework)
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- PostgreSQL (Production database)

**Machine Learning:**
- scikit-learn 1.8.0 (Random Forest, k-NN)
- pandas, numpy (Data processing)
- joblib (Model persistence)

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design

## ML Models

### Classification
- **Algorithm:** Random Forest
- **Features:** 20 features including demographics, academic performance, lifestyle factors
- **Output:** Stress level (Low/Medium/High) with probability distribution

### Recommendations
- **Algorithm:** k-Nearest Neighbors (k=50)
- **Output:** Top 5 personalized coping mechanisms based on similar users

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/utkarsh9630/mental-stress-assessment.git
cd mental-stress-assessment
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the application
```bash
python app.py
```

6. Open browser to `http://localhost:5000`

## Project Structure
```
mental-stress-assessment/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── forms.py               # WTForms
├── templates/             # HTML templates
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   └── assess.html
├── models/                # ML models
│   ├── rf_model.joblib
│   ├── knn_model.joblib
│   └── *.json
├── data/
│   └── train_recs.csv
├── requirements.txt
├── Procfile
└── README.md
```

## Deployment

Deployed on Render with PostgreSQL database.

### Deploy Your Own

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Screenshots

[Add screenshots of your application here]

## Future Enhancements

- [ ] Email notifications for high stress levels
- [ ] Export assessment history as PDF
- [ ] Mobile app version
- [ ] Integration with wearable devices
- [ ] Multi-language support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Contact

Your Name - Utkarsh Tripathi(mailto:tripathiutkarsh46@gmail.com)

Project Link: [https://github.com/utkarsh9630/mental-stress-assessment]