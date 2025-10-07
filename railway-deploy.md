# Railway Backend Deployment Guide

This guide will help you deploy the backend API to Railway for free hosting.

## Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Connect your repository

## Step 2: Deploy Backend

1. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `40K_LLM` repository

2. **Configure Service:**
   - Select the `backend` folder as the root directory
   - Railway will automatically detect it's a Python project

3. **Set Environment Variables:**
   - Go to your project settings
   - Add these environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./wh40k_lore.db
   API_HOST=0.0.0.0
   API_PORT=$PORT
   ```

4. **Deploy:**
   - Railway will automatically build and deploy
   - You'll get a URL like: `https://your-app-name.railway.app`

## Step 3: Update Frontend Configuration

1. **Update the API URL in your frontend:**
   ```bash
   # In your .env file or GitHub Secrets
   REACT_APP_API_URL=https://your-app-name.railway.app
   ```

2. **Update the GitHub Actions workflow:**
   - Edit `.github/workflows/deploy.yml`
   - Replace `https://your-backend-url.railway.app` with your actual Railway URL

## Step 4: Test the Deployment

1. **Test the backend:**
   - Visit `https://your-app-name.railway.app/health`
   - Should return `{"status": "healthy"}`

2. **Test the frontend:**
   - After GitHub Pages deployment
   - Visit `https://warhammer40k-professor.github.io`
   - Try asking a question

## Step 5: Custom Domain (Optional)

If you want a custom domain instead of GitHub Pages:

1. **Buy a domain** (e.g., `warhammer40kprofessor.com`)
2. **Update CNAME file:**
   ```bash
   echo "your-custom-domain.com" > frontend/public/CNAME
   ```
3. **Configure DNS:**
   - Point your domain to GitHub Pages
   - Add CNAME record: `www` → `warhammer40k-professor.github.io`

## Troubleshooting

### Backend Issues
- Check Railway logs in the dashboard
- Ensure all environment variables are set
- Verify the `requirements.txt` is in the backend folder

### Frontend Issues
- Check GitHub Actions logs
- Ensure `REACT_APP_API_URL` is set correctly
- Verify the build completes successfully

### CORS Issues
- The backend is configured to allow all origins in development
- For production, update the CORS settings in `backend/app/main.py`

## Cost Considerations

- **Railway**: Free tier includes 500 hours/month
- **GitHub Pages**: Free for public repositories
- **OpenAI API**: Pay-per-use (very affordable for this project)

## Security Notes

- Never commit API keys to the repository
- Use GitHub Secrets for sensitive data
- Consider rate limiting for production use
