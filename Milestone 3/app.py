import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Import only what's needed at startup
from hotel_assistant.config import DEFAULT_TOP_K, DEFAULT_SIMILARITY_THRESHOLD, AVAILABLE_MODELS

# Cached resource loaders
@st.cache_resource
def get_neo4j_connection():
    from hotel_assistant.database.neo4j_connection import Neo4jConnection
    return Neo4jConnection()

@st.cache_resource
def get_intent_classifier():
    from hotel_assistant.nlp.intent_classifier import IntentClassifier
    return IntentClassifier()

@st.cache_resource
def get_heavy_modules():
    """Load and cache heavy modules (embeddings, etc.)"""
    from hotel_assistant.database.query_executor import select_and_execute_query
    from hotel_assistant.nlp.entity_extractor import extract_entities
    from hotel_assistant.nlp.embeddings import semantic_search_mpnet
    from hotel_assistant.llm.llm_layer import llm_layer

    return {
        'select_and_execute_query': select_and_execute_query,
        'extract_entities': extract_entities,
        'semantic_search_mpnet': semantic_search_mpnet,
        'llm_layer': llm_layer
    }

st.set_page_config(page_title="Hotel Assistant", page_icon="🏨", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.2rem; color: #7f8c8d; text-align: center; margin-bottom: 2rem; }
    .answer-box { padding: 1.5rem; border-radius: 8px; background-color: #f8f9fa; border-left: 4px solid #3498db; margin: 1rem 0; color: #2c3e50; font-size: 1.05rem; line-height: 1.6; }
    .context-box { padding: 1rem; border-left: 4px solid #95a5a6; background-color: #ecf0f1; margin: 1rem 0; font-family: monospace; font-size: 0.9rem; color: #2c3e50; }
</style>
""", unsafe_allow_html=True)

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'conn' not in st.session_state:
    st.session_state.conn = None
if 'intent_classifier' not in st.session_state:
    st.session_state.intent_classifier = None

EXAMPLE_QUESTIONS = {
    "LIST_HOTELS": ["Show me hotels in Paris", "List 5-star hotels", "Find hotels in Egypt"],
    "RECOMMEND_HOTEL": ["Recommend hotels in Cairo with good cleanliness", "Suggest a family-friendly hotel in Dubai"],
    "DESCRIBE_HOTEL": ["Tell me about Nile Grandeur", "Describe The Azure Tower"],
    "COMPARE_HOTELS": ["Compare The Azure Tower and Nile Grandeur", "Compare Hilton vs Marriott for families"],
    "CHECK_VISA": ["Do I need a visa for Turkey?", "Visa requirements from Egypt to France"]
}

def initialize_connections():
    if st.session_state.conn is None:
        try:
            st.session_state.conn = get_neo4j_connection()
            st.session_state.intent_classifier = get_intent_classifier()
            return True
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            return False
    return True

def process_query(user_query, use_rag=True, model="gpt-4o-mini"):
    try:
        # Load heavy modules (cached after first load)
        # Show special message on first load
        if 'models_loaded' not in st.session_state:
            with st.spinner("🔄 Loading AI models (one-time setup, ~30 seconds)..."):
                modules = get_heavy_modules()
                st.session_state.models_loaded = True
        else:
            modules = get_heavy_modules()

        select_and_execute_query = modules['select_and_execute_query']
        extract_entities = modules['extract_entities']
        semantic_search_mpnet = modules['semantic_search_mpnet']
        llm_layer = modules['llm_layer']

        with st.spinner("🔍 Processing your query..."):
            intent = st.session_state.intent_classifier.classify(user_query)
            entities = extract_entities(user_query, intent)
            cypher_results = select_and_execute_query(st.session_state.conn, intent, entities)

            embedding_results = []
            if use_rag:
                embedding_results = semantic_search_mpnet(user_query, top_k=DEFAULT_TOP_K, threshold=DEFAULT_SIMILARITY_THRESHOLD)

            llm_result = llm_layer(user_query, intent, cypher_results, embedding_results if use_rag else None, model=model)

        return {
            'success': True,
            'intent': intent,
            'entities': entities,
            'cypher_results': cypher_results,
            'embedding_results': embedding_results,
            'llm_response': llm_result
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def display_results(result):
    if not result['success']:
        st.error(f"Error: {result['error']}")
        return

    st.markdown("### Assistant Response")
    llm_data = result['llm_response']

    if llm_data['success']:
        st.markdown(f'<div class="answer-box">{llm_data["response"]}</div>', unsafe_allow_html=True)
    else:
        st.error(f"LLM Error: {llm_data.get('error', 'Unknown')}")

    st.markdown("---")

    with st.expander("Query Details", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Intent**")
            st.code(result['intent'])
            st.markdown("**Entities**")
            st.json(result['entities'])

        with col2:
            st.markdown("**Knowledge Graph Results**")
            if result['cypher_results']:
                st.info(f"{len(result['cypher_results'])} results")
                with st.expander("View KG Data"):
                    st.json(result['cypher_results'])
            else:
                st.warning("No KG results")

        with col3:
            st.markdown("**Semantic Search Results**")
            if result['embedding_results']:
                st.info(f"{len(result['embedding_results'])} reviews")
                with st.expander("View RAG Data"):
                    for i, review in enumerate(result['embedding_results'][:3], 1):
                        st.markdown(f"**{i}. {review.get('hotel_name', 'N/A')}** (Score: {review.get('score', 0):.2f})")
                        st.caption(f"{review.get('review_text', '')[:200]}...")
                        if i < 3:
                            st.markdown("---")
            else:
                st.warning("No RAG results")

        metadata = llm_data.get('metadata', {})
        st.markdown("---")
        st.caption(f"Model: {metadata.get('model', 'N/A')} | Tokens: {metadata.get('tokens_used', 0)} | KG: {metadata.get('cypher_count', 0)} | RAG: {metadata.get('embedding_count', 0)}")

def main():
    st.markdown('<div class="main-header">🏨 Hotel Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Hotel Recommendation System</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Settings")
        selected_model = st.selectbox("LLM Model", AVAILABLE_MODELS, index=0)
        use_rag = st.checkbox("Enable RAG", value=True)
        st.markdown("---")

        st.markdown("## Example Questions")
        all_examples = sum(EXAMPLE_QUESTIONS.values(), [])
        example_question = st.selectbox("Select an example", all_examples, label_visibility="collapsed")

        if st.button("Use This Question", use_container_width=True):
            st.session_state.selected_question = example_question

        st.markdown("---")
        st.markdown("## Status")
        if st.session_state.conn:
            st.success("Connected")
        else:
            st.warning("Not connected")

    if not initialize_connections():
        st.stop()

    default_query = st.session_state.get('selected_question', '')
    user_query = st.text_input("Enter your question:", value=default_query, placeholder="e.g., Recommend hotels in Cairo")

    left, center1, center2, right = st.columns([3, 1, 1, 3])
    with center1:
        submit_button = st.button("Submit", use_container_width=True, type="primary")
    with center2:
        clear_button = st.button("Clear", use_container_width=True)

    if clear_button:
        st.session_state.selected_question = ""
        st.rerun()

    if submit_button and user_query:
        st.markdown("---")
        result = process_query(user_query, use_rag=use_rag, model=selected_model)
        st.session_state.conversation_history.append({'query': user_query, 'result': result})
        display_results(result)
        st.markdown("---")

    if st.session_state.conversation_history:
        with st.expander(f"History ({len(st.session_state.conversation_history)} queries)"):
            for i, conv in enumerate(reversed(st.session_state.conversation_history), 1):
                st.markdown(f"**Q{i}:** {conv['query']}")
                if conv['result']['success']:
                    st.caption(f"Intent: {conv['result']['intent']}")
                st.markdown("---")

if __name__ == "__main__":
    main()