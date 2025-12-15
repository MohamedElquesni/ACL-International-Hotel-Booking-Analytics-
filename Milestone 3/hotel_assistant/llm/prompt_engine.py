"""Intent-Specific Prompt Engineering"""
from typing import Tuple

class PromptEngine:
    """Generates optimized prompts for each intent with few-shot examples."""
    
    @staticmethod
    def get_prompts(intent: str, query: str, context: str) -> Tuple[str, str]:
        """Generate system and user prompts."""
        
        base_system = """You are an expert hotel assistant with access to a comprehensive hotel knowledge graph.

CRITICAL RULES:
1. Answer EXCLUSIVELY using the provided context data
2. NEVER use external knowledge or assumptions
3. If data is insufficient, explicitly state what's missing
4. Be precise, accurate, and cite specific numbers from the context
5. Maintain a professional yet friendly tone"""
        
        if intent == "LIST_HOTELS":
            system = base_system + """

TASK: Present hotels as a clear, scannable list
FORMAT:
                For each hotel, present it as:
                - A short one-line summary
                - Key details shown as labeled bullets
                - Use friendly but concise language  
TONE: Concise and helpful"""
            
            user = f"""CONTEXT:
{context}

USER QUERY: "{query}"

Provide a clear numbered list of hotels:"""

        elif intent == "RECOMMEND_HOTEL":
            system = base_system + """

TASK: Recommend hotels and explain WHY
FORMAT: Top 2-3 recommendations with reasoning
TONE: Persuasive but honest
INCLUDE: Specific scores, review counts, and guest feedback quotes"""
            
            user = f"""CONTEXT:
{context}

USER QUERY: "{query}"

Provide recommendations with clear reasoning:"""

        elif intent == "DESCRIBE_HOTEL":
            system = base_system + """

TASK: Provide comprehensive hotel description
FORMAT: Structured overview covering all available aspects
TONE: Informative and balanced
INCLUDE: Base ratings, review scores, and guest experiences"""
            
            user = f"""CONTEXT:
{context}

USER QUERY: "{query}"

Provide a detailed, well-structured description:"""

        elif intent == "COMPARE_HOTELS":
            system = base_system + """

TASK: Compare hotels objectively using base ratings
FORMAT: Side-by-side comparison highlighting differences
TONE: Analytical and balanced
INCLUDE: Specific rating differences, clear winner per category
IMPORTANT: Use the BASE RATINGS for comparison (not review scores)"""
            
            user = f"""CONTEXT:
{context}

USER QUERY: "{query}"

Provide a structured comparison:"""

        elif intent == "CHECK_VISA":
            system = base_system + """

TASK: Provide visa requirement information
FORMAT: Start with clear YES/NO, then details
TONE: Factual and authoritative
INCLUDE: Visa type if applicable"""
            
            user = f"""CONTEXT:
{context}

USER QUERY: "{query}"

Provide clear visa information:"""
        
        else:
            system = base_system
            user = f"Context:\\n{context}\\n\\nQuestion: {query}\\n\\nAnswer:"
        
        return system, user

print("PromptEngine class defined")