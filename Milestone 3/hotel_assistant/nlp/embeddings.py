"""Semantic Search using Vector Embeddings"""
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from ..database.neo4j_connection import Neo4jConnection

embedder_minilm = SentenceTransformer('all-MiniLM-L6-v2')
embedder_mpnet = SentenceTransformer('all-mpnet-base-v2')
conn_rag = Neo4jConnection()

def semantic_search_minilm(query: str, top_k: int = 5, threshold: float = 0.65):
    """
    Semantic search with MiniLM embeddings and similarity threshold.
    
    Args:
        query: Search query
        top_k: Maximum number of results
        threshold: Minimum similarity score (0-1). Results below this are filtered out.
    
    Returns:
        List of results with similarity >= threshold
    """
    query_embedding = embedder_minilm.encode([query], convert_to_numpy=True)[0].tolist()
    
    search_query = """
    CALL db.index.vector.queryNodes('review_minilm_index', $top_k, $query_embedding)
    YIELD node, score
    RETURN node.review_id AS review_id,
           node.hotel_name AS hotel_name,
           node.city AS city,
           node.country AS country,
           node.traveller_type AS traveller_type,
           node.review_text AS review_text,
           score
    """
    
    results = conn_rag.execute_query(search_query, {
        'query_embedding': query_embedding,
        'top_k': top_k
    })
    
    # Filter by similarity threshold
    filtered_results = [r for r in results if r['score'] >= threshold]
    
    return filtered_results

def semantic_search_mpnet(query: str, top_k: int = 5, threshold: float = 0.65):
    """
    Semantic search with MPNet embeddings and similarity threshold.
    
    Args:
        query: Search query
        top_k: Maximum number of results
        threshold: Minimum similarity score (0-1). Results below this are filtered out.
    
    Returns:
        List of results with similarity >= threshold
    """
    query_embedding = embedder_mpnet.encode([query], convert_to_numpy=True)[0].tolist()
    
    search_query = """
    CALL db.index.vector.queryNodes('review_mpnet_index', $top_k, $query_embedding)
    YIELD node, score
    RETURN node.review_id AS review_id,
           node.hotel_name AS hotel_name,
           node.city AS city,
           node.country AS country,
           node.traveller_type AS traveller_type,
           node.review_text AS review_text,
           score
    """
    
    results = conn_rag.execute_query(search_query, {
        'query_embedding': query_embedding,
        'top_k': top_k
    })
    
    # Filter by similarity threshold
    filtered_results = [r for r in results if r['score'] >= threshold]
    
    return filtered_results

print("Semantic search functions with threshold filtering defined")
print("Default threshold: 0.65 (moderate relevance)")
print("Recommended thresholds:")
print("  - 0.80+: Very high similarity")
print("  - 0.70-0.80: Good match")
print("  - 0.60-0.70: Moderate match")
print("  - < 0.60: Low relevance (filtered out)")

def semantic_search_minilm(query: str, top_k: int = 5, threshold: float = 0.65):
    """
    Semantic search with MiniLM embeddings and similarity threshold.
    
    Args:
        query: Search query
        top_k: Maximum number of results
        threshold: Minimum similarity score (0-1). Results below this are filtered out.
    
    Returns:
        List of results with similarity >= threshold
    """
    query_embedding = embedder_minilm.encode([query], convert_to_numpy=True)[0].tolist()
    
    search_query = """
    CALL db.index.vector.queryNodes('review_minilm_index', $top_k, $query_embedding)
    YIELD node, score
    RETURN node.review_id AS review_id,
           node.hotel_name AS hotel_name,
           node.city AS city,
           node.country AS country,
           node.traveller_type AS traveller_type,
           node.review_text AS review_text,
           score
    """
    
    results = conn_rag.execute_query(search_query, {
        'query_embedding': query_embedding,
        'top_k': top_k
    })
    
    # Filter by similarity threshold
    filtered_results = [r for r in results if r['score'] >= threshold]
    
    return filtered_results

def semantic_search_mpnet(query: str, top_k: int = 5, threshold: float = 0.65):
    """
    Semantic search with MPNet embeddings and similarity threshold.
    
    Args:
        query: Search query
        top_k: Maximum number of results
        threshold: Minimum similarity score (0-1). Results below this are filtered out.
    
    Returns:
        List of results with similarity >= threshold
    """
    query_embedding = embedder_mpnet.encode([query], convert_to_numpy=True)[0].tolist()
    
    search_query = """
    CALL db.index.vector.queryNodes('review_mpnet_index', $top_k, $query_embedding)
    YIELD node, score
    RETURN node.review_id AS review_id,
           node.hotel_name AS hotel_name,
           node.city AS city,
           node.country AS country,
           node.traveller_type AS traveller_type,
           node.review_text AS review_text,
           score
    """
    
    results = conn_rag.execute_query(search_query, {
        'query_embedding': query_embedding,
        'top_k': top_k
    })
    
    # Filter by similarity threshold
    filtered_results = [r for r in results if r['score'] >= threshold]
    
    return filtered_results

print("Semantic search functions with threshold filtering defined")
print("Default threshold: 0.65 (moderate relevance)")
print("Recommended thresholds:")
print("  - 0.80+: Very high similarity")
print("  - 0.70-0.80: Good match")
print("  - 0.60-0.70: Moderate match")
print("  - < 0.60: Low relevance (filtered out)")