# Deployment Guide

## Step 1: Prepare Repository

1. Initialize Git repository (if not already done):
```bash
cd stress_app
git init
git add .
git commit -m "Initial commit"
```

2. Create GitHub repository:
   - Go to github.com and create a new repository
   - Name it: mental-stress-assessment
   - Don't initialize with README (we already have one)

3. Push to GitHub:
```bash
git remote add origin https://github.com/YOUR_USERNAME/mental-stress-assessment.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Render (Recommended)

### Why Render?
- Free tier available
- Easy deployment
- Good for ML applications with large model files
- Automatic HTTPS

### Steps:

1. Go to [render.com](https://render.com) and sign up

2. Click "New +" and select "Web Service"

3. Connect your GitHub account and select your repository

4. Configure:
   - Name: mental-stress-assessment
   - Region: Choose closest to you
   - Branch: main
   - Root Directory: (leave blank)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

5. Choose Free tier

6. Click "Create Web Service"

7. Wait for deployment (first deploy takes 5-10 minutes due to large model files)

8. Your app will be live at: `https://your-app-name.onrender.com`

### Important Notes for Render:
- Free tier may sleep after inactivity (wakes up on first request)
- Total slug size should be under 500MB (your models are ~67MB, so you're fine)

## Step 3: Alternative - Deploy to Railway

### Steps:

1. Go to [railway.app](https://railway.app)

2. Sign in with GitHub

3. Click "New Project" → "Deploy from GitHub repo"

4. Select your repository

5. Railway auto-detects Python and installs dependencies

6. Add start command in Settings:
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

7. Click "Deploy"

8. Get your URL from the deployment page

### Railway Advantages:
- Very fast deployments
- Good free tier
- Automatic deployments on git push

## Step 4: Alternative - Deploy to Heroku

### Prerequisites:
- Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

### Steps:

1. Login to Heroku:
```bash
heroku login
```

2. Create app:
```bash
heroku create mental-stress-assessment
```

3. Deploy:
```bash
git push heroku main
```

4. Open app:
```bash
heroku open
```

### Heroku Notes:
- Free tier discontinued in November 2022
- Now requires paid plan ($7/month minimum)
- Good for production applications

## Step 5: Test Deployment

1. Navigate to your deployed URL

2. Fill out the form with test data

3. Click "Analyze Stress Level"

4. Verify predictions and recommendations appear

## Troubleshooting

### Issue: Application won't start

Check logs:
- Render: Click on "Logs" tab
- Railway: Click on deployment and view logs
- Heroku: `heroku logs --tail`

Common fixes:
- Ensure all dependencies in requirements.txt
- Check Python version matches runtime.txt
- Verify model files are committed and pushed

### Issue: 413 Request Entity Too Large

Your model files may be too large. Solutions:
1. Use Git LFS for large files
2. Store models in cloud storage (S3, GCS) and download on startup

### Issue: Out of Memory

Your application uses too much RAM:
1. Upgrade to paid tier with more memory
2. Reduce model size (feature selection, model compression)

### Issue: Slow Loading

Model loading takes time:
1. This is normal on free tiers
2. Consider model caching strategies
3. Use paid tier with more resources

## Environment Variables (if needed)

Set environment variables for production:

Render:
- Go to Environment section
- Add variables as needed

Railway:
- Go to Variables tab
- Add variables

Heroku:
```bash
heroku config:set VARIABLE_NAME=value
```

## Custom Domain (Optional)

### Render:
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

### Railway:
1. Go to Settings → Domains
2. Add custom domain
3. Configure DNS

## Monitoring

### Render:
- View logs in dashboard
- Set up health check: `/health` endpoint

### Railway:
- Built-in metrics
- View logs in dashboard

### Heroku:
```bash
heroku logs --tail
```

## Backup Strategy

1. Keep models in Git repository (with LFS if large)
2. Export training data separately
3. Document model training process
4. Version your models

## Next Steps

1. Add user authentication
2. Store user history in database
3. Add analytics tracking
4. Create mobile responsive design improvements
5. Add more coping mechanisms
6. Implement A/B testing for recommendations

## Support

If you encounter issues:
1. Check platform documentation
2. Review application logs
3. Test locally first
4. Check model file sizes and compatibility
