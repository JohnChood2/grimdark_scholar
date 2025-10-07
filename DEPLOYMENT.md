# Deployment Guide

This guide covers how to deploy your Warhammer 40K Lore Assistant to various platforms.

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker (optional)

### Setup
1. Clone the repository
2. Copy `env.example` to `.env` and configure your API keys
3. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```
4. Run the development servers:
   ```bash
   # Backend (Terminal 1)
   cd backend
   uvicorn app.main:app --reload
   
   # Frontend (Terminal 2)
   cd frontend
   npm start
   ```

### Using Docker
```bash
docker-compose up --build
```

## Production Deployment

### Option 1: Railway (Recommended)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Backend**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway init
   railway up
   ```

3. **Configure Environment Variables**
   - Add `OPENAI_API_KEY` in Railway dashboard
   - Set `DATABASE_URL` for production database

4. **Deploy Frontend**
   - Connect your GitHub repository
   - Set build command: `npm run build`
   - Set start command: `npm start`

### Option 2: Vercel + Railway

1. **Deploy Backend to Railway** (as above)
2. **Deploy Frontend to Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   cd frontend
   vercel
   ```

### Option 3: DigitalOcean App Platform

1. **Create App Spec**
   ```yaml
   name: wh40k-lore-assistant
   services:
   - name: backend
     source_dir: /backend
     github:
       repo: your-username/40K_LLM
       branch: main
     run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: OPENAI_API_KEY
       value: your_api_key
   
   - name: frontend
     source_dir: /frontend
     github:
       repo: your-username/40K_LLM
       branch: main
     run_command: npm start
     environment_slug: node-js
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: REACT_APP_API_URL
       value: https://your-backend-url.com
   ```

### Option 4: AWS/GCP/Azure

For cloud providers, you can use:
- **AWS**: Elastic Beanstalk or ECS
- **GCP**: Cloud Run or App Engine
- **Azure**: Container Instances or App Service

## Database Setup

### SQLite (Development)
No setup required - automatically created.

### PostgreSQL (Production)
```bash
# Create database
createdb wh40k_lore

# Run migrations
cd backend
alembic upgrade head
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Database connection string

### Optional
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `REACT_APP_API_URL`: Frontend API URL
- `SCRAPING_DELAY`: Delay between scrapes (default: 1.0)
- `MAX_PAGES_PER_CATEGORY`: Max pages to scrape (default: 50)

## Monitoring and Maintenance

### Health Checks
- Backend: `GET /health`
- Frontend: Built-in React health checks

### Logs
- Backend: Check application logs
- Frontend: Browser console and network tab

### Database Maintenance
```bash
# Backup database
pg_dump wh40k_lore > backup.sql

# Restore database
psql wh40k_lore < backup.sql
```

## Scaling Considerations

### Performance
- Use Redis for caching
- Implement database connection pooling
- Add CDN for static assets

### Cost Optimization
- Use serverless functions for LLM calls
- Implement request rate limiting
- Cache frequently asked questions

## Security

### API Security
- Implement API key authentication
- Add rate limiting
- Use HTTPS in production
- Validate all inputs

### Data Protection
- Encrypt sensitive data
- Implement proper access controls
- Regular security audits

## Troubleshooting

### Common Issues
1. **CORS errors**: Check frontend API URL configuration
2. **Database connection**: Verify DATABASE_URL format
3. **API key issues**: Ensure OPENAI_API_KEY is set correctly
4. **Memory issues**: Increase container memory limits

### Debug Mode
```bash
# Backend
DEBUG=1 uvicorn app.main:app --reload

# Frontend
REACT_APP_DEBUG=true npm start
```
