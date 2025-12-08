# ACL Project - Graph-RAG Travel Assistant

## 📊 Project Progress

### Milestones Overview
```
Milestone 1: ████████████████████ 100% ✅ COMPLETED
Milestone 2: ████████████████████ 100% ✅ COMPLETED
Milestone 3: ░░░░░░░░░░░░░░░░░░░░   0% 🚧 IN PROGRESS
```

**Deadline: December 15, 2025 at 23:59**

---

## ✅ Milestone 3 - Implementation Checklist

### 🔧 Part 1: Input Preprocessing

- [ ] **Intent Classification**
  - [ ] Implement intent classifier (rule-based, LLM-based, or hybrid)
  - [ ] Test with different user queries
  - [ ] Document classification accuracy

- [ ] **Entity Extraction**
  - [ ] Set up Named Entity Recognition (NER) using spaCy
  - [ ] Extract theme-specific entities (hotels/cities/countries OR players/teams OR flights/airports)
  - [ ] Test entity extraction on sample queries

- [ ] **Input Embedding**
  - [ ] Choose embedding model (e.g., all-MiniLM-L6-v2)
  - [ ] Implement text-to-vector conversion
  - [ ] Store embeddings for semantic search

---

### 🗄️ Part 2: Graph Retrieval Layer

#### Experiment 1: Baseline (Cypher Queries)

- [ ] **Write 10+ Cypher Query Templates**
  - [ ] Query 1: ________________________________
  - [ ] Query 2: ________________________________
  - [ ] Query 3: ________________________________
  - [ ] Query 4: ________________________________
  - [ ] Query 5: ________________________________
  - [ ] Query 6: ________________________________
  - [ ] Query 7: ________________________________
  - [ ] Query 8: ________________________________
  - [ ] Query 9: ________________________________
  - [ ] Query 10: ________________________________

- [ ] **Implement Query Execution**
  - [ ] Connect to Neo4j database
  - [ ] Map intents to appropriate queries
  - [ ] Extract entities and fill query parameters
  - [ ] Retrieve results from Knowledge Graph

- [ ] **Test Baseline Retrieval**
  - [ ] Test all 10 queries with sample questions
  - [ ] Document retrieval accuracy
  - [ ] Note edge cases and failures

#### Experiment 2: Embeddings

- [ ] **Choose Embedding Approach**
  - [ ] Option A: Node Embeddings (for numerical data)
  - [ ] Option B: Feature Vector Embeddings (for textual data)

- [ ] **Implement Embedding Model 1**
  - [ ] Model name: ________________________________
  - [ ] Create vector representations
  - [ ] Store in Neo4j vector index
  - [ ] Test semantic similarity search

- [ ] **Implement Embedding Model 2**
  - [ ] Model name: ________________________________
  - [ ] Create vector representations
  - [ ] Store in Neo4j vector index
  - [ ] Test semantic similarity search

- [ ] **Compare Embedding Models**
  - [ ] Measure retrieval accuracy
  - [ ] Measure response time
  - [ ] Document which performs better
  - [ ] Create comparison table

---

### 🤖 Part 3: LLM Layer

- [ ] **Set Up LLM Infrastructure**
  - [ ] Create HuggingFace account and API token
  - [ ] Test API connection

- [ ] **Implement LLM Model 1**
  - [ ] Model name: ________________________________
  - [ ] Implement API integration
  - [ ] Test basic queries

- [ ] **Implement LLM Model 2**
  - [ ] Model name: ________________________________
  - [ ] Implement API integration
  - [ ] Test basic queries

- [ ] **Implement LLM Model 3**
  - [ ] Model name: ________________________________
  - [ ] Implement API integration
  - [ ] Test basic queries

- [ ] **Prompt Engineering**
  - [ ] Design Context section
  - [ ] Design Persona section
  - [ ] Design Task section
  - [ ] Test prompt variations

- [ ] **Combine Retrieval Results**
  - [ ] Merge baseline Cypher results
  - [ ] Merge embedding-based results
  - [ ] Remove duplicates
  - [ ] Rank/prioritize results

