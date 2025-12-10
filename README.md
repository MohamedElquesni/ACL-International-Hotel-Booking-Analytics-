# ACL Project - Graph-RAG Travel Assistant

**Theme:** Hotel

## 📊 Project Progress

### Milestones Overview
```
Milestone 1: ████████████████████ 100% ✅ COMPLETED
Milestone 2: ████████████████████ 100% ✅ COMPLETED
Milestone 3: ░░░░░░░░░░░░░░░░░░░░   0% 🚧 IN PROGRESS
```

**Deadline: December 15, 2025 at 23:59**

### Task Options for Hotel Theme
- [ ] Booking and Visa Assistant
- [ ] Hotel Recommender System
- [ ] Custom Task: ________________________________

---

## ✅ Milestone 3 - Implementation Checklist

### 🔧 Part 1: Input Preprocessing

- [x] **Intent Classification**
  - [x] Implement intent classifier (rule-based, LLM-based, or hybrid)
  - [x] Classify what user wants to do (ask question, get recommendations, search entities)

- [x] **Entity Extraction**
  - [x] Set up Named Entity Recognition (NER)
  - [x] Extract Hotel theme entities: hotels, cities, countries, traveller types, demographics
  - [x] Use extracted entities to fill Cypher query parameters

- [ ] **Input Embedding** (only if using embeddings approach in Part 2b)
  - [ ] Choose embedding model
  - [ ] Convert user text input into vector representation for semantic similarity search

---

### 🗄️ Part 2: Graph Retrieval Layer

#### Experiment 1: Baseline (Cypher Queries)

- [ ] **Write At Least 10 Cypher Query Templates**
  - [ ] Query 1 (Hotel Search): Find hotels in [city] with rating > [X]
  - [ ] Query 2 (Review Retrieval): Get reviews for [hotel_name]
  - [ ] Query 3 (Amenity Filtering): Find hotels with [amenity] in [location]
  - [ ] Query 4 (Location-Based): Find all hotels in [country/city]
  - [ ] Query 5 (Visa Requirements): Get visa requirements for [country]
  - [ ] Query 6 (Price Range): Find hotels with price between [X] and [Y]
  - [ ] Query 7 (Traveller Type): Find hotels suitable for [traveller_type]
  - [ ] Query 8 (Top Rated): Get top-rated hotels in [location]
  - [ ] Query 9 (Nearby Hotels): Find hotels near [landmark/location]
  - [ ] Query 10 (Hotel Comparison): Compare features/ratings between 2+ hotels
  - [ ] Query 11 (Budget Hotels): Find cheapest hotels in [location]
  - [ ] Query 12 (Custom): ________________________________

- [ ] **Execute Queries to Retrieve Information**
  - [ ] Use Cypher queries to fetch nodes, relationships, and properties from KG
  - [ ] Pass extracted entities from input to query the KG and retrieve answers

#### Experiment 2: Embeddings

- [ ] **Choose ONE Embedding Approach**
  - [ ] Option A: Node Embeddings (use graph embedding techniques like Node2Vec, GraphSAGE, or text embeddings of node properties)
  - [ ] Option B: Feature Vector Embeddings (combine hotel name, location, amenities, rating, review text into single feature vector)

- [ ] **Experiment with Embedding Model 1**
  - [ ] Model name: ________________________________
  - [ ] Implement semantic similarity search using vector embeddings

- [ ] **Experiment with Embedding Model 2**
  - [ ] Model name: ________________________________
  - [ ] Implement semantic similarity search using vector embeddings

- [ ] **Compare the Two Embedding Models**
  - [ ] Document experiment results for both models
  - [ ] Show which performs better

---

### 🤖 Part 3: LLM Layer

- [ ] **Combine KG Results from Baseline and Embeddings**
  - [ ] Merge results from Cypher queries (baseline)
  - [ ] Merge results from embedding-based retrieval
  - [ ] Create unified context with retrieved nodes, relationships, and data
  - [ ] Remove duplicates if needed

