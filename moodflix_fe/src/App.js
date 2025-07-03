import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  // 채팅 메시지 목록 상태
  const [messages, setMessages] = useState([]);
  // 입력창에 입력된 메시지 상태
  const [inputMessage, setInputMessage] = useState('');
  // 로딩(타이핑) 상태
  const [isLoading, setIsLoading] = useState(false);
  // 스크롤 하단 이동을 위한 ref
  const messagesEndRef = useRef(null);

  // 새로운 메시지가 추가될 때마다 스크롤을 맨 아래로 이동
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 메시지 전송 함수
  const sendMessage = async () => {
    if (!inputMessage.trim()) return; // 빈 메시지 방지

    // 사용자 메시지 객체 생성
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    // 사용자 메시지를 화면에 추가
    setMessages(prev => [...prev, userMessage]);
    setInputMessage(''); // 입력창 비우기
    setIsLoading(true);  // 로딩 상태 표시

    try {
      // 서버로 POST 요청 보내기
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage
        })
      });

      // HTTP 에러 처리
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 서버 응답 데이터 파싱
      const data = await response.json();
      
      // 응답 데이터에 response 필드가 없을 경우 에러
      if (!data.response) {
        throw new Error('응답 데이터에 response 필드가 없습니다');
      }

      // 봇 메시지 객체 생성
      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };

      // 봇 메시지를 화면에 추가
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      // 에러 발생 시 에러 메시지 출력 및 안내 메시지 표시
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: '죄송합니다. 메시지를 전송하는 중 오류가 발생했습니다.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false); // 로딩 상태 해제
    }
  };

  // Enter 키로 메시지 전송, Shift+Enter로 줄바꿈
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>💬 채팅</h1>
        </div>
        
        <div className="messages-container">
          {/* 메시지 없을 때 환영 메시지 */}
          {messages.length === 0 && (
            <div className="welcome-message">
              <p>안녕하세요! 무엇을 도와드릴까요? 😊</p>
            </div>
          )}
          
          {/* 메시지 목록 렌더링 */}
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              {/* 봇 메시지일 때만 프로필 사진 표시 */}
              {message.sender === 'bot' && (
                <div className="profile-image">
                  <img src="/saba.jpg" alt="봇 프로필" />
                </div>
              )}
              <div className="message-content">
                <p>{message.text}</p>
                <span className="timestamp">{message.timestamp}</span>
              </div>
            </div>
          ))}
          
          {/* 로딩(타이핑) 인디케이터 */}
          {isLoading && (
            <div className="message bot-message">
              <div className="profile-image">
                <img src="/saba.jpg" alt="봇 프로필" />
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          {/* 스크롤 하단 이동용 더미 div */}
          <div ref={messagesEndRef} />
        </div>
        
        {/* 입력창 및 전송 버튼 */}
        <div className="input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="메시지를 입력하세요..."
            disabled={isLoading}
          />
          <button 
            onClick={sendMessage} 
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            전송
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
