# 🚀 Complete Deployment Guide

Deploy your Warhammer 40K Lore Assistant to the web with a custom domain!

## 🌐 Domain Options

Choose your perfect domain name:

### GitHub Pages Options:
- `grimdark-scholar.github.io` ⭐ (Recommended)
- `warhammer40k-professor.github.io`
- `wh40k-lore-master.github.io`
- `lexicanum-ai.github.io`
- `warhammer-lore-ai.github.io`

### Custom Domain Options:
- `warhammer40kprofessor.com`
- `wh40k-ai.com`
- `grimdark-scholar.com`

## 📋 Deployment Steps

### Step 1: Prepare Your Repository

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Warhammer 40K Lore Assistant"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/40K_LLM.git
   git push -u origin main
   ```

2. **Update Domain Name (Optional):**
   ```bash
   # Edit the CNAME file to your preferred domain
   echo "your-chosen-name.github.io" > frontend/public/CNAME
   ```

### Step 2: Deploy Backend to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `40K_LLM` repository
   - Set root directory to `backend`

4. **Configure Environment Variables:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./wh40k_lore.db
   API_HOST=0.0.0.0
   API_PORT=$PORT
   ```

5. **Deploy:**
   - Railway will automatically build and deploy
   - Note your backend URL (e.g., `https://your-app.railway.app`)

### Step 3: Configure Frontend

1. **Update API URL:**
   ```bash
   # Edit frontend/.env or set in GitHub Secrets
   REACT_APP_API_URL=https://your-app.railway.app
   ```

2. **Update GitHub Actions:**
   - Edit `.github/workflows/deploy.yml`
   - Replace the API_URL with your Railway URL

### Step 4: Enable GitHub Pages

1. **Go to your repository settings**
2. **Navigate to Pages section**
3. **Set source to "GitHub Actions"**
4. **Push to main branch to trigger deployment**

### Step 5: Test Your Deployment

1. **Backend Test:**
   - Visit `https://your-app.railway.app/health`
   - Should return `{"status": "healthy"}`

2. **Frontend Test:**
   - Visit `https://grimdark-scholar.github.io`
   - Try asking a question about Warhammer 40K!

## 🎨 Custom Domain Setup (Optional)

### Option 1: GitHub Pages Custom Domain

1. **Buy a domain** (e.g., `warhammer40kprofessor.com`)
2. **Update CNAME:**
   ```bash
   echo "warhammer40kprofessor.com" > frontend/public/CNAME
   ```
3. **Configure DNS:**
   - Add CNAME record: `www` → `grimdark-scholar.github.io`
   - Add A record: `@` → `185.199.108.153` (GitHub Pages IP)

### Option 2: Vercel Deployment

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend:**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Configure Custom Domain:**
   - Go to Vercel dashboard
   - Add your custom domain
   - Update DNS settings

## 🔧 Advanced Configuration

### Environment Variables

**Backend (Railway):**
```
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./wh40k_lore.db
API_HOST=0.0.0.0
API_PORT=$PORT
```

**Frontend (GitHub Secrets):**
```
REACT_APP_API_URL=https://your-backend.railway.app
```

### CORS Configuration

Update `backend/app/main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://grimdark-scholar.github.io",
        "https://your-custom-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring & Analytics

### Railway Monitoring
- View logs in Railway dashboard
- Monitor resource usage
- Set up alerts for errors

### GitHub Pages Analytics
- Enable GitHub Pages analytics
- Monitor page views and performance

### Custom Analytics
- Add Google Analytics to frontend
- Track user interactions
- Monitor API usage

## 💰 Cost Breakdown

### Free Tier (Recommended)
- **Railway**: 500 hours/month free
- **GitHub Pages**: Free for public repos
- **OpenAI API**: ~$5-20/month (depending on usage)

### Paid Options
- **Railway Pro**: $5/month for unlimited hours
- **Custom Domain**: $10-15/year
- **Premium Analytics**: $10-20/month

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Update CORS settings in backend
   - Check API URL configuration

2. **Build Failures:**
   - Check GitHub Actions logs
   - Verify environment variables

3. **API Connection Issues:**
   - Test backend health endpoint
   - Check Railway logs

4. **Domain Issues:**
   - Verify DNS settings
   - Check CNAME file

### Debug Commands

```bash
# Test backend locally
curl https://your-backend.railway.app/health

# Test frontend build
cd frontend && npm run build

# Check deployment status
gh api repos/:owner/:repo/pages
```

## 🎯 Portfolio Benefits

Your deployed project will showcase:

- **Live Demo**: `https://warhammer40k-professor.github.io`
- **Professional Domain**: Custom branding
- **Full-Stack Skills**: Frontend + Backend + AI
- **DevOps Knowledge**: CI/CD, deployment, monitoring
- **Real-World Application**: Solving actual problems

## 🚀 Next Steps

1. **Deploy the application** using this guide
2. **Add to your portfolio** with live links
3. **Share on social media** to get feedback
4. **Iterate and improve** based on user feedback
5. **Add more features** like user accounts, favorites, etc.

Your Warhammer 40K Lore Assistant will be live on the web and ready to impress potential employers! 🎉
