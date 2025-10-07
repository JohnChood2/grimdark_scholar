import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { BookOpen, ChevronRight, Loader } from 'lucide-react';
import { getTopics } from '../services/api';

const BrowserContainer = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  border: 1px solid rgba(255, 107, 53, 0.2);
`;

const BrowserTitle = styled.h2`
  color: #ffffff;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
`;

const TopicsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
`;

const TopicCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 107, 53, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(255, 107, 53, 0.3);
    border-color: #ff6b35;
  }
`;

const TopicIcon = styled.div`
  color: #ff6b35;
  font-size: 2rem;
  margin-bottom: 1rem;
`;

const TopicName = styled.h3`
  color: #ffffff;
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
`;

const TopicDescription = styled.p`
  color: #cccccc;
  font-size: 0.9rem;
  line-height: 1.5;
`;

const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #ff6b35;
  gap: 1rem;
`;

const ErrorMessage = styled.div`
  color: #ef4444;
  text-align: center;
  padding: 2rem;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(239, 68, 68, 0.3);
`;

const TopicBrowser: React.FC = () => {
  const [topics, setTopics] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const topicsData = await getTopics();
        setTopics(topicsData.topics || []);
      } catch (err) {
        setError('Failed to load topics. Please try again later.');
        console.error('Error fetching topics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
  }, []);

  const handleTopicClick = (topic: string) => {
    // This could open a detailed view or search for that topic
    console.log(`Clicked on topic: ${topic}`);
    // For now, we'll just log it. In a full implementation, you might:
    // - Navigate to a topic detail page
    // - Pre-fill a search with that topic
    // - Show related articles
  };

  if (loading) {
    return (
      <BrowserContainer>
        <BrowserTitle>Browse Topics</BrowserTitle>
        <LoadingContainer>
          <Loader className="animate-spin" />
          Loading topics...
        </LoadingContainer>
      </BrowserContainer>
    );
  }

  if (error) {
    return (
      <BrowserContainer>
        <BrowserTitle>Browse Topics</BrowserTitle>
        <ErrorMessage>{error}</ErrorMessage>
      </BrowserContainer>
    );
  }

  return (
    <BrowserContainer>
      <BrowserTitle>Browse Topics</BrowserTitle>
      <TopicsGrid>
        {topics.map((topic, index) => (
          <TopicCard key={index} onClick={() => handleTopicClick(topic)}>
            <TopicIcon>
              <BookOpen />
            </TopicIcon>
            <TopicName>{topic}</TopicName>
            <TopicDescription>
              Explore articles and information about {topic} in the Warhammer 40K universe.
            </TopicDescription>
          </TopicCard>
        ))}
      </TopicsGrid>
    </BrowserContainer>
  );
};

export default TopicBrowser;
