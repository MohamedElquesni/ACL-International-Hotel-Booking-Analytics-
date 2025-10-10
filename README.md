# International Hotel Booking Analytics

## Project Structure

```
Project/
├── Dataset [Original]/          # Original dataset files
│   ├── booking_db.sqlite
│   ├── hotels.csv
│   ├── reviews.csv
│   └── users.csv
├── data/                        # Cleaned and processed datasets
├── models/                      # Saved trained models
├── reports/                     # Analysis reports and visualizations
├── notebooks/                   # Jupyter notebooks
│   └── milestone1_analysis.ipynb
└── Previous Labs For Reference/ # Reference materials
```

## Notebook Structure Guidelines

### Each Major Objective Must Be:
1. **Clearly boxed** with markdown headers and visual separation
2. **Hierarchically organized** with subboxes for sub-tasks
3. **Self-contained** with all relevant code, outputs, and explanations

### Standard Section Format:
```
# 📦 [Objective Number]: [Objective Title]
## Description
[Brief description of the objective]

### 📋 Sub-objective 1: [Title]
[Content]

### 📋 Sub-objective 2: [Title]
[Content]
```

## Milestone 1 Objectives

### 1. Data Cleaning
- Remove unnecessary columns
- Handle null values and duplicates

### 2. Data Engineering Questions (with visualizations)
- Q1: Which city is best for each traveler type? (Solo, Business, Family, Couple)
- Q2: What are the top 3 countries with the best value-for-money score per traveler's age group?

### 3. Predictive Modeling
- Build a multi-class classification model (statistical ML or shallow FFNN)
- Predict: `country_group` (11 groups)
- Input Features: Score-based, User demographics, Quality features
- Evaluate with: Accuracy, Precision, Recall, F1-score

### 4. Model Explainability
- Apply SHAP and LIME to interpret predictions
- Show which features most influence the model

## Deliverables
1. Jupyter Notebook with complete workflow
2. Cleaned dataset with `country_group` column
3. Report answering the 2 questions with visualizations
4. Trained model
5. XAI outputs (SHAP/LIME plots)
6. Inference function

## Deadline
**October 22, 2025 at 11:59 PM**
