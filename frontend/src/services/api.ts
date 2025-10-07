import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for LLM requests
});

export interface QuestionRequest {
  question: string;
  context?: string;
}

export interface AnswerResponse {
  answer: string;
  sources: string[];
  confidence: number;
}

export interface TopicsResponse {
  topics: string[];
}

export const askQuestion = async (question: string): Promise<AnswerResponse> => {
  try {
    const response = await api.post<AnswerResponse>('/ask', {
      question,
    });
    return response.data;
  } catch (error) {
    console.error('Error asking question:', error);
    throw new Error('Failed to get answer. Please try again.');
  }
};

export const getTopics = async (): Promise<TopicsResponse> => {
  try {
    const response = await api.get<TopicsResponse>('/topics');
    return response.data;
  } catch (error) {
    console.error('Error fetching topics:', error);
    throw new Error('Failed to load topics. Please try again.');
  }
};

export const scrapeLexicanum = async (url: string, maxPages: number = 10): Promise<any> => {
  try {
    const response = await api.post('/scrape', {
      url,
      max_pages: maxPages,
    });
    return response.data;
  } catch (error) {
    console.error('Error scraping Lexicanum:', error);
    throw new Error('Failed to scrape data. Please try again.');
  }
};

export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

export const scrapePage = async (url: string, maxPages: number = 10): Promise<any> => {
  try {
    const response = await api.post('/scrape', {
      url,
      max_pages: maxPages,
    });
    return response.data;
  } catch (error) {
    console.error('Error scraping page:', error);
    throw new Error('Failed to scrape page. Please try again.');
  }
};

export const processData = async (): Promise<any> => {
  try {
    const response = await api.post('/process-data');
    return response.data;
  } catch (error) {
    console.error('Error processing data:', error);
    throw new Error('Failed to process data. Please try again.');
  }
};

export const searchKnowledgeBase = async (query: string, limit: number = 10): Promise<any> => {
  try {
    const response = await api.post('/search', {
      query,
      limit,
    });
    return response.data;
  } catch (error) {
    console.error('Error searching knowledge base:', error);
    throw new Error('Failed to search knowledge base. Please try again.');
  }
};
