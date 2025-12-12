# Milestone 3: Graph-RAG Hotel Travel Assistant

**Theme:** Hotel Recommendation + Visa Assistant
**Approach:** Hybrid (Cypher Queries + Neo4j Vector Index + LLM)
**Status:** Parts 1, 2.a, 1.c, 2.b Complete ✅ | Part 3 (LLM Layer) Next ➡️

---

## 🎯 Project Overview

Building an end-to-end Graph-RAG system that:
1. Classifies user intent (5 intents)
2. Extracts entities from queries (NER)
3. Retrieves relevant data from Neo4j Knowledge Graph
4. Uses LLM to generate natural language responses
5. Provides Streamlit UI for interaction

---

## ✅ Completed Components

### Part 1: Input Preprocessing

#### 1.a Intent Classification ✅
**Location:** `Milestone 3.ipynb` (Cells 2-9)

**Implementation:**
- LLM-based classifier using OpenAI GPT-4o-mini
- 5 action-based intents:
  - `LIST_HOTELS` - Find hotels matching filters
  - `RECOMMEND_HOTEL` - Get personalized suggestions
  - `DESCRIBE_HOTEL` - Get info about specific hotel
  - `COMPARE_HOTELS` - Compare 2+ hotels
  - `CHECK_VISA` - Check visa requirements

**Performance:** 100% accuracy on 28 test cases

**Key Design Decision:**
- Uses LLM instead of rule-based for flexibility with natural language variations
- Explicit tie-breaking rules in prompt to handle ambiguous queries

---

#### 1.b Entity Extraction ✅
**Location:** `Milestone 3.ipynb` (Cells 10-17)

**Implementation:**
- LLM-based NER using same GPT-4o-mini model
- Intent-specific schemas ensure only relevant entities extracted
- Three-stage approach: LLM extraction → Schema enforcement → Normalization

**Entity Schemas by Intent:**

| Intent | Extracted Entities |
|--------|-------------------|
| `LIST_HOTELS` | city, country, star_rating |
| `RECOMMEND_HOTEL` | city, country, traveller_type, age_group, user_gender, star_rating, aspects |
| `DESCRIBE_HOTEL` | hotel_name, aspects |
| `COMPARE_HOTELS` | hotel1, hotel2, traveller_type, aspects |
| `CHECK_VISA` | from_country, to_country |

**Allowed Aspects:**
- cleanliness, comfort, facilities, location, staff, value_for_money

**Critical Behavioral Rule:**
- Vague quality words ("good", "best", "nice") do **NOT** trigger aspect extraction
- Aspects extracted **ONLY** if explicitly mentioned (e.g., "clean rooms" → cleanliness)

**Test Results:** All 3 critical test cases passed
- ✅ Explicit aspects: "good location and clean rooms" → extracted `location`, `cleanliness`
- ✅ Vague words: "good hotels" → aspects=None (correct!)
- ✅ Comparison: "staff quality and comfort" → extracted `staff`, `comfort`

---

## 📋 Next Steps

### Part 2.a: Baseline Cypher Queries ➡️ NEXT
**Status:** Not started

**Requirements:**
- [ ] Create at least 10 Cypher query templates
- [ ] Map intent+entities → appropriate queries
- [ ] Test retrieval from Neo4j KG
- [ ] Handle each of the 5 intents with multiple query variations

**Example Queries Needed:**
1. LIST_HOTELS: Filter by city, country, star rating
2. RECOMMEND_HOTEL: Filter by demographics + aspect scores
3. DESCRIBE_HOTEL: Get full hotel details + reviews
4. COMPARE_HOTELS: Get side-by-side comparison data
5. CHECK_VISA: Query visa requirements between countries

---

### Part 1.c: Input Embedding ✅
**Status:** Complete
**Location:** `Milestone 3.ipynb` (After Part 1.b)

**Implementation:**
- Using sentence-transformers library
- Model: `all-MiniLM-L6-v2` (fast, lightweight, 384-dim embeddings)
- Function: `embed_query(query)` converts text to embedding vectors
- Will be used for semantic similarity search in Part 2.b

---

### Part 2.b: Embeddings (RAG) ✅ Complete
**Status:** Fully implemented with Neo4j vector index and 2-model comparison
**Location:** `Milestone 3.ipynb` (After Part 2.a)

