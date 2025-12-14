import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import hotel assistant modules
from hotel_assistant.database.neo4j_connection import Neo4jConnection
from hotel_assistant.database.query_executor import select_and_execute_query
from hotel_assistant.nlp.intent_classifier import IntentClassifier
from hotel_assistant.nlp.entity_extractor import extract_entities
from hotel_assistant.nlp.embeddings import semantic_search_mpnet
from hotel_assistant.llm.llm_layer import llm_layer
from hotel_assistant.config import (
    DEFAULT_TOP_K,
    DEFAULT_SIMILARITY_THRESHOLD,
    AVAILABLE_MODELS,
    INTENT_TYPES
)

# Page configuration
st.set_page_config(
    page_title="Hotel Assistant",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .context-box {
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        background-color: #e8f4f8;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
    .answer-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #e8f5e9;
        margin: 1rem 0;
    }
    .metadata-box {
        padding: 0.8rem;
        border-radius: 5px;
        background-color: #fff3e0;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'conn' not in st.session_state:
    st.session_state.conn = None
if 'intent_classifier' not in st.session_state:
    st.session_state.intent_classifier = None

# Predefined example questions
EXAMPLE_QUESTIONS = {
    "LIST_HOTELS": [
        "Show me hotels in Paris",
        "List 5-star hotels",
        "Find hotels in Egypt"
    ],
    "RECOMMEND_HOTEL": [
        "Recommend hotels in Cairo with good cleanliness",
        "Suggest a family-friendly hotel in Dubai",
        "Best hotels for business travelers in Tokyo"
    ],
    "DESCRIBE_HOTEL": [
        "Tell me about Nile Grandeur",
        "Describe The Azure Tower",
        "What are the facilities at Hilton Cairo?"
    ],
    "COMPARE_HOTELS": [
        "Compare The Azure Tower and Nile Grandeur",
        "Compare Hilton vs Marriott for families",
        "Which is better: Hotel A or Hotel B for cleanliness?"
    ],
    "CHECK_VISA": [
        "Do I need a visa for Turkey?",
        "Visa requirements from Egypt to France",
        "Do Americans need a visa for Japan?"
    ]
}

def initialize_connections():
    """Initialize database and classifier connections"""
    if st.session_state.conn is None:
        try:
            st.session_state.conn = Neo4jConnection()
            st.session_state.intent_classifier = IntentClassifier()
            return True
        except Exception as e:
            st.error(f"Failed to initialize connections: {str(e)}")
            return False
    return True

def process_query(user_query, use_rag=True, model="gpt-4o-mini"):
    """Process user query through the RAG pipeline"""
    try:
        # Step 1: Classify intent
        with st.spinner("Classifying intent..."):
            intent = st.session_state.intent_classifier.classify(user_query)

        # Step 2: Extract entities
        with st.spinner("Extracting entities..."):
            entities = extract_entities(user_query, intent)

        # Step 3: Execute Cypher query (KG)
        with st.spinner("Querying knowledge graph..."):
            cypher_results = select_and_execute_query(
                st.session_state.conn,
                intent,
                entities
            )

        # Step 4: Semantic search (RAG) - optional
        embedding_results = []
        if use_rag:
            with st.spinner("Performing semantic search..."):
                embedding_results = semantic_search_mpnet(
                    user_query,
                    top_k=DEFAULT_TOP_K,
                    threshold=DEFAULT_SIMILARITY_THRESHOLD
                )

        # Step 5: Generate LLM response
        with st.spinner("Generating response..."):
            llm_result = llm_layer(
                user_query=user_query,
                intent=intent,
                cypher_output=cypher_results,
                embedding_output=embedding_results if use_rag else None,
                model=model
            )

        return {
            'success': True,
            'intent': intent,
            'entities': entities,
            'cypher_results': cypher_results,
            'embedding_results': embedding_results,
            'llm_response': llm_result
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def display_results(result):
    """Display query results in a structured format"""
    if not result['success']:
        st.error(f"Error: {result['error']}")
        return

    # Create columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        # Intent and Entities
        st.markdown("### 📊 Query Analysis")
        st.markdown(f"**Intent:** `{result['intent']}`")
        st.markdown(f"**Entities:** `{result['entities']}`")

        # KG Results (Context)
        st.markdown("### 🗄️ Knowledge Graph Results")
        if result['cypher_results']:
            st.markdown(f"**{len(result['cypher_results'])} results** from Cypher query:")
            with st.expander("View KG Context", expanded=False):
                st.json(result['cypher_results'])
        else:
            st.info("No results from knowledge graph")

        # RAG Results
        if result['embedding_results']:
            st.markdown("### 🔍 Semantic Search Results")
            st.markdown(f"**{len(result['embedding_results'])} reviews** found:")
            with st.expander("View RAG Context", expanded=False):
                for i, review in enumerate(result['embedding_results'][:3], 1):
                    st.markdown(f"**{i}. {review.get('hotel_name', 'N/A')}** (Score: {review.get('score', 0):.2f})")
                    st.caption(f"{review.get('review_text', '')[:200]}...")
                    st.markdown("---")

    with col2:
        # LLM Response
        st.markdown("### 🤖 Assistant Response")
        llm_data = result['llm_response']

        if llm_data['success']:
            # Display the answer
            st.markdown(f"""
            <div class="answer-box">
            {llm_data['response']}
            </div>
            """, unsafe_allow_html=True)

            # Metadata
            with st.expander("Response Metadata"):
                metadata = llm_data['metadata']
                st.markdown(f"""
                - **Model:** {metadata.get('model', 'N/A')}
                - **Tokens Used:** {metadata.get('tokens_used', 0)}
                - **KG Results:** {metadata.get('cypher_count', 0)}
                - **Embedding Results:** {metadata.get('embedding_count', 0)}
                """)
        else:
            st.error(f"LLM Error: {llm_data.get('error', 'Unknown error')}")

def main():
    """Main Streamlit application"""

    # Header
    st.markdown('<div class="main-header">🏨 Hotel Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Hotel Recommendation System with Knowledge Graph & RAG</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # Model selection
        selected_model = st.selectbox(
            "LLM Model",
            AVAILABLE_MODELS,
            index=0,
            help="Select the OpenAI model for response generation"
        )

        # RAG toggle
        use_rag = st.checkbox(
            "Enable RAG (Semantic Search)",
            value=True,
            help="Include review embeddings in context"
        )

        st.markdown("---")

        # Example questions
        st.markdown("## 💡 Example Questions")
        selected_intent = st.selectbox("Select Task Type", list(EXAMPLE_QUESTIONS.keys()))

        example_question = st.radio(
            "Quick Questions:",
            EXAMPLE_QUESTIONS[selected_intent],
            key="example_selector"
        )

        if st.button("Use This Question", use_container_width=True):
            st.session_state.selected_question = example_question

        st.markdown("---")

        # System status
        st.markdown("## 📡 System Status")
        if st.session_state.conn:
            st.success("✓ Connected to Neo4j")
            st.success("✓ Intent Classifier Ready")
        else:
            st.warning("⚠ Not connected")

    # Initialize connections
    if not initialize_connections():
        st.stop()

    # Main query input
    st.markdown("## 🔎 Ask Your Question")

    # Use selected question or let user type
    default_query = st.session_state.get('selected_question', '')
    user_query = st.text_input(
        "Enter your question or select from examples:",
        value=default_query,
        placeholder="e.g., Recommend hotels in Cairo with good cleanliness",
        key="user_query_input"
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        submit_button = st.button("🚀 Submit", use_container_width=True, type="primary")
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)

    if clear_button:
        st.session_state.selected_question = ""
        st.rerun()

    # Process query
    if submit_button and user_query:
        st.markdown("---")

        # Process and display results
        result = process_query(user_query, use_rag=use_rag, model=selected_model)

        # Save to history
        st.session_state.conversation_history.append({
            'query': user_query,
            'result': result
        })

        # Display results
        display_results(result)

        st.markdown("---")

    # Conversation history
    if st.session_state.conversation_history:
        with st.expander(f"📜 Conversation History ({len(st.session_state.conversation_history)} queries)"):
            for i, conv in enumerate(reversed(st.session_state.conversation_history), 1):
                st.markdown(f"**Q{i}:** {conv['query']}")
                if conv['result']['success']:
                    st.caption(f"Intent: {conv['result']['intent']}")
                st.markdown("---")

if __name__ == "__main__":
    main()
