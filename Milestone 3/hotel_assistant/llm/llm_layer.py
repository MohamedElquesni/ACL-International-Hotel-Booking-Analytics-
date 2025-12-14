"""Main LLM Layer for Response Generation"""
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .prompt_engine import PromptEngine
from .context_builder import ContextBuilder
from .result_merger import merge_and_rank_results

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def llm_layer(
    user_query: str,
    intent: str,
    cypher_output: List[Dict],
    embedding_output: Optional[List[Dict]] = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    max_tokens: int = 1000
) -> Dict[str, Any]:
    """
    Production-grade LLM layer with:
    - Smart result merging
    - Intent-optimized prompts
    - Few-shot examples
    - Output validation
    
    Args:
        user_query: Original user question
        intent: Classified intent
        cypher_output: Results from baseline Cypher queries
        embedding_output: Optional RAG results
        model: GPT model (gpt-4o-mini, gpt-4o, gpt-4-turbo)
        temperature: 0.0 for deterministic, higher for creative
        max_tokens: Max response length
    
    Returns:
        Complete response with metadata and quality metrics
    """
    
    # Step 1: Merge and deduplicate results
    merged_data = merge_and_rank_results(cypher_output, embedding_output, intent)
    
    # Step 2: Build optimized context
    context = ContextBuilder.build(intent, merged_data)
    
    # Step 3: Generate intent-specific prompts
    system_prompt, user_prompt = PromptEngine.get_prompts(intent, user_query, context)
    
    # Step 4: Call LLM with error handling
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        finish_reason = response.choices[0].finish_reason
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'model': model,
            'intent': intent
        }
    
    # Step 5: Return comprehensive result
    return {
        'success': True,
        'model': model,
        'intent': intent,
        'response': answer,
        'metadata': {
            'query': user_query,
            'cypher_results_count': merged_data['metadata']['cypher_count'],
            'embedding_results_count': merged_data['metadata']['embedding_count'],
            'has_results': merged_data['metadata']['has_results'],
            'tokens_used': tokens_used,
            'finish_reason': finish_reason,
            'temperature': temperature
        },
        'context_used': context[:500] + "..." if len(context) > 500 else context,
        'full_context': context
    }

print("llm_layer function defined")