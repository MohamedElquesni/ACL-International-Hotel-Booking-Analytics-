"""Entity Extraction from User Queries"""
import os
import json
from typing import Dict, Any
from openai import OpenAI

SCHEMAS = {
    "LIST_HOTELS": {"city": None, "country": None, "star_rating": None},
    "RECOMMEND_HOTEL": {"city": None, "country": None, "traveller_type": None,
                        "age_group": None, "user_gender": None, "star_rating": None, "aspects": None},
    "DESCRIBE_HOTEL": {"hotel_name": None, "aspects": None},
    "COMPARE_HOTELS": {"hotel1": None, "hotel2": None, "traveller_type": None, "aspects": None},
    "CHECK_VISA": {"from_country": None, "to_country": None}
}

ALLOWED_ASPECTS = ["cleanliness", "comfort", "facilities", "location", "staff", "value_for_money"]

def enforce_schema(intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    schema = SCHEMAS.get(intent, {})
    result = {}
    for key in schema.keys():
        value = entities.get(key)
        if value is not None and value != "" and value != []:
            result[key] = value
        else:
            result[key] = None
    return result

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_entities(text: str, intent: str) -> Dict[str, Any]:
    if intent not in SCHEMAS:
        return dict(SCHEMAS.get("LIST_HOTELS", {}))
    
    prompt = f"""Extract entities from this query and return ONLY valid JSON.
    
    Query: \"{text}\"
    Intent: {intent}
    Required keys: {list(SCHEMAS[intent].keys())}
    
    RULES:
    1. Extract ONLY explicitly mentioned entities
    2. Vague words (good, best, nice) do NOT extract aspects
    3. Aspects only if explicitly mentioned (e.g., "clean rooms" -> cleanliness)
    4. For possessive forms (e.g., "hotel's cleanliness"), extract the aspect after the possessive
    5. Preserve complete hotel names including articles (e.g., "The Azure Tower", not "Azure Tower")
    6. Allowed aspects: {ALLOWED_ASPECTS}
    7. traveller_type: family, solo, couple, business, group
    8. user_gender: male, female
    9. star_rating: 1-5 (numeric)
    
    Return ONLY JSON matching: {SCHEMAS[intent]}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=200
        )
        
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        
        entities = json.loads(raw)
        return enforce_schema(intent, entities)
    except Exception as e:
        print(f"Error: {e}")
        return dict(SCHEMAS[intent])