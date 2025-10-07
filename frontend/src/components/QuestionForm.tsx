import React, { useState } from 'react';
import styled from 'styled-components';
import { Send, Loader } from 'lucide-react';
import { askQuestion } from '../services/api';

const FormContainer = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  border: 1px solid rgba(255, 107, 53, 0.2);
`;

const FormTitle = styled.h2`
  color: #ffffff;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const TextArea = styled.textarea`
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 107, 53, 0.3);
  border-radius: 10px;
  padding: 1rem;
  color: #ffffff;
  font-size: 1rem;
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
  
  &::placeholder {
    color: #cccccc;
  }
  
  &:focus {
    outline: none;
    border-color: #ff6b35;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.2);
  }
`;

const SubmitButton = styled.button<{ loading: boolean }>`
  background: linear-gradient(45deg, #ff6b35, #f7931e);
  border: none;
  border-radius: 10px;
  padding: 1rem 2rem;
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: ${props => props.loading ? 'not-allowed' : 'pointer'};
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  opacity: ${props => props.loading ? 0.7 : 1};
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
  }
  
  &:disabled {
    cursor: not-allowed;
  }
`;

const ExampleQuestions = styled.div`
  margin-top: 1.5rem;
`;

const ExampleTitle = styled.h3`
  color: #cccccc;
  font-size: 1rem;
  margin-bottom: 1rem;
`;

const ExampleList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
`;

const ExampleButton = styled.button`
  background: rgba(255, 107, 53, 0.2);
  border: 1px solid rgba(255, 107, 53, 0.5);
  border-radius: 20px;
  padding: 0.5rem 1rem;
  color: #ff6b35;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 107, 53, 0.3);
    transform: translateY(-1px);
  }
`;

interface QuestionFormProps {
  onAnswer: (answer: any) => void;
}

const exampleQuestions = [
  "What are Space Marines?",
  "Tell me about the Horus Heresy",
  "Who is the Emperor of Mankind?",
  "What is the Warp?",
  "Explain Chaos Space Marines",
  "What are the different Space Marine chapters?"
];

const QuestionForm: React.FC<QuestionFormProps> = ({ onAnswer }) => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    setLoading(true);
    try {
      const answer = await askQuestion(question);
      onAnswer(answer);
    } catch (error) {
      console.error('Error asking question:', error);
      onAnswer({
        answer: "Sorry, I encountered an error while processing your question. Please try again.",
        confidence: 0,
        sources: []
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuestion: string) => {
    setQuestion(exampleQuestion);
  };

  return (
    <FormContainer>
      <FormTitle>Ask About Warhammer 40K Lore</FormTitle>
      <Form onSubmit={handleSubmit}>
        <TextArea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask me anything about Warhammer 40K lore... (e.g., What are Space Marines? Tell me about the Horus Heresy)"
          disabled={loading}
        />
        <SubmitButton type="submit" loading={loading} disabled={loading}>
          {loading ? (
            <>
              <Loader className="animate-spin" />
              Thinking...
            </>
          ) : (
            <>
              <Send />
              Ask Question
            </>
          )}
        </SubmitButton>
      </Form>

      <ExampleQuestions>
        <ExampleTitle>Try these example questions:</ExampleTitle>
        <ExampleList>
          {exampleQuestions.map((example, index) => (
            <ExampleButton
              key={index}
              type="button"
              onClick={() => handleExampleClick(example)}
              disabled={loading}
            >
              {example}
            </ExampleButton>
          ))}
        </ExampleList>
      </ExampleQuestions>
    </FormContainer>
  );
};

export default QuestionForm;
