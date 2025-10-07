#!/usr/bin/env python3
"""
Initial data collection script for Warhammer 40K Lexicanum
This script scrapes key pages to populate the knowledge base
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.scrapers.lexicanum_scraper import LexicanumScraper
from app.services.data_processor import DataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Key pages to scrape for initial data collection
KEY_PAGES = [
    "https://wh40k.lexicanum.com/wiki/Space_Marines",
    "https://wh40k.lexicanum.com/wiki/Chaos_Space_Marines", 
    "https://wh40k.lexicanum.com/wiki/Eldar",
    "https://wh40k.lexicanum.com/wiki/Orks",
    "https://wh40k.lexicanum.com/wiki/Tau_Empire",
    "https://wh40k.lexicanum.com/wiki/Imperial_Guard",
    "https://wh40k.lexicanum.com/wiki/Adeptus_Mechanicus",
    "https://wh40k.lexicanum.com/wiki/Inquisition",
    "https://wh40k.lexicanum.com/wiki/Emperor_of_Mankind",
    "https://wh40k.lexicanum.com/wiki/Horus_Heresy",
    "https://wh40k.lexicanum.com/wiki/Primarch",
    "https://wh40k.lexicanum.com/wiki/Warp",
    "https://wh40k.lexicanum.com/wiki/Psyker",
    "https://wh40k.lexicanum.com/wiki/Astartes",
    "https://wh40k.lexicanum.com/wiki/Chapter",
    "https://wh40k.lexicanum.com/wiki/Legion",
    "https://wh40k.lexicanum.com/wiki/Titan",
    "https://wh40k.lexicanum.com/wiki/Knight",
    "https://wh40k.lexicanum.com/wiki/Dreadnought",
    "https://wh40k.lexicanum.com/wiki/Terminator_Armour"
]

async def collect_initial_data():
    """Collect initial data from key Lexicanum pages"""
    
    logger.info("Starting initial data collection...")
    
    # Initialize services
    scraper = LexicanumScraper(delay=2.0)  # 2 second delay to be respectful
    processor = DataProcessor()
    
    scraped_entries = []
    
    # Scrape each key page
    for i, url in enumerate(KEY_PAGES, 1):
        logger.info(f"Scraping {i}/{len(KEY_PAGES)}: {url}")
        
        try:
            page_data = scraper.scrape_page(url)
            if page_data:
                scraped_entries.append(page_data)
                logger.info(f"✓ Successfully scraped: {page_data['title']}")
            else:
                logger.warning(f"✗ Failed to scrape: {url}")
                
        except Exception as e:
            logger.error(f"✗ Error scraping {url}: {str(e)}")
            continue
    
    if not scraped_entries:
        logger.error("No data was successfully scraped!")
        return False
    
    # Save raw scraped data
    raw_filename = scraper.save_data("initial_collection_raw.json")
    logger.info(f"Saved {len(scraped_entries)} raw entries to {raw_filename}")
    
    # Process the data
    logger.info("Processing scraped data...")
    processed_entries = processor.process_batch(scraped_entries)
    
    # Save processed data
    processed_filename = processor.save_processed_data(processed_entries, "processed_data_latest.json")
    logger.info(f"Saved {len(processed_entries)} processed entries to {processed_filename}")
    
    # Get and display statistics
    stats = processor.get_processing_statistics(processed_entries)
    
    logger.info("=== Data Collection Complete ===")
    logger.info(f"Total entries: {stats['total_entries']}")
    logger.info(f"Total content length: {stats['total_content_length']:,} characters")
    logger.info(f"Average content length: {stats['avg_content_length']:.0f} characters")
    logger.info(f"Categories found: {list(stats['category_distribution'].keys())}")
    logger.info(f"Top terms: {[term[0] for term in stats['top_terms'][:5]]}")
    
    return True

def main():
    """Main function"""
    try:
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Run the data collection
        success = asyncio.run(collect_initial_data())
        
        if success:
            print("\n🎉 Initial data collection completed successfully!")
            print("You can now start the API server and test the question answering functionality.")
            print("\nTo start the server:")
            print("cd backend && uvicorn app.main:app --reload")
        else:
            print("\n❌ Data collection failed. Please check the logs for errors.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Data collection interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
