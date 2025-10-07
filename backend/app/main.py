from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
import logging

# Import our services
from app.services.llm_service import LLMService
from app.services.data_processor import DataProcessor
from app.scrapers.lexicanum_scraper import LexicanumScraper
from app.models.database import get_db, create_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize services
llm_service = LLMService()
data_processor = DataProcessor()
scraper = LexicanumScraper()

# Create database tables
create_tables()

app = FastAPI(
    title="Warhammer 40K Lore Assistant",
    description="An LLM-powered assistant for Warhammer 40K lore questions",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = None

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class ScrapeRequest(BaseModel):
    url: str
    max_pages: Optional[int] = 10

class ProcessedDataResponse(BaseModel):
    message: str
    total_entries: int
    categories: List[str]
    top_terms: List[tuple]

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Warhammer 40K Lore Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Question answering endpoint
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer a question about Warhammer 40K lore using scraped Lexicanum data
    """
    try:
        # Load processed data (in production, this would be from database)
        processed_data = data_processor.load_processed_data("processed_data_latest.json")
        
        if not processed_data:
            # Fallback to basic response if no data available
            return AnswerResponse(
                answer="I don't have access to the Lexicanum data yet. Please run the scraping process first to populate the knowledge base.",
                sources=["https://wh40k.lexicanum.com/wiki/Main_Page"],
                confidence=0.1
            )
        
        # Find relevant context
        context = llm_service.find_relevant_context(request.question, processed_data)
        
        if not context:
            return AnswerResponse(
                answer="I couldn't find relevant information in the knowledge base to answer your question. The knowledge base might need to be updated with more data.",
                sources=["https://wh40k.lexicanum.com/wiki/Main_Page"],
                confidence=0.2
            )
        
        # Generate answer using LLM
        result = llm_service.generate_enhanced_answer(request.question, context)
        
        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Data scraping endpoint
@app.post("/scrape")
async def scrape_lexicanum(request: ScrapeRequest):
    """
    Scrape Lexicanum data for the knowledge base
    """
    try:
        logger.info(f"Starting scrape of {request.url}")
        
        # Scrape the specified URL
        scraped_data = scraper.scrape_page(request.url)
        
        if not scraped_data:
            raise HTTPException(status_code=400, detail="Failed to scrape the specified URL")
        
        # Process the scraped data
        processed_data = data_processor.process_batch([scraped_data])
        
        # Save processed data
        filename = data_processor.save_processed_data(processed_data, "processed_data_latest.json")
        
        # Get statistics
        stats = data_processor.get_processing_statistics(processed_data)
        
        return {
            "message": "Scraping completed successfully",
            "url": request.url,
            "filename": filename,
            "total_entries": stats["total_entries"],
            "categories": list(stats["category_distribution"].keys())
        }
        
    except Exception as e:
        logger.error(f"Error scraping {request.url}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Process existing data endpoint
@app.post("/process-data")
async def process_existing_data():
    """
    Process any existing scraped data
    """
    try:
        # Look for existing scraped data files
        import glob
        data_files = glob.glob("data/lexicanum_data_*.json")
        
        if not data_files:
            return {"message": "No scraped data files found. Please run scraping first."}
        
        # Load the most recent file
        latest_file = max(data_files, key=os.path.getctime)
        raw_data = scraper.load_data(os.path.basename(latest_file))
        
        # Process the data
        processed_data = data_processor.process_batch(raw_data)
        
        # Save processed data
        filename = data_processor.save_processed_data(processed_data, "processed_data_latest.json")
        
        # Get statistics
        stats = data_processor.get_processing_statistics(processed_data)
        
        return {
            "message": "Data processing completed successfully",
            "filename": filename,
            "total_entries": stats["total_entries"],
            "categories": list(stats["category_distribution"].keys()),
            "top_terms": stats["top_terms"][:10]
        }
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Search endpoint
@app.post("/search")
async def search_knowledge_base(request: SearchRequest):
    """
    Search through the knowledge base
    """
    try:
        # Load processed data
        processed_data = data_processor.load_processed_data("processed_data_latest.json")
        
        if not processed_data:
            return {"message": "No processed data available", "results": []}
        
        # Search through the data
        results = data_processor.search_content(processed_data, request.query)
        
        # Limit results
        limited_results = results[:request.limit]
        
        return {
            "query": request.query,
            "total_results": len(results),
            "returned_results": len(limited_results),
            "results": [
                {
                    "title": result["entry"]["title"],
                    "url": result["entry"]["url"],
                    "score": result["score"],
                    "matched_fields": result["matched_fields"],
                    "preview": result["entry"]["content"][:200] + "..."
                }
                for result in limited_results
            ]
        }
        
    except Exception as e:
        logger.error(f"Error searching: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get available topics
@app.get("/topics")
async def get_topics():
    """
    Get list of available topics in the knowledge base
    """
    # TODO: Implement database query
    return {"topics": ["Space Marines", "Chaos", "Eldar", "Orks", "Tau"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
