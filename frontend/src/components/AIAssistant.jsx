import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

/**
 * AIAssistant Component
 * Conversational AI security assistant that explains threats and provides guidance
 */
function AIAssistant({ user }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: 'Hello! 👋 I\'m your AI Security Assistant. I can help you understand cybersecurity threats, explain security concepts, and give you personalized security advice. What would you like to know?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: input,
      timestamp: new Date()
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await axios.post(
        `${API_BASE}/security/ai-assistance`,
        { query: input },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const assistantMessage = {
        id: messages.length + 2,
        sender: 'assistant',
        text: response.data.message,
        category: response.data.category,
        references: response.data.references,
        followUp: response.data.follow_up_questions,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = {
        id: messages.length + 2,
        sender: 'assistant',
        text: 'I encountered an error processing your question. Please try again.',
        isError: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      setError(err.response?.data?.message || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickQuestion = (question) => {
    setInput(question);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 h-screen flex flex-col">
      <div className="bg-white dark:bg-gray-800 rounded-t-lg shadow-lg p-6 border-b dark:border-gray-700">
        <div className="flex items-center space-x-3">
          <span className="text-4xl">🤖</span>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Security Assistant</h1>
            <p className="text-gray-600 dark:text-gray-400">Ask me anything about cybersecurity</p>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 bg-gray-50 dark:bg-gray-900 overflow-y-auto p-6 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-md ${msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-800'} p-4 rounded-lg shadow`}>
              <p className={`text-sm ${msg.sender === 'user' ? 'text-white' : 'text-gray-900 dark:text-white'}`}>
                {msg.text}
              </p>
              {msg.followUp && msg.followUp.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-300 dark:border-gray-600">
                  <p className="text-xs font-semibold mb-2 text-gray-700 dark:text-gray-300">Follow-up questions:</p>
                  <div className="space-y-1">
                    {msg.followUp.map((question, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleQuickQuestion(question)}
                        className="block w-full text-left text-xs text-blue-600 dark:text-blue-400 hover:underline"
                      >
                        → {question}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              <p className="text-xs mt-2 opacity-70">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions */}
      {messages.length === 1 && (
        <div className="bg-white dark:bg-gray-800 border-t dark:border-gray-700 p-4 space-y-2">
          <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">💡 Try asking about:</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            <QuickButton 
              text="What is phishing?" 
              onClick={() => handleQuickQuestion('What is phishing and how can I protect myself?')}
            />
            <QuickButton 
              text="How to create strong passwords"
              onClick={() => handleQuickQuestion('What makes a password strong and secure?')}
            />
            <QuickButton 
              text="What is two-factor authentication?"
              onClick={() => handleQuickQuestion('What is two-factor authentication and why is it important?')}
            />
            <QuickButton 
              text="How to stay safe online"
              onClick={() => handleQuickQuestion('What are the best practices to stay safe online?')}
            />
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 dark:bg-red-900 border-t border-red-400 dark:border-red-700 p-3">
          <p className="text-red-700 dark:text-red-200 text-sm">Error: {error}</p>
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={sendMessage} className="bg-white dark:bg-gray-800 border-t dark:border-gray-700 p-4 rounded-b-lg shadow-lg">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a security question..."
            disabled={loading}
            className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
          >
            {loading ? '...' : '📤'}
          </button>
        </div>
      </form>
    </div>
  );
}

function QuickButton({ text, onClick }) {
  return (
    <button
      onClick={onClick}
      className="text-left px-4 py-2 bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg text-blue-700 dark:text-blue-200 hover:bg-blue-100 dark:hover:bg-blue-800 transition text-sm font-medium"
    >
      {text}
    </button>
  );
}

export default AIAssistant;