- [ ] **Use Structured Prompt: Context + Persona + Task**
  - [ ] **Context:** Include retrieved KG information (nodes, relationships, data)
  - [ ] **Persona:** Define assistant's role (e.g., "You are a helpful hotel travel assistant")
  - [ ] **Task:** Clear instructions on what to do with context (e.g., "Answer the user's question using only the provided information")

- [ ] **Compare At Least Three LLM Models**
  - [ ] **LLM Model 1:** ________________________________
  - [ ] **LLM Model 2:** ________________________________
  - [ ] **LLM Model 3:** ________________________________

- [ ] **Comparison Must Include Qualitative AND Quantitative Impressions**
  - [ ] **Quantitative:** Metrics like accuracy, response time, token usage, cost
  - [ ] **Qualitative:** Human evaluation of answer quality, relevance, naturalness, correctness
  - [ ] Create comparison table/report
  - [ ] Document which model performs best

---

### 💻 Part 4: Build UI (e.g., Streamlit)

- [ ] **Required Features**
  - [ ] Allow user to input questions
  - [ ] **View KG-retrieved context** (show raw information retrieved from KG before LLM processing)
  - [ ] **View final LLM answer** (display LLM's response to user's query)

- [ ] **Optional Features (encouraged but not required)**
  - [ ] **Cypher Queries Executed:** Show actual Cypher queries that were run
  - [ ] **Graph Visualization Snippets:** Visualize retrieved subgraph (nodes and relationships)
  - [ ] **Recommendations:** Display hotel recommendations with explanations
  - [ ] **Model Selection Dropdown:** Allow users to select which LLM to use
  - [ ] **Retrieval Method Selection:** Allow users to choose baseline, embeddings, or both

---

### 📊 Part 5: Experiments, Results, & Improvements

**Your final presentation must include:**

- [ ] **System Architecture**
  - [ ] Document overall system design, components, and how they interact
  - [ ] Show pipeline: preprocessing → retrieval → LLM → UI
  - [ ] Include architecture diagrams

- [ ] **Retrieval Strategy and Examples**
  - [ ] Explain Cypher queries
  - [ ] Explain embedding approach
  - [ ] Show example queries and their results
  - [ ] Document both baseline and embedding-based retrieval strategies

- [ ] **LLM Comparison**
  - [ ] Present quantitative metrics comparing 3+ models
  - [ ] Present qualitative analysis comparing 3+ models

- [ ] **Error Analysis**
  - [ ] Document cases where the system failed
  - [ ] Explain why it failed
  - [ ] Explain how it could be improved

- [ ] **Improvements Added**
  - [ ] Describe enhancements you made to overcome limitations

- [ ] **Remaining Limitations**
  - [ ] Acknowledge what the system cannot do well
  - [ ] Describe what would need further work

---

## 📑 Presentation Checklist (18-22 minutes)

**Presentation Outline (from guidelines):**

- [ ] **High-Level System Architecture (2 min)**
  - [ ] Show overview of pipeline
  - [ ] Present task of choice
  - [ ] Mention if external dataset was used

- [ ] **Input Preprocessing (2 min)**
  - [ ] Intent classifier (rule-based, LLM-based, or hybrid)
  - [ ] Entity extraction, with examples
  - [ ] Embedding step (if used)

- [ ] **Graph Retrieval Layer - Baseline (2-3 min)**
  - [ ] Show your Cypher query templates (at least 10 should be implemented)
  - [ ] Show snippet of retrieved nodes/relationships

- [ ] **Graph Retrieval Layer - Embedding-Based Retrieval (2-3 min)**
  - [ ] State approach selected: Node embeddings OR Feature vector embeddings
  - [ ] Show the two embedding models compared, with experiment results

