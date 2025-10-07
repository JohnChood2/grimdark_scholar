import openai
import os
from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for integrating with Large Language Models
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        else:
            logger.warning("No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
    
    def generate_answer(self, question: str, context: str, model: str = "gpt-4") -> Dict:
        """
        Generate an answer to a question using provided context
        """
        try:
            if not self.api_key:
                return {
                    "answer": "LLM service not configured. Please set OPENAI_API_KEY environment variable.",
                    "confidence": 0.0,
                    "sources": []
                }
            
            prompt = self._build_prompt(question, context)
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable assistant about Warhammer 40K lore. Answer questions based on the provided context from the Lexicanum wiki. Be accurate, detailed, and cite your sources when possible."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            confidence = self._calculate_confidence(answer, context)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "sources": self._extract_sources(context)
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "confidence": 0.0,
                "sources": []
            }
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build the prompt for the LLM"""
        return f"""
Context from Warhammer 40K Lexicanum:
{context}

Question: {question}

Please provide a detailed answer based on the context above. If the context doesn't contain enough information to answer the question, please say so and provide what information is available.
"""
    
    def _calculate_confidence(self, answer: str, context: str) -> float:
        """
        Calculate confidence score based on answer quality and context relevance
        This is a simple heuristic - in production, you might want more sophisticated scoring
        """
        if not answer or "don't know" in answer.lower() or "not enough information" in answer.lower():
            return 0.3
        
        # Simple confidence based on answer length and context usage
        context_words = set(context.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(context_words.intersection(answer_words))
        
        if overlap > 5:
            return 0.8
        elif overlap > 2:
            return 0.6
        else:
            return 0.4
    
    def _extract_sources(self, context: str) -> List[str]:
        """Extract source URLs from context"""
        # This would need to be implemented based on how you store source information
        # For now, return a placeholder
        return ["https://wh40k.lexicanum.com/wiki/Main_Page"]
    
    def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text using OpenAI's embedding model
        """
        try:
            if not self.api_key:
                return []
            
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return []
    
    def find_relevant_context(self, question: str, knowledge_base: List[Dict]) -> str:
        """
        Find the most relevant context from the knowledge base for a question
        """
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        scored_entries = []
        
        for entry in knowledge_base:
            score = 0
            content = entry.get('content', '').lower()
            title = entry.get('title', '').lower()
            key_terms = [term.lower() for term in entry.get('key_terms', [])]
            category = entry.get('main_category', '').lower()
            
            # Title match (highest weight)
            if any(word in title for word in question_words):
                score += 20
            
            # Key terms match
            for term in key_terms:
                if any(word in term for word in question_words):
                    score += 15
            
            # Content match
            content_overlap = len(question_words.intersection(set(content.split())))
            score += content_overlap * 2
            
            # Category match
            if any(word in category for word in question_words):
                score += 10
            
            # Phrase matching
            if question_lower in content:
                score += 25
            
            if score > 0:
                scored_entries.append({
                    'entry': entry,
                    'score': score,
                    'content': entry.get('content', ''),
                    'title': entry.get('title', ''),
                    'url': entry.get('url', '')
                })
        
        # Sort by score and take top entries
        scored_entries.sort(key=lambda x: x['score'], reverse=True)
        
        # Combine top 3 entries for context
        context_parts = []
        for entry in scored_entries[:3]:
            context_parts.append(f"Title: {entry['title']}\nContent: {entry['content'][:1000]}...")
        
        return "\n\n".join(context_parts)[:3000]  # Limit total context length
    
    def generate_enhanced_answer(self, question: str, context: str, model: str = "gpt-4") -> Dict:
        """
        Generate an enhanced answer with better prompting
        """
        try:
            if not self.api_key:
                return {
                    "answer": "LLM service not configured. Please set OPENAI_API_KEY environment variable.",
                    "confidence": 0.0,
                    "sources": []
                }
            
            # Enhanced prompt for Warhammer 40K context
            system_prompt = """You are a knowledgeable expert on Warhammer 40K lore. You have access to information from the Lexicanum wiki, which is a comprehensive source for Warhammer 40K information.

Guidelines for answering:
1. Be accurate and detailed in your responses
2. Use proper Warhammer 40K terminology and names
3. If the context doesn't contain enough information, say so clearly
4. Provide specific examples and details when available
5. Maintain the grimdark tone appropriate to the setting
6. Cite specific sources when possible
7. If asked about something not in the context, explain what you know and suggest where to find more information

Always be helpful and informative while staying true to the established lore."""
            
            user_prompt = f"""Context from Warhammer 40K Lexicanum:
{context}

Question: {question}

Please provide a detailed and accurate answer based on the context above. If the context doesn't contain enough information to fully answer the question, please provide what information is available and suggest where to find more details."""
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            confidence = self._calculate_enhanced_confidence(answer, context, question)
            sources = self._extract_sources_from_context(context)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error generating enhanced answer: {str(e)}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "confidence": 0.0,
                "sources": []
            }
    
    def _calculate_enhanced_confidence(self, answer: str, context: str, question: str) -> float:
        """
        Calculate confidence based on answer quality and context relevance
        """
        if not answer or "don't know" in answer.lower() or "not enough information" in answer.lower():
            return 0.3
        
        # Check for specific indicators of confidence
        confidence_indicators = [
            "according to", "as mentioned", "specifically", "in particular",
            "the lore states", "it is known that", "can be found"
        ]
        
        answer_lower = answer.lower()
        confidence_boost = sum(1 for indicator in confidence_indicators if indicator in answer_lower)
        
        # Base confidence on context usage
        context_words = set(context.lower().split())
        answer_words = set(answer_lower.split())
        overlap = len(context_words.intersection(answer_words))
        
        base_confidence = min(0.9, 0.4 + (overlap * 0.05) + (confidence_boost * 0.1))
        
        return base_confidence
    
    def _extract_sources_from_context(self, context: str) -> List[str]:
        """Extract source URLs from context"""
        sources = []
        lines = context.split('\n')
        
        for line in lines:
            if 'url:' in line.lower() or 'http' in line:
                # Extract URL from line
                url_match = re.search(r'https?://[^\s]+', line)
                if url_match:
                    sources.append(url_match.group())
        
        # If no URLs found, return default
        if not sources:
            sources = ["https://wh40k.lexicanum.com/wiki/Main_Page"]
        
        return sources[:3]  # Limit to top 3 sources

# Example usage
if __name__ == "__main__":
    service = LLMService()
    
    # Test question answering
    context = "Space Marines are the elite warriors of the Imperium of Man..."
    question = "What are Space Marines?"
    
    result = service.generate_answer(question, context)
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}")