**Approach:** Feature Vector Embeddings (Option 2)
- Combine hotel properties into natural language (synthetic reviews)
- Embed combined representations with TWO models for comparison

**Completed:**
- ✅ Step 1: Extracted 1000 hotel-traveller combinations from Neo4j
- ✅ Step 2: Natural review text generator with GPT-4o-mini
- ✅ Step 3: Batch generator (1000 reviews with rate limiting)
- ✅ Step 4: Saved reviews to `synthetic_reviews.json`
- ✅ Step 5: Quality verification (word count, diversity, traveller types)
- ✅ Step 6: Created embeddings with **TWO models** for comparison
- ✅ Step 7: Stored in **Neo4j vector index** (not FAISS)
- ✅ Step 8: Created vector indices for both models
- ✅ Step 9: Implemented semantic search for both models
- ✅ Step 10: Quantitative comparison (speed, relevance scores)

**Two Embedding Models Compared:**
1. **all-MiniLM-L6-v2** (384 dimensions) - Fast, lightweight
2. **all-mpnet-base-v2** (768 dimensions) - Higher quality

**Comparison Metrics:**
- Search speed (query time)
- Relevance scores (cosine similarity)
- Top-k match quality

---

### Part 3: LLM Layer
**Status:** Not started

**Requirements:**
- [ ] Combine KG results (baseline + embeddings)
- [ ] Structure prompt: Context + Persona + Task
- [ ] Compare 3+ LLM models (quantitative + qualitative)
- [ ] Evaluate: accuracy, response time, cost, quality

---

### Part 4: UI (Streamlit)
**Status:** Not started

**Requirements:**
- [ ] User can input queries
- [ ] Display KG-retrieved context
- [ ] Display final LLM answer
- [ ] Optional: Show Cypher queries, graph visualization

---

## 🗂️ Project Structure

```
Milestone 3/
├── Milestone 3.ipynb           # Main implementation notebook
├── KnowledgeGraph/
│   ├── config.txt              # Neo4j connection credentials
│   ├── Create_kg.py            # Graph creation script
│   ├── verify_schema.py        # Schema validation
│   ├── Dataset/                # CSV files (hotels, users, reviews, visa)
│   └── README.md               # KG schema documentation
├── Description/
│   └── Milestone 3.pdf         # Project specification
├── Notes/
│   └── TA_Notes_Clean_Structured.docx
└── Required Labs/
    ├── Lab 6.pdf
    ├── Lab 7.pdf
    └── Lab 8.pdf
```

---

## 🔧 Knowledge Graph Schema

### Nodes
- **Hotel**: hotel_id, name, star_rating, city, country, 6 base scores (cleanliness, comfort, facilities, location, staff, value_for_money), average_reviews_score
- **Traveller**: user_id, age (age_group), type (traveller_type), gender
- **Review**: review_id, text, date, score_overall, 6 aspect scores
- **City**: name
- **Country**: name

### Relationships
```
Traveller -[:WROTE]-> Review
Review -[:REVIEWED]-> Hotel
Hotel -[:LOCATED_IN]-> City
City -[:LOCATED_IN]-> Country
Traveller -[:FROM_COUNTRY]-> Country
Country -[:NEEDS_VISA {visa_type}]-> Country
```

---

## 🚀 How to Run

### Prerequisites
```bash
# Install dependencies
pip install openai python-dotenv neo4j fuzzywuzzy python-Levenshtein
```

### Environment Setup
Create `.env` file with:
```
OPENAI_API_KEY=your_key_here
```

### Run Notebook
```bash
jupyter notebook "Milestone 3/Milestone 3.ipynb"
```

### Test Components

**Test Intent Classification:**
```python
classifier = IntentClassifier()
intent = classifier.classify("Recommend hotels for families in Dubai")
# Output: "RECOMMEND_HOTEL"
```

**Test Entity Extraction:**
```python
entities = extract_entities(
    "Recommend hotels for families in Dubai with good location",
    "RECOMMEND_HOTEL"
)
# Output: {"city": "Dubai", "traveller_type": "family", "aspects": ["location"], ...}
```

---

## 🎨 Design Decisions

