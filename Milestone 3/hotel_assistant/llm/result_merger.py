"""Merge and Rank Results from KG and RAG"""
from typing import List, Dict, Any, Optional
from collections import defaultdict

from collections import defaultdict
from typing import Tuple

def merge_and_rank_results(
    cypher_output: List[Dict],
    embedding_output: Optional[List[Dict]],
    intent: str
) -> Dict[str, Any]:
    """
    Intelligently merge KG and embedding results.
    - Deduplicates hotels
    - Ranks by relevance
    - Enriches KG data with review insights
    """
    merged = {
        'primary_results': [],
        'supporting_reviews': [],
        'metadata': {
            'cypher_count': len(cypher_output) if cypher_output else 0,
            'embedding_count': len(embedding_output) if embedding_output else 0
        }
    }
    
    if not cypher_output and not embedding_output:
        merged['metadata']['has_results'] = False
        return merged
    
    merged['metadata']['has_results'] = True
    
    # Use KG results as primary source (structured data)
    if cypher_output:
        merged['primary_results'] = cypher_output
    
    # Add embedding results as supporting evidence
    if embedding_output:
        if intent in ["RECOMMEND_HOTEL", "DESCRIBE_HOTEL", "COMPARE_HOTELS"]:
            # Group reviews by hotel for context enrichment
            reviews_by_hotel = defaultdict(list)
            for review in embedding_output:
                hotel_name = review.get('hotel_name', '')
                reviews_by_hotel[hotel_name].append(review)
            
            merged['supporting_reviews'] = dict(reviews_by_hotel)
        else:
            # For LIST intent, just include unique hotels not in KG results
            kg_hotels = {r.get('hotel_name', '') for r in cypher_output} if cypher_output else set()
            unique_embedding = [
                r for r in embedding_output 
                if r.get('hotel_name', '') not in kg_hotels
            ]
            merged['supporting_reviews'] = unique_embedding[:5]
    
    return merged

print("merge_and_rank_results function defined")