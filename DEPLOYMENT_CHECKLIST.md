# Deployment Checklist

## Pre-Deployment

- [ ] Extract stress_app_complete.zip
- [ ] Navigate to stress_app directory
- [ ] Verify all model files are present in models/ folder
- [ ] Verify train_recs.csv is present in data/ folder

## Local Testing

- [ ] Install Python 3.11 (or 3.8+)
- [ ] Run: pip install -r requirements.txt
- [ ] Run: python app.py
- [ ] Open browser to http://localhost:5000
- [ ] Test form submission
- [ ] Verify predictions appear
- [ ] Run: python test_app.py
- [ ] Confirm all tests pass

## Git Setup

- [ ] Create GitHub account (if needed)
- [ ] Create new repository: mental-stress-assessment
- [ ] Run: git init
- [ ] Run: git add .
- [ ] Run: git commit -m "Initial commit"
- [ ] Run: git remote add origin YOUR_REPO_URL
- [ ] Run: git push -u origin main
- [ ] Verify files uploaded on GitHub

## Deploy to Render

- [ ] Go to render.com
- [ ] Sign up with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub account
- [ ] Select mental-stress-assessment repository
- [ ] Name: mental-stress-assessment
- [ ] Environment: Python 3
- [ ] Build Command: pip install -r requirements.txt
- [ ] Start Command: gunicorn app:app
- [ ] Select Free tier
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Click on the URL provided
- [ ] Test the live application

## Post-Deployment Testing

- [ ] Open deployed URL
- [ ] Test with different input values
- [ ] Verify all stress levels predict correctly
- [ ] Verify recommendations appear
- [ ] Test on mobile device
- [ ] Test on different browsers
- [ ] Check application logs for errors

## Optional Enhancements

- [ ] Add custom domain
- [ ] Set up monitoring
- [ ] Enable analytics
- [ ] Add user feedback form
- [ ] Implement rate limiting
- [ ] Add API documentation
- [ ] Create backup strategy

## Documentation

- [ ] Update README with deployed URL
- [ ] Add screenshots to repository
- [ ] Document any issues encountered
- [ ] Create user guide
- [ ] Update contact information

## Sharing

- [ ] Share deployed URL with users
- [ ] Create demo video
- [ ] Write blog post about project
- [ ] Add to portfolio
- [ ] Share on LinkedIn

## Maintenance

- [ ] Monitor application logs weekly
- [ ] Check for security updates
- [ ] Update dependencies monthly
- [ ] Retrain models with new data (if available)
- [ ] Gather user feedback
- [ ] Plan feature updates

## Troubleshooting Guide

If deployment fails:
1. Check logs in platform dashboard
2. Verify all files are committed
3. Check Python version matches runtime.txt
4. Ensure requirements.txt has all dependencies
5. Verify model files are not corrupted
6. Check file size limits

If prediction fails:
1. Check input validation
2. Verify model files loaded correctly
3. Check feature names match
4. Review application logs
5. Test locally first

If slow performance:
1. Normal for first request on free tier
2. Consider upgrading to paid tier
3. Implement caching
4. Optimize model loading

## Success Criteria

Application is successfully deployed when:
- [ ] URL is accessible from any browser
- [ ] Form accepts input without errors
- [ ] Predictions return within 5 seconds
- [ ] Recommendations are displayed
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Health endpoint returns 200

## Notes

- Free tier may sleep after 15 min inactivity
- First request after sleep takes 30-60 seconds
- Models total ~67MB (well under limits)
- Application uses ~512MB RAM
- Cold start time: 5-10 seconds
- Warm response time: <500ms

## Support Resources

- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
- scikit-learn Documentation: https://scikit-learn.org/
- Project README.md
- Project DEPLOYMENT.md
- GitHub Issues page

## Completion

Date deployed: _____________
Deployed URL: _____________
Status: _____________
Notes: _____________