### Why LLM-based NER instead of spaCy/BERT?
- Hotel domain has flexible entity expressions
- LLM understands context better ("families" → traveller_type)
- Can apply complex rules (vague words don't trigger aspects)
- Same model as intent classifier (consistent behavior)

### Why Skip Part 1.c (Input Embedding) for Now?
- Not needed for baseline (Part 2.a)
- Only required if implementing Part 2.b (embeddings)
- Baseline Cypher queries work without embeddings
- Can add later as enhancement

### Why Generate Synthetic Reviews?
- Original reviews may be short/incomplete
- Synthetic reviews combine structured data + text
- Better for semantic similarity search
- Grounded in actual data (no hallucination)

---

## 📊 Implementation Progress

| Part | Component | Status | Location |
|------|-----------|--------|----------|
| 1.a | Intent Classification | ✅ Complete | Cells 2-9 |
| 1.b | Entity Extraction | ✅ Complete | Cells 10-17 |
| 1.c | Input Embedding | ✅ Complete | After 1.b |
| 2.a | Baseline Cypher | ✅ Complete + Hardened | Cells 18-24 |
| 2.b | Synthetic Reviews | ✅ Complete (1000 reviews) | Steps 1-5 |
| 2.b | Neo4j Vector Index | ✅ Complete (2 models) | Steps 6-10 |
| 3 | LLM Layer | ➡️ Next | - |
| 4 | UI (Streamlit) | 📝 Planned | - |

---

## 🛡️ Part 2.a: Critical Fixes Applied

**All 8 critical issues resolved** (2025-12-12):

1. ✅ **Relationship Direction Consistency**: All queries use canonical directions
   - `(Traveller)-[:WROTE]->(Review)-[:REVIEWED]->(Hotel)`
   - `(Hotel)-[:LOCATED_IN]->(City)-[:LOCATED_IN]->(Country)`

2. ✅ **Executor Bug**: Fixed empty params dict `{}` rejection
   - Changed `if not query or not params:` → `if not query:`

3. ✅ **NULL Handling**: Added WHERE filters and coalesce() in aggregations
   - `WHERE t.type IS NOT NULL` before collect()
   - `ORDER BY coalesce(demographic_rating, 0)`

4. ✅ **Cypher Injection Prevention**: Aspect whitelist validation
   - `validate_aspects()` filters all user input
   - Fallback to non-aspect query if no valid aspects

5. ✅ **Rating Scale Fixed**: Corrected 0-10 scale thresholds
   - Changed from `>= 4.0` to `>= 8.0` (MIN_RATING_THRESHOLD)

6. ✅ **Visa Path NULL Safety**: Protected nodes(path) with CASE
   - Safe route_length handling with fallback `999`

7. ✅ **Router Logic**: Removed unsupported country-only path
   - LIST_HOTELS now correctly requires city only

8. ✅ **Strengthened Graph-Aware**: Enhanced Q2 and Q3 with multi-hop traversals
   - Q2: Added Traveller demographic grouping
   - Q3: Added co-visitation patterns from origin country

**Implementation**: 10 graph-aware query templates, safe routing, defensive execution

---

## 🐛 Known Issues / TODOs

- [ ] Need to handle fuzzy matching for hotel/city names (Part 3/4)
- [ ] Consider adding synonym handling for traveller types (Enhancement)
- [ ] Decide on embedding models if implementing 2.b

---

## 📚 Key Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Neo4j Vector Index - LangChain](https://python.langchain.com/docs/integrations/vectorstores/neo4jvector)
- [Sentence Transformers](https://www.sbert.net/)
- [LangChain Graph RAG Tutorial](https://python.langchain.com/docs/use_cases/graph/)

---

## 👥 Team Notes

**Last Updated:** 2025-12-12

**Current Focus:** Parts 1.c, 2.a Complete ✅ | Part 2.b Synthetic Reviews Generated ✅ | Next: Embeddings Pipeline ➡️

**Recent Work:**
- ✅ Implemented Part 1.c: Input embedding with sentence-transformers (all-MiniLM-L6-v2)
- ✅ Implemented Part 2.b synthetic review generation:
  - Extracted 1000 hotel-traveller combinations from Neo4j
  - Generated natural, human-like reviews (80-150 words each)
  - Diversified by traveller type (family, couple, solo, business, group)
  - Varied tones (enthusiastic, satisfied, balanced, critical)
  - Saved to `synthetic_reviews.json`
- ✅ Part 2.a: 10 graph-aware Cypher query templates, all hardened against injection and NULL errors

**Reminder:** Deadline is December 15th at 23:59
