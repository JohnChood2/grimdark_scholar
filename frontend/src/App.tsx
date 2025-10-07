import React, { useState } from 'react';
import styled from 'styled-components';
import { Search, BookOpen, Shield, Zap } from 'lucide-react';
import QuestionForm from './components/QuestionForm';
import AnswerDisplay from './components/AnswerDisplay';
import TopicBrowser from './components/TopicBrowser';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #ffffff;
`;

const Header = styled.header`
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  padding: 2rem 0;
  text-align: center;
  border-bottom: 2px solid #ff6b35;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin: 0;
  background: linear-gradient(45deg, #ff6b35, #f7931e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(255, 107, 53, 0.5);
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin: 0.5rem 0 0 0;
  color: #cccccc;
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
`;

const FeatureCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  border: 1px solid rgba(255, 107, 53, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
  }
`;

const FeatureIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ff6b35;
`;

const FeatureTitle = styled.h3`
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #ffffff;
`;

const FeatureDescription = styled.p`
  color: #cccccc;
  line-height: 1.6;
`;

const TabContainer = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem;
  margin-top: 2rem;
`;

const TabButtons = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
`;

const TabButton = styled.button<{ active: boolean }>`
  background: ${props => props.active ? '#ff6b35' : 'transparent'};
  border: 2px solid #ff6b35;
  color: ${props => props.active ? '#ffffff' : '#ff6b35'};
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  
  &:hover {
    background: #ff6b35;
    color: #ffffff;
  }
`;

type TabType = 'ask' | 'browse';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('ask');
  const [currentAnswer, setCurrentAnswer] = useState<any>(null);

  const handleAnswer = (answer: any) => {
    setCurrentAnswer(answer);
  };

  return (
    <AppContainer>
      <Header>
        <Title>Warhammer 40K Lore Assistant</Title>
        <Subtitle>Your gateway to the grim darkness of the far future</Subtitle>
      </Header>

      <MainContent>
        <FeatureGrid>
          <FeatureCard>
            <FeatureIcon>
              <BookOpen />
            </FeatureIcon>
            <FeatureTitle>Comprehensive Lore</FeatureTitle>
            <FeatureDescription>
              Access thousands of articles from the Lexicanum wiki covering all aspects of Warhammer 40K lore.
            </FeatureDescription>
          </FeatureCard>

          <FeatureCard>
            <FeatureIcon>
              <Search />
            </FeatureIcon>
            <FeatureTitle>AI-Powered Search</FeatureTitle>
            <FeatureDescription>
              Ask questions in natural language and get detailed, accurate answers about the 40K universe.
            </FeatureDescription>
          </FeatureCard>

          <FeatureCard>
            <FeatureIcon>
              <Shield />
            </FeatureIcon>
            <FeatureTitle>Reliable Sources</FeatureTitle>
            <FeatureDescription>
              All information is sourced from the official Lexicanum wiki, ensuring accuracy and reliability.
            </FeatureDescription>
          </FeatureCard>

          <FeatureCard>
            <FeatureIcon>
              <Zap />
            </FeatureIcon>
            <FeatureTitle>Fast & Responsive</FeatureTitle>
            <FeatureDescription>
              Get instant answers to your questions with our optimized search and AI integration.
            </FeatureDescription>
          </FeatureCard>
        </FeatureGrid>

        <TabContainer>
          <TabButtons>
            <TabButton 
              active={activeTab === 'ask'} 
              onClick={() => setActiveTab('ask')}
            >
              Ask a Question
            </TabButton>
            <TabButton 
              active={activeTab === 'browse'} 
              onClick={() => setActiveTab('browse')}
            >
              Browse Topics
            </TabButton>
          </TabButtons>

          {activeTab === 'ask' && (
            <>
              <QuestionForm onAnswer={handleAnswer} />
              {currentAnswer && <AnswerDisplay answer={currentAnswer} />}
            </>
          )}

          {activeTab === 'browse' && (
            <TopicBrowser />
          )}
        </TabContainer>
      </MainContent>
    </AppContainer>
  );
}

export default App;
