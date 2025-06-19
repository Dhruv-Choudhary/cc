from fastapi import APIRouter
from pydantic import BaseModel
from recommender import fetch_matching_cards
import re

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

# 🧠 Extraction helpers
def extract_income(text: str):
    match = re.search(r'(\d{4,6})', text.replace(",", ""))
    return int(match.group(1)) if match else None

def extract_reward_type(text: str):
    keywords = ["cashback", "lounge", "travel", "rewards"]
    for word in keywords:
        if word in text.lower():
            return word
    return None

def extract_max_fee(text: str):
    fee_keywords = ["joining", "fee", "budget", "under", "maximum", "not more than"]
    if any(k in text.lower() for k in fee_keywords):
        match = re.search(r'(\d{3,5})', text.replace(",", ""))
        return int(match.group(1)) if match else None
    return None

def extract_spending(text: str):
    categories = ["fuel", "groceries", "travel", "dining", "shopping"]
    found = [cat for cat in categories if cat in text.lower()]
    return found

def extract_existing_card(text: str):
    if "no card" in text.lower() or "don't have" in text.lower():
        return False
    if "have" in text.lower() or "own" in text.lower():
        return True
    return None

def extract_credit_score(text: str):
    match = re.search(r'(\d{3,4})', text)
    if match:
        score = int(match.group(1))
        if 300 <= score <= 900:
            return score
    if "unknown" in text.lower():
        return "unknown"
    return None

# 🧠 Smart chat endpoint
@router.post("/chat-agent")
def chat_agent(data: ChatRequest):
    try:
        income = None
        reward_type = None
        max_joining_fee = 3000
        has_card = False
        credit_score = None
        last_user_input = ""

        for msg in reversed(data.messages):
            if msg.role == "user":
                text = msg.content.lower()
                last_user_input = text

                if not income:
                    income = extract_income(text)
                if not reward_type:
                    reward_type = extract_reward_type(text)
                if not credit_score:
                    credit_score = extract_credit_score(text)
                if not max_joining_fee:
                    max_joining_fee = extract_max_fee(text) or max_joining_fee
                if "have" in text and "card" in text:
                    has_card = True

        # Exit phrases
        if any(p in last_user_input for p in ["exit", "quit", "bye", "stop"]):
            return {"reply": "Thanks for chatting! Come back anytime for more card suggestions."}

        # Casual responses
        if any(p in last_user_input for p in ["ok", "okay", "great", "thanks"]):
            return {"reply": "You're welcome! Let me know if you'd like to explore more cards or restart the chat."}

        # Handle user saying they already have a card
        if has_card and (not income or not reward_type):
            if not income:
                return {"reply": "Thanks for sharing. What is your monthly income?"}
            if not reward_type:
                return {"reply": "Got it. What kind of benefits are you looking for — cashback, travel, or lounge access?"}

        # Still missing required info
        if not income:
            return {"reply": "Please tell me your monthly income (e.g., ₹40000)."}
        if not reward_type:
            return {"reply": "Thanks! What kind of rewards do you prefer — cashback, lounge access, or travel points?"}

        # Final response
        reply = (
            f"Great! Based on your income ₹{income}, preference for {reward_type}, "
            f"and joining fee under ₹{max_joining_fee}, here are your top card options:"
        )
        cards = fetch_matching_cards(
            reward_preference=reward_type,
            max_joining_fee=max_joining_fee,
            user_income=income
        )
        return {"reply": reply, "recommendations": cards}

    except Exception as e:
        print("❌ Error in chat-agent:", str(e))
        return {"reply": f"❌ Something went wrong. {str(e)}"}
