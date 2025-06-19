from fastapi import FastAPI
from pydantic import BaseModel
from recommender import fetch_matching_cards
from fastapi.middleware.cors import CORSMiddleware
from chat_agent import router as chat_agent_router



app = FastAPI()
app.include_router(chat_agent_router)
from chat_agent import router as chat_agent_router
app.include_router(chat_agent_router)

# Allow frontend to access backend (for later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User input model
class UserInput(BaseModel):
    income: int
    reward_preference: str
    max_joining_fee: float

# Recommendation endpoint
@app.post("/recommend")
def recommend(user_input: UserInput):
    cards = fetch_matching_cards(
        reward_preference=user_input.reward_preference,
        max_joining_fee=user_input.max_joining_fee,
        user_income=user_input.income  # ✅ Pass income
    )
    return {
        "message": f"Found {len(cards)} matching cards",
        "recommendations": cards
    }
