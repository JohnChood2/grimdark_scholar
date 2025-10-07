import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin, urlparse
import re
import json
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class LexicanumScraper:
    """
    Web scraper for Warhammer 40K Lexicanum wiki
    """
    
    def __init__(self, base_url: str = "https://wh40k.lexicanum.com", delay: float = 1.0, data_dir: str = "data"):
        self.base_url = base_url
        self.delay = delay
        self.data_dir = data_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.scraped_data: List[Dict] = []
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
    def scrape_page(self, url: str) -> Dict:
        """
        Scrape a single page from Lexicanum
        """
        try:
            if url in self.visited_urls:
                return None
                
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract page data
            page_data = {
                'url': url,
                'title': self._extract_title(soup),
                'content': self._extract_content(soup),
                'categories': self._extract_categories(soup),
                'links': self._extract_internal_links(soup),
                'images': self._extract_images(soup),
                'scraped_at': datetime.now().isoformat(),
                'word_count': len(self._extract_content(soup).split()),
                'has_infobox': self._extract_infobox(soup) is not None,
                'infobox_data': self._extract_infobox(soup)
            }
            
            self.visited_urls.add(url)
            time.sleep(self.delay)  # Be respectful to the server
            
            return page_data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_elem = soup.find('h1', {'class': 'firstHeading'})
        if title_elem:
            return title_elem.get_text().strip()
        return "Unknown Title"
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page"""
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            return ""
        
        # Remove unwanted elements
        for element in content_div.find_all(['script', 'style', 'nav', 'aside']):
            element.decompose()
        
        # Extract text content
        content = content_div.get_text(separator='\n', strip=True)
        return content
    
    def _extract_categories(self, soup: BeautifulSoup) -> List[str]:
        """Extract page categories"""
        categories = []
        cat_links = soup.find_all('a', href=re.compile(r'/wiki/Category:'))
        for link in cat_links:
            category = link.get_text().strip()
            if category:
                categories.append(category)
        return categories
    
    def _extract_internal_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract internal links to other Lexicanum pages"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/') and ':' not in href:
                full_url = urljoin(self.base_url, href)
                links.append(full_url)
        return list(set(links))  # Remove duplicates
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract image URLs from the page"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin(self.base_url, src)
                images.append(src)
        return images
    
    def _extract_infobox(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract infobox data if present"""
        infobox = soup.find('table', {'class': 'infobox'})
        if not infobox:
            return None
        
        infobox_data = {}
        for row in infobox.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            if len(cells) == 2:
                key = cells[0].get_text().strip()
                value = cells[1].get_text().strip()
                infobox_data[key] = value
        
        return infobox_data if infobox_data else None
    
    def save_data(self, filename: str = None) -> str:
        """Save scraped data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lexicanum_data_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(self.scraped_data)} entries to {filepath}")
        return filepath
    
    def load_data(self, filename: str) -> List[Dict]:
        """Load previously scraped data from JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"File {filepath} does not exist")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} entries from {filepath}")
        return data
    
    def get_statistics(self) -> Dict:
        """Get statistics about scraped data"""
        if not self.scraped_data:
            return {"total_entries": 0}
        
        total_entries = len(self.scraped_data)
        total_words = sum(entry.get('word_count', 0) for entry in self.scraped_data)
        categories = set()
        for entry in self.scraped_data:
            categories.update(entry.get('categories', []))
        
        return {
            "total_entries": total_entries,
            "total_words": total_words,
            "unique_categories": len(categories),
            "categories": list(categories),
            "avg_words_per_entry": total_words / total_entries if total_entries > 0 else 0
        }
    
    def scrape_category(self, category_url: str, max_pages: int = 50) -> List[Dict]:
        """
        Scrape all pages in a category
        """
        try:
            response = self.session.get(category_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all page links in the category
            page_links = []
            for link in soup.find_all('a', href=re.compile(r'/wiki/[^:]+$')):
                href = link['href']
                if href.startswith('/wiki/'):
                    full_url = urljoin(self.base_url, href)
                    page_links.append(full_url)
            
            # Scrape pages (limit to max_pages)
            scraped_pages = []
            for i, page_url in enumerate(page_links[:max_pages]):
                if i >= max_pages:
                    break
                    
                page_data = self.scrape_page(page_url)
                if page_data:
                    scraped_pages.append(page_data)
                    
                logger.info(f"Progress: {i+1}/{min(len(page_links), max_pages)}")
            
            return scraped_pages
            
        except Exception as e:
            logger.error(f"Error scraping category {category_url}: {str(e)}")
            return []
    
    def scrape_main_categories(self, max_pages_per_category: int = 20) -> Dict[str, List[Dict]]:
        """
        Scrape main Warhammer 40K categories
        """
        main_categories = {
            'Space Marines': '/wiki/Category:Space_Marines',
            'Chaos': '/wiki/Category:Chaos',
            'Eldar': '/wiki/Category:Eldar',
            'Orks': '/wiki/Category:Orks',
            'Tau': '/wiki/Category:Tau',
            'Imperial Guard': '/wiki/Category:Imperial_Guard',
            'Adeptus Mechanicus': '/wiki/Category:Adeptus_Mechanicus',
            'Inquisition': '/wiki/Category:Inquisition'
        }
        
        all_data = {}
        
        for category_name, category_path in main_categories.items():
            logger.info(f"Scraping category: {category_name}")
            category_url = urljoin(self.base_url, category_path)
            category_data = self.scrape_category(category_url, max_pages_per_category)
            all_data[category_name] = category_data
            
        return all_data

# Example usage
if __name__ == "__main__":
    scraper = LexicanumScraper()
    
    # Scrape a single page
    page_data = scraper.scrape_page("https://wh40k.lexicanum.com/wiki/Space_Marines")
    print(f"Scraped page: {page_data['title'] if page_data else 'Failed'}")
    
    # Scrape main categories
    # all_data = scraper.scrape_main_categories(max_pages_per_category=5)
    # print(f"Scraped {len(all_data)} categories")
