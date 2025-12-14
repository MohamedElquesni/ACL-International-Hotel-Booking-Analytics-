"""Model Comparison Utilities"""
from typing import List, Dict, Any
from .llm_layer import llm_layer

def compare_models(
    user_query: str,
    intent: str,
    cypher_output: List[Dict],
    embedding_output: Optional[List[Dict]] = None,
    models: List[str] = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
) -> Dict[str, Any]:
    """Compare multiple models on the same query."""
    
    results = {}
    
    print(f"\\nComparing {len(models)} models on query: '{user_query}'")
    print("=" * 80)
    
    for model in models:
        print(f"\\nTesting {model}...")
        result = llm_layer(
            user_query=user_query,
            intent=intent,
            cypher_output=cypher_output,
            embedding_output=embedding_output,
            model=model
        )
        results[model] = result
        
        if result['success']:
            print(f"✓ Generated {len(result['response'])} chars, {result['metadata']['tokens_used']} tokens")
        else:
            print(f"✗ Error: {result['error']}")
    
    return {
        'query': user_query,
        'intent': intent,
        'model_results': results,
        'comparison': {
            'tokens_used': {m: results[m]['metadata']['tokens_used'] for m in models if results[m]['success']},
            'response_lengths': {m: len(results[m]['response']) for m in models if results[m]['success']}
        }
    }

print("compare_models function defined")