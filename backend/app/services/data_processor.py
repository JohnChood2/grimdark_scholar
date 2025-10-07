import json
import re
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Process and clean scraped Lexicanum data
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common wiki artifacts
        text = re.sub(r'\[edit\]', '', text)
        text = re.sub(r'\[citation needed\]', '', text)
        text = re.sub(r'\[1\]|\[2\]|\[3\]|\[4\]|\[5\]', '', text)
        
        # Remove references like [1], [2], etc.
        text = re.sub(r'\[\d+\]', '', text)
        
        # Clean up multiple spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def extract_key_terms(self, content: str) -> List[str]:
        """Extract key terms and concepts from content"""
        # Common Warhammer 40K terms to look for
        key_terms = [
            'Space Marine', 'Chaos', 'Eldar', 'Ork', 'Tau', 'Imperial Guard',
            'Adeptus Astartes', 'Adeptus Mechanicus', 'Inquisition', 'Emperor',
            'Horus Heresy', 'Primarch', 'Chapter', 'Legion', 'Warp', 'Psyker',
            'Bolter', 'Chainsword', 'Power Armour', 'Terminator', 'Dreadnought',
            'Titan', 'Knight', 'Baneblade', 'Leman Russ', 'Rhino', 'Land Raider'
        ]
        
        found_terms = []
        content_lower = content.lower()
        
        for term in key_terms:
            if term.lower() in content_lower:
                found_terms.append(term)
        
        return found_terms
    
    def categorize_content(self, title: str, content: str, categories: List[str]) -> str:
        """Determine the main category for content"""
        # Priority order for categorization
        category_keywords = {
            'Space Marines': ['space marine', 'adeptus astartes', 'chapter', 'primarch'],
            'Chaos': ['chaos', 'daemon', 'warp', 'heretic', 'chaos space marine'],
            'Eldar': ['eldar', 'aeldari', 'craftworld', 'aspect warrior'],
            'Orks': ['ork', 'orkz', 'warboss', 'gretchin', 'squig'],
            'Tau': ['tau', 'tau empire', 'fire caste', 'ethereal'],
            'Imperial Guard': ['imperial guard', 'astra militarum', 'regiment', 'commissar'],
            'Adeptus Mechanicus': ['adeptus mechanicus', 'tech-priest', 'machine spirit', 'forge world'],
            'Inquisition': ['inquisition', 'inquisitor', 'grey knight', 'daemonhunter']
        }
        
        # Check categories first
        for cat in categories:
            for main_cat, keywords in category_keywords.items():
                if any(keyword in cat.lower() for keyword in keywords):
                    return main_cat
        
        # Check content for keywords
        content_lower = content.lower()
        title_lower = title.lower()
        
        for main_cat, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in content_lower or keyword in title_lower:
                    return main_cat
        
        return 'General'
    
    def process_entry(self, entry: Dict) -> Dict:
        """Process a single scraped entry"""
        processed = entry.copy()
        
        # Clean content
        processed['content'] = self.clean_text(entry.get('content', ''))
        processed['title'] = self.clean_text(entry.get('title', ''))
        
        # Extract key terms
        processed['key_terms'] = self.extract_key_terms(processed['content'])
        
        # Categorize content
        processed['main_category'] = self.categorize_content(
            processed['title'],
            processed['content'],
            entry.get('categories', [])
        )
        
        # Add processing metadata
        processed['processed_at'] = datetime.now().isoformat()
        processed['content_length'] = len(processed['content'])
        processed['has_infobox'] = bool(entry.get('infobox_data'))
        
        return processed
    
    def process_batch(self, entries: List[Dict]) -> List[Dict]:
        """Process a batch of entries"""
        processed_entries = []
        
        for entry in entries:
            try:
                processed = self.process_entry(entry)
                processed_entries.append(processed)
            except Exception as e:
                logger.error(f"Error processing entry {entry.get('url', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Processed {len(processed_entries)} out of {len(entries)} entries")
        return processed_entries
    
    def save_processed_data(self, processed_entries: List[Dict], filename: str = None) -> str:
        """Save processed data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"processed_data_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(processed_entries, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(processed_entries)} processed entries to {filepath}")
        return filepath
    
    def load_processed_data(self, filename: str) -> List[Dict]:
        """Load processed data from JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"File {filepath} does not exist")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} processed entries from {filepath}")
        return data
    
    def get_processing_statistics(self, processed_entries: List[Dict]) -> Dict:
        """Get statistics about processed data"""
        if not processed_entries:
            return {"total_entries": 0}
        
        total_entries = len(processed_entries)
        total_content_length = sum(entry.get('content_length', 0) for entry in processed_entries)
        
        # Category distribution
        categories = {}
        for entry in processed_entries:
            cat = entry.get('main_category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        # Key terms frequency
        all_key_terms = []
        for entry in processed_entries:
            all_key_terms.extend(entry.get('key_terms', []))
        
        term_frequency = {}
        for term in all_key_terms:
            term_frequency[term] = term_frequency.get(term, 0) + 1
        
        # Top terms
        top_terms = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_entries": total_entries,
            "total_content_length": total_content_length,
            "avg_content_length": total_content_length / total_entries if total_entries > 0 else 0,
            "category_distribution": categories,
            "top_terms": top_terms,
            "entries_with_infobox": sum(1 for entry in processed_entries if entry.get('has_infobox', False))
        }
    
    def search_content(self, processed_entries: List[Dict], query: str) -> List[Dict]:
        """Search through processed entries"""
        query_lower = query.lower()
        results = []
        
        for entry in processed_entries:
            score = 0
            
            # Title match (higher weight)
            if query_lower in entry.get('title', '').lower():
                score += 10
            
            # Content match
            if query_lower in entry.get('content', '').lower():
                score += 5
            
            # Key terms match
            for term in entry.get('key_terms', []):
                if query_lower in term.lower():
                    score += 3
            
            # Category match
            if query_lower in entry.get('main_category', '').lower():
                score += 2
            
            if score > 0:
                results.append({
                    'entry': entry,
                    'score': score,
                    'matched_fields': self._get_matched_fields(entry, query_lower)
                })
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def _get_matched_fields(self, entry: Dict, query: str) -> List[str]:
        """Get list of fields that matched the query"""
        matched = []
        
        if query in entry.get('title', '').lower():
            matched.append('title')
        if query in entry.get('content', '').lower():
            matched.append('content')
        if query in entry.get('main_category', '').lower():
            matched.append('category')
        
        return matched

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    
    # Example of processing data
    sample_entry = {
        'url': 'https://wh40k.lexicanum.com/wiki/Space_Marines',
        'title': 'Space Marines',
        'content': 'The Space Marines are the elite warriors of the Imperium...',
        'categories': ['Space Marines', 'Adeptus Astartes']
    }
    
    processed = processor.process_entry(sample_entry)
    print(f"Processed entry: {processed['title']}")
    print(f"Main category: {processed['main_category']}")
    print(f"Key terms: {processed['key_terms']}")