- [ ] **LLM Comparison & Evaluation**
  - [ ] Create test question set (minimum 10 questions)
  - [ ] Run all 3 models on test set
  - [ ] **Quantitative Metrics:**
    - [ ] Measure accuracy
    - [ ] Measure response time
    - [ ] Measure token usage
    - [ ] Calculate cost (if applicable)
  - [ ] **Qualitative Evaluation:**
    - [ ] Rate answer quality (1-5 scale)
    - [ ] Rate relevance to question
    - [ ] Rate naturalness of language
    - [ ] Rate correctness
  - [ ] Create comparison table
  - [ ] Document best performing model

---

### 💻 Part 4: Build UI (Streamlit)

- [ ] **Set Up Streamlit**
  - [ ] Install Streamlit
  - [ ] Create basic app structure
  - [ ] Test local deployment

- [ ] **Core UI Features (Required)**
  - [ ] Text input for user questions
  - [ ] Display KG-retrieved context
  - [ ] Display final LLM answer
  - [ ] Add styling/formatting

- [ ] **Optional UI Features**
  - [ ] Display executed Cypher queries
  - [ ] Graph visualization snippets (NetworkX/Plotly)
  - [ ] Show recommendations with explanations
  - [ ] Model selection dropdown (switch between LLMs)
  - [ ] Retrieval method selection (baseline/embeddings/both)

- [ ] **Testing**
  - [ ] Test with 10+ different queries
  - [ ] Test all model combinations
  - [ ] Fix bugs and edge cases
  - [ ] Ensure smooth user experience

---

### 📊 Part 5: Experiments & Analysis

- [ ] **Error Analysis**
  - [ ] Document 5+ failure cases
  - [ ] Analyze why each failed
  - [ ] Propose improvements

- [ ] **Improvements Implemented**
  - [ ] List all enhancements made
  - [ ] Document before/after comparison
  - [ ] Measure improvement impact

- [ ] **Remaining Limitations**
  - [ ] Document current system limitations
  - [ ] Suggest future work
  - [ ] Be honest about what doesn't work

- [ ] **System Architecture Diagram**
  - [ ] Create visual diagram showing all components
  - [ ] Show data flow (Input → Preprocessing → Retrieval → LLM → UI)
  - [ ] Include all technologies used

---

## 📑 Presentation Checklist (18-22 minutes)

### Slide Preparation

- [ ] **Slide 1: Title Slide**
  - [ ] Project name
  - [ ] Team members
  - [ ] Date

- [ ] **Slide 2-3: High-Level System Architecture (2 min)**
  - [ ] Pipeline overview diagram
  - [ ] Task chosen (QA/booking/recommender)
  - [ ] External dataset (if used)

- [ ] **Slide 4-5: Input Preprocessing (2 min)**
  - [ ] Intent classifier explanation
  - [ ] Entity extraction examples
  - [ ] Embedding step (if used)

- [ ] **Slide 6-7: Graph Retrieval - Baseline (2-3 min)**
  - [ ] Show 10 Cypher query templates
  - [ ] Example retrieved nodes/relationships
  - [ ] Sample output

- [ ] **Slide 8-9: Graph Retrieval - Embeddings (2-3 min)**
  - [ ] Approach chosen (Node or Feature Vector)
  - [ ] Two embedding models compared
  - [ ] Experiment results table

- [ ] **Slide 10-12: LLM Layer (3-4 min)**
  - [ ] Context construction explanation
  - [ ] Prompt structure examples
  - [ ] LLM comparison table (3+ models)
  - [ ] Quantitative metrics graph
  - [ ] Qualitative evaluation summary

- [ ] **Slide 13-14: Error Analysis & Improvements (2 min)**
  - [ ] 3-5 failure cases with explanations
  - [ ] Improvements implemented
  - [ ] Before/after comparison

- [ ] **Live Demo Preparation (4-5 min)**
  - [ ] Prepare 5+ demo questions
  - [ ] Test demo multiple times
  - [ ] Prepare backup plan if demo fails
  - [ ] Screenshots as backup

