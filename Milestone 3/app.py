import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Import only what's needed at startup
from hotel_assistant.config import DEFAULT_TOP_K, DEFAULT_SIMILARITY_THRESHOLD, AVAILABLE_MODELS, AVAILABLE_EMBEDDING_MODELS

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
    from hotel_assistant.nlp.embeddings import semantic_search_mpnet, semantic_search_minilm
    from hotel_assistant.llm.llm_layer import llm_layer

    return {
        'select_and_execute_query': select_and_execute_query,
        'extract_entities': extract_entities,
        'semantic_search_mpnet': semantic_search_mpnet,
        'semantic_search_minilm': semantic_search_minilm,
        'llm_layer': llm_layer
    }

st.set_page_config(page_title="Hotel Assistant", page_icon="🏨", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Background and Page Setup */
    .main {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }

    .stMainBlockContainer  {
        display : flex !important;
        align-items: center !important;
        justify-content: center !important;
        width : 100% !important;
    }
    
    /* Main Content Wrapper - Mobile Frame */
    .main .block-container {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 2rem 1rem !important;
    }
    
    /* Chat Container - The vertical block with all chat content */
    .main .block-container > div > .stVerticalBlock {
        width: 500px !important;
        max-width: 500px !important;
        background: #e5ddd5;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        padding: 1rem;
    }
    
    /* Chat Header */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    .chat-subtitle {
        font-size: 0.9rem;
        opacity: 0.95;
        margin-top: 5px;
    }
    
    /* Chat Messages Container */
    .chat-messages {
        min-height: 300px;
        max-height: 500px;
        overflow-y: auto;
        padding: 10px 5px;
        margin-bottom: 10px;
    }
    
    /* User Message (Outgoing - Right) */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 5px 0;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 75%;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    /* Bot Message (Incoming - Left) */
    .bot-message {
        display: flex;
        justify-content: flex-start;
        margin: 5px 0;
    }
    
    .bot-bubble {
        background: white;
        color: #2c3e50;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* System/Info Message */
    .info-message {
        text-align: center;
        margin: 10px 0;
    }
    
    .info-bubble {
        display: inline-block;
        background: rgba(149, 165, 166, 0.2);
        color: #7f8c8d;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-style: italic;
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 0.7rem;
        color: #95a5a6;
        margin-top: 4px;
        text-align: right;
    }
    
    /* Details Badge */
    .details-badge {
        display: inline-block;
        background: rgba(52, 152, 219, 0.1);
        color: #3498db;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 0.75rem;
        margin-top: 8px;
        cursor: pointer;
        border: 1px solid rgba(52, 152, 219, 0.3);
    }
    
    /* Input Area Styling */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #2c3e50 !important;
        padding: 12px 18px !important;
        background: #2c3e50 !important;
        color: white !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
        background: #34495e !important;
    }
    
    .stButton > button {
        border-radius: 25px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.5);
        border-radius: 10px;
    }
    
    /* Custom override for emotion class */
    .st-emotion-cache-tn0cau {
        /* Add your custom styles here */
        /* Example: */
        /* background: #f0f0f0 !important; */
        /* color: #333 !important; */
        /* padding: 10px !important; */
        width : 500px !important;
    }
