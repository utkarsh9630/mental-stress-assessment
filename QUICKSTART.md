# Quick Start Guide

## Local Development

### 1. Install Dependencies

```bash
cd stress_app
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The app will start on http://localhost:5000

### 3. Test the Application

Open a new terminal and run:
```bash
python test_app.py
```

Or open your browser and navigate to http://localhost:5000

## Deploy to GitHub

### 1. Create GitHub Repository

Go to github.com and create a new repository named: `mental-stress-assessment`

### 2. Initialize and Push

```bash
cd stress_app
git init
git add .
git commit -m "Initial commit: Mental Stress Assessment System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mental-stress-assessment.git
git push -u origin main
```

## Deploy to Render (Free)

### 1. Sign Up
- Go to https://render.com
- Sign up with GitHub

### 2. Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the repository

### 3. Configure
- Name: `mental-stress-assessment`
- Environment: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Choose Free tier

### 4. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for first deployment
- Access your app at: `https://your-app-name.onrender.com`

## Deploy to Railway (Alternative)

### 1. Sign Up
- Go to https://railway.app
- Sign in with GitHub

### 2. Deploy
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository
- Railway auto-detects and deploys

### 3. Configure
- Go to Settings
- Add start command: `gunicorn app:app`
- Deploy

Your app URL will be shown in the dashboard.

## Verify Deployment

1. Open your deployed URL
2. Fill out the form
3. Click "Analyze Stress Level"
4. Check that predictions and recommendations appear

## Common Issues

### Models not loading
Make sure all .joblib and .json files are committed:
```bash
git add models/*.joblib models/*.json
git commit -m "Add model files"
git push
```

### Out of memory
- Upgrade to paid tier
- Or reduce model size

### Slow first request
- Normal on free tiers
- App goes to sleep after inactivity
- First request wakes it up (takes 30-60 seconds)

## Next Steps

1. Add your own branding
2. Customize the UI colors in templates/index.html
3. Add more coping mechanisms
4. Implement user authentication
5. Add database for storing results

## Support

Check these files for more details:
- README.md - Project overview
- DEPLOYMENT.md - Detailed deployment guide
- app.py - Flask application code
- templates/index.html - Web interface

For issues, check the logs:
- Render: Dashboard → Logs tab
- Railway: Deployment → View logs
- Local: Terminal output
