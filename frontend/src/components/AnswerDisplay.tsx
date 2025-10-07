import React from 'react';
import styled from 'styled-components';
import { BookOpen, ExternalLink, CheckCircle, AlertCircle } from 'lucide-react';

const AnswerContainer = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  margin-top: 2rem;
  border: 1px solid rgba(255, 107, 53, 0.2);
`;

const AnswerHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const AnswerIcon = styled.div`
  color: #ff6b35;
  font-size: 1.5rem;
`;

const AnswerTitle = styled.h3`
  color: #ffffff;
  margin: 0;
  font-size: 1.5rem;
`;

const ConfidenceIndicator = styled.div<{ confidence: number }>`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: ${props => {
    if (props.confidence > 0.7) return 'rgba(34, 197, 94, 0.2)';
    if (props.confidence > 0.4) return 'rgba(251, 191, 36, 0.2)';
    return 'rgba(239, 68, 68, 0.2)';
  }};
  border: 1px solid ${props => {
    if (props.confidence > 0.7) return 'rgba(34, 197, 94, 0.5)';
    if (props.confidence > 0.4) return 'rgba(251, 191, 36, 0.5)';
    return 'rgba(239, 68, 68, 0.5)';
  }};
  color: ${props => {
    if (props.confidence > 0.7) return '#22c55e';
    if (props.confidence > 0.4) return '#fbbf24';
    return '#ef4444';
  }};
  font-size: 0.9rem;
  font-weight: 600;
`;

const AnswerText = styled.div`
  color: #ffffff;
  line-height: 1.8;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  
  p {
    margin-bottom: 1rem;
  }
  
  p:last-child {
    margin-bottom: 0;
  }
`;

const SourcesSection = styled.div`
  border-top: 1px solid rgba(255, 107, 53, 0.2);
  padding-top: 1.5rem;
`;

const SourcesTitle = styled.h4`
  color: #cccccc;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const SourcesList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const SourceItem = styled.li`
  margin-bottom: 0.5rem;
`;

const SourceLink = styled.a`
  color: #ff6b35;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 8px;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.2);
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 107, 53, 0.2);
    transform: translateX(5px);
  }
`;

const NoSources = styled.div`
  color: #888888;
  font-style: italic;
`;

interface AnswerDisplayProps {
  answer: {
    answer: string;
    confidence: number;
    sources: string[];
  };
}

const AnswerDisplay: React.FC<AnswerDisplayProps> = ({ answer }) => {
  const getConfidenceText = (confidence: number) => {
    if (confidence > 0.7) return 'High Confidence';
    if (confidence > 0.4) return 'Medium Confidence';
    return 'Low Confidence';
  };

  const getConfidenceIcon = (confidence: number) => {
    if (confidence > 0.7) return <CheckCircle size={16} />;
    if (confidence > 0.4) return <AlertCircle size={16} />;
    return <AlertCircle size={16} />;
  };

  return (
    <AnswerContainer>
      <AnswerHeader>
        <AnswerIcon>
          <BookOpen />
        </AnswerIcon>
        <AnswerTitle>Answer</AnswerTitle>
        <ConfidenceIndicator confidence={answer.confidence}>
          {getConfidenceIcon(answer.confidence)}
          {getConfidenceText(answer.confidence)}
        </ConfidenceIndicator>
      </AnswerHeader>

      <AnswerText>
        {answer.answer.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </AnswerText>

      <SourcesSection>
        <SourcesTitle>
          <ExternalLink size={16} />
          Sources
        </SourcesTitle>
        {answer.sources && answer.sources.length > 0 ? (
          <SourcesList>
            {answer.sources.map((source, index) => (
              <SourceItem key={index}>
                <SourceLink href={source} target="_blank" rel="noopener noreferrer">
                  <ExternalLink size={14} />
                  {source}
                </SourceLink>
              </SourceItem>
            ))}
          </SourcesList>
        ) : (
          <NoSources>No specific sources available</NoSources>
        )}
      </SourcesSection>
    </AnswerContainer>
  );
};

export default AnswerDisplay;
