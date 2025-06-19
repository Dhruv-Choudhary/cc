import openai
import os
from dotenv import load_dotenv
from recommender import fetch_matching_cards

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask(question):
    answer = input(f"🤖 {question}\n> ")
    return answer.strip()

def chat_summary(user_data, recommendations):
    print("\n✅ Summary of Your Inputs:")
    for k, v in user_data.items():
        print(f"  • {k}: {v}")
    print("\n🎯 Top Card Recommendations:")
    if recommendations:
        for i, card in enumerate(recommendations, start=1):
            print(f"\n{i}. {card['name']} ({card['issuer']})")
            print(f"   💳 Fee: ₹{card['joining_fee']} | {card['reward_type']} – {card['reward_rate']}")
            print(f"   ✨ Perks: {card['perks']}")
    else:
        print("No matching cards found. Try different inputs.")

def main():
    print("💬 Welcome to the Credit Card Recommender!")
    print("I'll ask a few quick questions to find your ideal card.\n")

    user_data = {
        "income": ask("What is your monthly income (₹)?"),
        "spending": ask("Where do you spend most? (fuel/travel/dining/groceries/etc)"),
        "reward_preference": ask("Do you prefer cashback, travel points, or lounge access?"),
        "existing_cards": ask("Do you already have any credit cards? (optional)"),
        "credit_score": ask("What is your approx credit score? (or type 'unknown')")
    }

    try:
        max_fee = 2000  # you can ask this too
        cards = fetch_matching_cards(
            reward_preference=user_data["reward_preference"],
            max_joining_fee=max_fee
        )
        chat_summary(user_data, cards)
    except Exception as e:
        print("⚠️ Error during recommendation:", e)

if __name__ == "__main__":
    main()
