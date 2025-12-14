"""Intent Classification using OpenAI"""
import os
from typing import Optional, Dict, Any
from openai import OpenAI

SCHEMAS: Dict[str, Dict[str, Any]] = {
    "LIST_HOTELS": {"city": None, "country": None, "star_rating": None},
    "RECOMMEND_HOTEL": {"city": None, "country": None, "traveller_type": None, 
                        "age_group": None, "user_gender": None, "star_rating": None, "aspects": None},
    "DESCRIBE_HOTEL": {"hotel_name": None, "aspects": None},
    "COMPARE_HOTELS": {"hotel1": None, "hotel2": None, "traveller_type": None, "aspects": None},
    "CHECK_VISA": {"from_country": None, "to_country": None}
}

ALLOWED_ASPECTS = ["cleanliness", "comfort", "facilities", "location", "staff", "value_for_money"]


class IntentClassifier:
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.intents = {
            "LIST_HOTELS": "Find multiple hotels matching filters",
            "RECOMMEND_HOTEL": "Get personalized suggestions",
            "DESCRIBE_HOTEL": "Get details about one hotel",
            "COMPARE_HOTELS": "Compare multiple hotels",
            "CHECK_VISA": "Check visa requirements"
        }
    
    def classify(self, user_query: str) -> Optional[str]:
        prompt = f"""Classify this query into ONE intent: {list(self.intents.keys())} or return NONE.
        
        Intent definitions:
        - LIST_HOTELS: neutral search (keywords: show, find, list)
        - RECOMMEND_HOTEL: opinions/advice (keywords: recommend, suggest, best, top)
        - DESCRIBE_HOTEL: one specific hotel (must mention hotel name)
        - COMPARE_HOTELS: multiple hotels (keywords: compare, vs, which is better)
        - CHECK_VISA: visa requirements (keywords: visa, entry requirement)
        
        Query: \"{user_query}\"
        
        Return ONLY the intent name or NONE."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=20
            )
            intent = response.choices[0].message.content.strip().upper()
            return intent if intent in self.intents else None
        except Exception as e:
            print(f"Error: {e}")
            return None