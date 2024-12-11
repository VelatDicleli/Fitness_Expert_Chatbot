import React, { useState } from "react";
import axios from "axios";
import "./Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSendMessage = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: "user" }]);

      try {
        const response = await axios.post("http://chatbot-api-1968973726.eu-north-1.elb.amazonaws.com/chat", {
          message: input,
        });

        setMessages((prev) => [
          ...prev,
          { text: response.data, sender: "bot" },
        ]);
      } catch (error) {
        setMessages((prev) => [
          ...prev,
          { text: "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.", sender: "bot" },
        ]);
      }

      setInput("");
    }
  };

  return (
    <div className="chatbot">
      <div className="chatbox">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-box">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Write your message..."
        />
        <button onClick={handleSendMessage}>Gönder</button>
      </div>
    </div>
  );
};

export default Chatbot;