### Demo Checklist

- [ ] **Demo Setup**
  - [ ] Streamlit app runs smoothly
  - [ ] Neo4j database is accessible
  - [ ] All models are loaded and ready
  - [ ] Internet connection works

- [ ] **Demo Flow**
  - [ ] Explain full pipeline first
  - [ ] Show ability to switch embedding models
  - [ ] Show ability to switch LLMs
  - [ ] Ask 3-5 questions live
  - [ ] Show KG context being retrieved
  - [ ] Show final LLM answer

- [ ] **Backup Plan**
  - [ ] Record demo video (in case of technical issues)
  - [ ] Take screenshots of all steps
  - [ ] Have sample outputs ready

### Presentation Delivery

- [ ] **Team Coordination**
  - [ ] Assign sections to each team member
  - [ ] Practice transitions between speakers
  - [ ] Time each section (stay within 18-22 min)
  - [ ] Rehearse full presentation 2-3 times

- [ ] **Individual Q&A Preparation**
  - [ ] Each member: Review their code thoroughly
  - [ ] Each member: Prepare to explain design decisions
  - [ ] Each member: Prepare to walk through code
  - [ ] Each member: Review error cases in their component

---

## 📤 Submission Checklist

### Code Submission (Due: Dec 15 at 23:59)

- [ ] **GitHub Repository**
  - [ ] Create "Milestone3" branch
  - [ ] Commit all code
  - [ ] Include requirements.txt or environment.yml
  - [ ] Include data files (or instructions to obtain them)
  - [ ] Push to GitHub
  - [ ] Keep private until deadline

- [ ] **Code Organization**
  - [ ] Clean, commented code
  - [ ] README with setup instructions
  - [ ] Remove unnecessary files
  - [ ] Test that code runs from scratch

- [ ] **Presentation Slides**
  - [ ] Export to PDF
  - [ ] Upload to submission form
  - [ ] Include link in README

- [ ] **Submit Form**
  - [ ] Submit GitHub repository link
  - [ ] Submit presentation slides link
  - [ ] Submit before deadline

### Post-Deadline

- [ ] Make repository public OR add "csen903w25-sys" as collaborator
- [ ] Verify all files are accessible

---

## 📅 Evaluation Day Checklist (Dec 16)

### Before Your Slot

- [ ] Arrive 10 minutes early
- [ ] Test laptop and projector connection
- [ ] Open all necessary applications
- [ ] Close unnecessary tabs/applications
- [ ] Have backup on USB drive
- [ ] Charge laptop fully

### During Evaluation (45 minutes total)

- [ ] **Presentation (18-22 min)**
  - [ ] Stay within time limit
  - [ ] All team members participate
  - [ ] Speak clearly and confidently
  - [ ] Show live demo
  - [ ] Handle questions gracefully

- [ ] **Individual Q&A (remaining time)**
  - [ ] Only the person asked answers
  - [ ] Be honest if you don't know
  - [ ] Explain your code clearly
  - [ ] Discuss design decisions

---

## 🎯 Final Tips

### Do's ✅
- Start early (don't wait until last minute)
- Test everything multiple times
- Document as you go
- Ask for help during office hours
- Use free models to avoid costs
- Keep it simple and functional
- Be honest about limitations

### Don'ts ❌
- Don't overcomplicate the system
- Don't skip testing
- Don't leave demo until last day
- Don't explain concepts from labs (assume they know)
- Don't add unnecessary features
- Don't arrive late to evaluation
- Don't panic during Q&A

---

## 📚 Resources

### Required Labs
- [Lab 6: Knowledge Graphs](Milestone 3/Required Labs/Lab 6.pdf)
- [Lab 7: Neuro-Symbolic AI](Milestone 3/Required Labs/Lab 7.pdf)
- [Lab 8: RAG with LangChain](Milestone 3/Required Labs/Lab 8.pdf)

### Useful Links
- [Neo4j Documentation](https://neo4j.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [HuggingFace Models](https://huggingface.co/models)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Last Updated:** December 8, 2024
