# 💳 Credit Card Recommender (LLM-Powered)

An AI-powered credit card recommendation system that uses a conversational agent to guide users and recommend the best Indian credit cards based on their income, spending habits, and preferences.

---

## 🚀 Features

- 🤖 Conversational chatbot powered by OpenAI API
- 💰 Smart recommendations based on:
  - Monthly income
  - Reward type (cashback, travel, lounge, rewards)
  - Joining fee filter
- 📊 Card comparison view with estimated reward calculations
- 📱 Mobile responsive frontend built in React
- 🔧 Backend using FastAPI + MySQL
- ✅ WhatsApp integration (Twilio API)
- 🔄 Memory: Remembers previous user inputs during chat

---

## 🧠 Technologies Used

- React (Frontend)
- FastAPI (Backend)
- OpenAI (LLM Agent)
- MySQL (Database)
- Axios (Frontend-backend communication)


---

## 📦 How to Run Locally

### 1. Clone this repo
```bash
git clone https://github.com/Dhruv-Choudhary/credit-card-recommendor.git
cd credit-card-recommendor

### 2 backup setup 
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

####frontend setup
cd frontend
npm install
npm start
