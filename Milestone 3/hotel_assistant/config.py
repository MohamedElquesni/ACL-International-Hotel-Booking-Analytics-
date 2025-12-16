"""Configuration File for Hotel Assistant"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Neo4j Configuration
NEO4J_CONFIG_PATH = os.getenv("NEO4J_CONFIG_PATH", "KnowledgeGraph/config.txt")

# Model Settings
DEFAULT_LLM_MODEL = "gpt-4o-mini"
INTENT_CLASSIFICATION_MODEL = "gpt-4o-mini"
ENTITY_EXTRACTION_MODEL = "gpt-4o-mini"

# Embedding Models
EMBEDDING_MODEL_MINILM = "all-MiniLM-L6-v2"
EMBEDDING_MODEL_MPNET = "all-mpnet-base-v2"

# Available Embedding Models for UI Selection
AVAILABLE_EMBEDDING_MODELS = {
    "MiniLM (Faster)": "minilm",
    "MPNet (More Accurate)": "mpnet"
}

# Search Settings
DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.65

# LLM Settings
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 1000

# Available Models for Comparison
AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]

# Intent Types
INTENT_TYPES = [
    "LIST_HOTELS",
    "RECOMMEND_HOTEL",
    "DESCRIBE_HOTEL",
    "COMPARE_HOTELS",
    "CHECK_VISA"
]

# Aspect Types
ASPECT_TYPES = [
    "cleanliness",
    "comfort",
    "facilities",
    "location",
    "staff",
    "value_for_money"
]
