from database import get_db_connection

def fetch_matching_cards(reward_preference: str, max_joining_fee: float, user_income: int):
    try:
        print("Connecting to DB...")
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        if reward_preference.strip() == "":
            print("No reward preference, running basic query")
            query = """
                SELECT * FROM credit_cards
                WHERE joining_fee <= %s
                ORDER BY joining_fee ASC
                LIMIT 5
            """
            cursor.execute(query, (max_joining_fee,))
        else:
            print("Reward preference:", reward_preference)
            query = """
                SELECT * FROM credit_cards
                WHERE LOWER(reward_type) LIKE %s AND joining_fee <= %s
                ORDER BY joining_fee ASC
                LIMIT 5
            """
            cursor.execute(query, (f"%{reward_preference.lower()}%", max_joining_fee))

        results = cursor.fetchall()
        print("Query returned:", len(results), "results")

        # Add reward simulation and reason
        cards = [enrich_card(card, user_income) for card in results]

        cursor.close()
        db.close()
        return cards

    except Exception as e:
        print("❌ ERROR in fetch_matching_cards:", str(e))
        return []


def enrich_card(card, user_income):
    try:
        # Assume user spends ~30% of income per month
        monthly_spend = user_income * 0.3

        # Try to find percentage in reward_rate
        reward_text = card.get("reward_rate", "") or card.get("reward_type", "")
        percent = 0
        for token in reward_text.split():
            if "%" in token:
                try:
                    percent = float(token.replace("%", "").strip())
                    break
                except:
                    pass

        estimated_annual_reward = round((monthly_spend * percent / 100) * 12, 2)
        reason = f"This card offers {percent}% {card['reward_type']} on spends."

        return {
            **card,
            "estimated_annual_reward": f"₹{estimated_annual_reward:,}",
            "recommendation_reason": reason
        }
    except Exception as e:
        print("⚠️ Error in enrich_card:", e)
        return card
