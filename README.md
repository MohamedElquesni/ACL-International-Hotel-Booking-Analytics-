# International Hotel Booking Analytics

## Project Structure

```
Project/
├── Dataset [Original]/                    # Original dataset files (shared across milestones)
│   ├── booking_db.sqlite
│   ├── hotels.csv
│   ├── reviews.csv
│   └── users.csv
│
├── Milestone 1/                           # Milestone 1: Prediction & Explainability
│   ├── notebooks/
│   │   └── milestone1.ipynb               # Main analysis notebook
│   ├── data/                              # Cleaned and processed datasets
│   ├── models/                            # Saved trained models
│   ├── reports/                           # Analysis reports and visualizations
│   ├── outputs/                           # XAI outputs (SHAP/LIME plots)
│   ├── Milestone 1 - Description.pdf
│   └── Previous Labs For Reference/
│       ├── Lab 0.pdf
│       ├── Lab 1.pdf
│       ├── Lab 2.pdf
│       ├── Lab 3.pdf
│       └── Lab 4.pdf
│
├── Milestone 2/                           # (To be created)
│
├── Milestone 3/                           # (To be created)
│
├── General Description.pdf                # Overall project description
└── README.md                              # This file
```

## Milestone 1 Progress

### Objectives

- [x] **1. Data Cleaning**
  - [x] Remove unnecessary columns
  - [x] Handle null values and duplicates

- [ ] **2. Data Engineering Questions (with visualizations)**
  - [ ] Q1: Which city is best for each traveler type? (Solo, Business, Family, Couple)
  - [ ] Q2: What are the top 3 countries with the best value-for-money score per traveler's age group?

- [ ] **3. Predictive Modeling**
  - [ ] Build a multi-class classification model (statistical ML or shallow FFNN)
  - [ ] Predict: `country_group` (11 groups)
  - [ ] Input Features: Score-based, User demographics, Quality features
  - [ ] Evaluate with: Accuracy, Precision, Recall, F1-score

- [ ] **4. Model Explainability**
  - [ ] Apply SHAP and LIME to interpret predictions
  - [ ] Show which features most influence the model

### Deliverables

- [ ] Jupyter Notebook with complete workflow
- [ ] Cleaned dataset with `country_group` column
- [ ] Report answering the 2 questions with visualizations
- [ ] Trained model
- [ ] XAI outputs (SHAP/LIME plots)
- [ ] Inference function