</style>
""", unsafe_allow_html=True)

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'conn' not in st.session_state:
    st.session_state.conn = None
if 'intent_classifier' not in st.session_state:
    st.session_state.intent_classifier = None

EXAMPLE_QUESTIONS = {
    "LIST_HOTELS": ["Show me hotels in Paris", "List 5-star hotels", "Find hotels in Egypt" , "Show me hotels in Zanzibar"],
    "RECOMMEND_HOTEL": ["Recommend hotels in Cairo with good cleanliness", "Suggest a family-friendly hotel in Dubai"],
    "DESCRIBE_HOTEL": ["Tell me about Nile Grandeur", "Describe The Azure Tower"],
    "COMPARE_HOTELS": ["Compare The Azure Tower and Nile Grandeur", "Compare Hilton vs Marriott for families"],
    "CHECK_VISA": ["Do I need a visa for Turkey?", "Visa requirements from Egypt to France"]
}

def initialize_connections():
    if st.session_state.conn is None or st.session_state.intent_classifier is None:
        try:
            st.session_state.conn = get_neo4j_connection()
            st.session_state.intent_classifier = get_intent_classifier()
            return True
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            st.session_state.conn = None
            st.session_state.intent_classifier = None
            return False
    return True

def process_query(user_query, use_rag=True, model="gpt-4o-mini", embedding_model="mpnet"):
    try:
        # Ensure intent classifier is initialized
        if st.session_state.intent_classifier is None:
            return {'success': False, 'error': 'Intent classifier not initialized. Please refresh the page.'}

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
        llm_layer = modules['llm_layer']

        with st.spinner("🔍 Processing your query..."):
            intent = st.session_state.intent_classifier.classify(user_query)
            entities = extract_entities(user_query, intent)
            cypher_results = select_and_execute_query(st.session_state.conn, intent, entities)

            embedding_results = []
            if use_rag:
                # Select the appropriate embedding search function based on model choice
                if embedding_model == "minilm":
                    semantic_search = modules['semantic_search_minilm']
                else:
                    semantic_search = modules['semantic_search_mpnet']

                embedding_results = semantic_search(user_query, top_k=DEFAULT_TOP_K, threshold=DEFAULT_SIMILARITY_THRESHOLD)

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

def display_chat_message(message_type, content, show_details=False, result=None):
    """Display a single chat message in mobile chat style"""
    if message_type == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="user-bubble">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif message_type == "bot":
        st.markdown(f"""
        <div class="bot-message">
            <div class="bot-bubble">{content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_details and result:
            with st.expander("📊 Query Details", expanded=False):
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
                
                llm_data = result.get('llm_response', {})
                metadata = llm_data.get('metadata', {})
                st.markdown("---")
                st.caption(f"Tokens: {metadata.get('tokens_used', 0)}")
    
    elif message_type == "info":
        st.markdown(f"""
        <div class="info-message">
            <div class="info-bubble">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def display_results(result):
    """Display results in chat format"""
    if not result['success']:
        display_chat_message("bot", f"❌ Error: {result['error']}")
        return

    llm_data = result['llm_response']

    if llm_data['success']:
        display_chat_message("bot", llm_data["response"], show_details=True, result=result)
    else:
        display_chat_message("bot", f"❌ LLM Error: {llm_data.get('error', 'Unknown')}")

def main():
    # Sidebar Settings
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        selected_model = st.selectbox("LLM Model", AVAILABLE_MODELS, index=0)
        use_rag = st.checkbox("Enable RAG", value=True)

        # Embedding model selector (only shown when RAG is enabled)
        if use_rag:
            embedding_model_display = st.selectbox(
                "Embedding Model",
                list(AVAILABLE_EMBEDDING_MODELS.keys()),
                index=1  # Default to MPNet
            )
            embedding_model = AVAILABLE_EMBEDDING_MODELS[embedding_model_display]
        else:
            embedding_model = "mpnet"  # Default value when RAG is disabled

        st.markdown("---")

        st.markdown("## 💡 Example Questions")
        all_examples = sum(EXAMPLE_QUESTIONS.values(), [])
        example_question = st.selectbox("Select an example", all_examples, label_visibility="collapsed")

        if st.button("Use This Question", use_container_width=True):
            st.session_state.selected_question = example_question

        st.markdown("---")
        st.markdown("## 📊 Status")
        if st.session_state.conn:
            st.success("✅ Connected")
        else:
            st.warning("⚠️ Not connected")
        
        if st.session_state.conversation_history:
            st.info(f"💬 {len(st.session_state.conversation_history)} messages")

    if not initialize_connections():
        st.stop()

    # Create main chat container
    chat_container = st.container()
    
    with chat_container:
        # Chat Header
        st.markdown("""
        <div class="chat-header">
            <div class="chat-title">🏨 Hotel Assistant</div>
            <div class="chat-subtitle">AI-Powered Hotel Recommendations</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat Messages Area
        messages_container = st.container()
        with messages_container:
            st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
            
            # Display conversation history
            if not st.session_state.conversation_history:
                display_chat_message("info", "👋 Welcome! Ask me anything about hotels, recommendations, or visa requirements.")
            else:
                for conv in st.session_state.conversation_history:
                    # User message
                    display_chat_message("user", conv['query'])
                    
                    # Bot response
                    if conv['result']['success']:
                        llm_data = conv['result']['llm_response']
                        if llm_data['success']:
                            display_chat_message("bot", llm_data["response"], show_details=True, result=conv['result'])
                        else:
                            display_chat_message("bot", f"❌ Error: {llm_data.get('error', 'Unknown')}")
                    else:
                        display_chat_message("bot", f"❌ Error: {conv['result']['error']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Input Area (at bottom of chat frame)
        st.markdown("---")
        default_query = st.session_state.get('selected_question', '')
        user_query = st.text_input("Type your message...", value=default_query, placeholder="e.g., Recommend hotels in Cairo", label_visibility="collapsed")

        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            submit_button = st.button("Send", use_container_width=True, type="primary")
        with col3:
            clear_button = st.button("Clear", use_container_width=True)

    if clear_button:
        st.session_state.conversation_history = []
        st.session_state.selected_question = ""
        st.rerun()

    if submit_button and user_query:
        result = process_query(user_query, use_rag=use_rag, model=selected_model, embedding_model=embedding_model)
        st.session_state.conversation_history.append({'query': user_query, 'result': result})
        st.session_state.selected_question = ""  # Clear the input after sending
        st.rerun()

if __name__ == "__main__":
    main()