- [ ] **LLM Layer (3-4 min)**
  - [ ] Context Construction: how you integrate input, baseline Cypher output, and embedding output
  - [ ] Prompt Structure (context, persona, task)
  - [ ] LLMs Comparison: quantitative metrics and qualitative evaluation

- [ ] **Error Analysis & Improvements (2 min)**
  - [ ] Document failure cases and explanations
  - [ ] Show improvements implemented

- [ ] **Live Demo (4-5 min)**
  - [ ] Wrap up full pipeline (from raw input to final answer)
  - [ ] Demo must be live (not recorded video)
  - [ ] Must be able to switch between embedding models
  - [ ] Must be able to switch between LLMs
  - [ ] Use chosen questions to demonstrate integration
  - [ ] Demo must show integration, not isolated components
  - [ ] UI should reflect the process done in background

### Presentation Guidelines

**What NOT to do:**
- [ ] Do NOT explain concepts from labs
- [ ] Do NOT add introductions, problem statements, motivations, or related work
- [ ] Do NOT depend only on diagrams, only on text, or only on screenshots
- [ ] Do NOT use text-heavy descriptions
- [ ] Do NOT include dataset descriptions or high-level theme overviews

**Regulations:**
- [ ] All team members must participate in presentation
- [ ] Presentation slides must be submitted by December 15th at 23:59
- [ ] Each team member responsible for one component (distribute work equally)

**Individual Q&A (after presentation):**
- [ ] Each member will be examined individually on their specific component
- [ ] Multiple rounds per person depending on remaining time
- [ ] You may be asked to walk through code, explain operations, discuss errors, or justify decisions
- [ ] **Only the person asked may answer**

---

## 📤 Submission Guidelines

**Deadline: December 15th at 23:59**

- [ ] **Submit GitHub repository**
  - [ ] Create branch named "Milestone3"
  - [ ] Include all code and requirements
  - [ ] Keep repository private until deadline

- [ ] **Submit link to presentation slides**

- [ ] **After deadline:**
  - [ ] Make repository public OR add "csen903w25-sys" as collaborator for grading

---

## 📅 Evaluation (December 16)

**Format: 45-minute slot per team**

### Part 1: Team Presentation (15% of grade)
- [ ] 18-22 minutes minimum/maximum
- [ ] Focus on: system architecture, pipeline integration, retrieval strategies, experimental results, live demo
- [ ] Evaluates: functionality, completeness, performance of Graph-RAG pipeline
- [ ] All team members must participate

### Part 2: Individual Q&A Evaluation (15% of grade)
- [ ] Each member examined individually on their specific component
- [ ] Multiple rounds per person possible (depending on remaining time)
- [ ] Questions about: code walkthrough, operations sequence, error cases, implementation decisions
- [ ] **When a question is directed to a specific member, only that member is allowed to answer**

---

## 📚 Resources & Important Notes

### Required Labs (Milestone 3 folder)
- Lab 6: Knowledge Graphs
- Lab 7: Introduction to Neuro-Symbolic AI
- Lab 8: Retrieval Augmented Generation Using LangChain

### Important Notes from Milestone Description
- ✅ You ARE allowed to add to existing schema and/or integrate data with external dataset
- ✅ Question Answering System is the primary task (option to extend to other tasks)
- ✅ You are free to define any creative task/use case, as long as core Graph-RAG pipeline is implemented
- ✅ You will be evaluated on: system integration, design, functionality, and attempts of improvement
- ✅ **There is NO threshold for performance** - focus on the implementation and learning process

### Hotel Theme Specifics
- **Focus areas:** Hotel search, reviews, recommendations, visa requirements
- **Entities:** Hotels, cities, countries, traveller types, demographics
- **Use textual review content** for feature vector embeddings
- **Consider:** Traveller demographics and preferences in recommendations

### Useful Documentation Links
- [Neo4j Documentation](https://neo4j.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [HuggingFace Models (free)](https://huggingface.co/models)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Last Updated:** December 8, 2024
