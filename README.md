<<<<<<< HEAD
# Warhammer 40K Lore Assistant

A Large Language Model-powered assistant that answers questions about Warhammer 40K lore using data from the Lexicanum wiki.

## Features

- 🔍 Web scraping of Warhammer 40K Lexicanum data
- 🤖 LLM-powered question answering
- 🌐 Web interface for easy interaction
- 📚 Comprehensive lore database
- 🚀 Deployed and accessible online

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React with TypeScript
- **Database**: SQLite/PostgreSQL for data storage
- **LLM**: OpenAI GPT-4 or Anthropic Claude
- **Deployment**: Docker + Railway/Vercel
- **Web Scraping**: BeautifulSoup4 + requests

## Project Structure

```
40K_LLM/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app
│   │   ├── models/         # Database models
│   │   ├── scrapers/       # Web scraping modules
│   │   ├── services/       # LLM integration
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── Dockerfile
├── data/                   # Scraped data storage
├── docs/                   # Documentation
├── docker-compose.yml      # Local development
└── README.md
```

## Getting Started

### Quick Setup (Recommended)

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Edit your environment file:**
   ```bash
   # Edit .env file and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start the application:**
   ```bash
   # Option 1: Docker Compose (Recommended)
   docker-compose up --build
   
   # Option 2: Manual setup
   # Terminal 1 - Backend
   cd backend && uvicorn app.main:app --reload
   
   # Terminal 2 - Frontend  
   cd frontend && npm start
   ```

4. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🌐 Deploy to the Web

### Quick Deployment

1. **Run the deployment script:**
   ```bash
   ./scripts/deploy.sh
   ```

2. **Follow the instructions** to deploy to GitHub Pages

3. **Your site will be live at:**
   - `https://grimdark-scholar.github.io` (or your chosen domain)

### Manual Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🎯 Portfolio Ready

Your project will be live on the web with:
- **Custom domain**: `grimdark-scholar.github.io`
- **Professional hosting**: GitHub Pages + Railway
- **Live demo**: Ready to share with employers
- **Source code**: Available on GitHub

### Manual Setup

#### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key
- Docker (optional)

#### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd 40K_LLM
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Run initial data collection (optional):**
   ```bash
   cd ..
   python scripts/initial_data_collection.py
   ```

6. **Start the servers:**
   ```bash
   # Backend (Terminal 1)
   cd backend && uvicorn app.main:app --reload
   
   # Frontend (Terminal 2)
   cd frontend && npm start
   ```

## Development Roadmap

- [x] Project setup and structure
- [x] Web scraping implementation
- [x] Data processing and storage
- [x] LLM integration
- [x] Web interface development
- [x] Basic deployment setup
- [x] Documentation and testing

## API Endpoints

### Core Endpoints
- `POST /ask` - Ask a question about Warhammer 40K lore
- `GET /topics` - Get available topics
- `GET /health` - Health check

### Data Management
- `POST /scrape` - Scrape a specific Lexicanum page
- `POST /process-data` - Process existing scraped data
- `POST /search` - Search the knowledge base

## Features Implemented

### ✅ Backend (FastAPI)
- RESTful API with comprehensive endpoints
- Web scraping with BeautifulSoup4
- LLM integration with OpenAI GPT-4
- Data processing and storage
- Database models with SQLAlchemy
- Docker containerization

### ✅ Frontend (React + TypeScript)
- Modern, responsive UI with Warhammer 40K theming
- Question form with example questions
- Answer display with confidence indicators
- Topic browser for exploring categories
- API integration service
- Styled components with dark theme

### ✅ Infrastructure
- Docker Compose for local development
- Environment configuration
- Database schema with SQLAlchemy
- Comprehensive documentation
- Setup automation scripts

## Contributing

This project is open source and contributions are welcome!

## License

MIT License - see LICENSE file for details
=======
# grimdark_scholar
Warhammer 40K Lore Assistant - Grimdark Scholar
>>>>>>> 5fcab5862d3a5abbdfcaafedaad6c722d2ecc78e
