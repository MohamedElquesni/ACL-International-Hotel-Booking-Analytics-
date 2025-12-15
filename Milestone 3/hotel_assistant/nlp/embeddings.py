"""Semantic Search using Vector Embeddings"""
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from ..database.neo4j_connection import Neo4jConnection

_embedder_minilm = None
_embedder_mpnet = None
_conn_rag = None

def get_embedder_minilm():
    """Lazy load MiniLM embedder"""
    global _embedder_minilm
    if _embedder_minilm is None:
        _embedder_minilm = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedder_minilm

def get_embedder_mpnet():
    """Lazy load MPNet embedder"""
    global _embedder_mpnet
    if _embedder_mpnet is None:
        _embedder_mpnet = SentenceTransformer('all-mpnet-base-v2')
    return _embedder_mpnet

def get_conn_rag():
    """Lazy load Neo4j connection for RAG"""
    global _conn_rag
    if _conn_rag is None:
        _conn_rag = Neo4jConnection()
    return _conn_rag

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
    embedder = get_embedder_minilm()
    query_embedding = embedder.encode([query], convert_to_numpy=True)[0].tolist()

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

    conn = get_conn_rag()
    results = conn.execute_query(search_query, {
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
    embedder = get_embedder_mpnet()
    query_embedding = embedder.encode([query], convert_to_numpy=True)[0].tolist()

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

    conn = get_conn_rag()
    results = conn.execute_query(search_query, {
        'query_embedding': query_embedding,
        'top_k': top_k
    })

    # Filter by similarity threshold
    filtered_results = [r for r in results if r['score'] >= threshold]

    return filtered_results
