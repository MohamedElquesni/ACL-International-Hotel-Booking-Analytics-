# Milestone 1: International Hotel Booking Analytics

> Predicting hotel country groups using machine learning and explainable AI

## 📋 Project Overview

**Goal:** Build a classification model to predict which geographic region a hotel belongs to based on user demographics, review scores, and hotel characteristics.

- **Dataset:** 50,000 reviews across 25 hotels in 25 countries
- **Task:** Multi-class classification (11 country groups)
- **Evaluation:** Accuracy, Precision, Recall, F1-Score

---

## ✅ Progress Tracker

| Section | Status | Priority |
|---------|--------|----------|
| 1. Data Cleaning | ✅ Complete | - |
| 2. Data Engineering Questions | ✅ Complete | - |
| 3. Exploratory Data Analysis | ❌ TODO | 🔴 High |
| 4. Feature Engineering | ❌ TODO | 🔴 High |
| 5. Data Preprocessing | ❌ TODO | 🔴 High |
| 6. Model Development | ❌ TODO | 🔴 Critical |
| 7. Model Evaluation | ❌ TODO | 🔴 Critical |
| 8. Model Explainability (XAI) | ❌ TODO | 🟡 Required |
| 9. Inference Function | ❌ TODO | 🟡 Required |
| 10. Conclusions | ❌ TODO | 🟢 Low |

---

## 📖 Section Details

### Section 1: Data Cleaning ✅

**1.1** Load three datasets (hotels.csv, reviews.csv, users.csv)
**1.2** Rename columns with prefixes for clarity
**1.3** Check for missing values and duplicates
**1.4** Merge datasets on foreign keys

---

### Section 2: Data Engineering Questions ✅

**2.1** Best City for Each Traveler Type
- Calculate average review scores by (city, traveler_type)
- Create heatmap visualization
- Identify best city for each of 4 traveler types
- Document insights and recommendations

**2.2** Top 3 Countries by Value-for-Money per Age Group
- Calculate average value-for-money scores by (country, age_group)
- Create heatmap visualization
- Identify top 3 countries for each of 5 age groups
- Statistical validation (sample sizes, std dev)
- Document insights

---

### Section 3: Exploratory Data Analysis ❌

**3.1** Target Variable Analysis
- Create `country_group` target variable
- Analyze distribution (bar chart, pie chart)
- Calculate class imbalance ratio
- Document implications for modeling

**3.2** Numerical Features Analysis
- Identify all numerical columns
- Statistical summary (.describe())
- Distribution plots (histograms with KDE)
- Box plots for outlier detection
- Document findings (skewness, outliers, variance)

**3.3** Correlation Analysis
- Calculate correlation matrix
- Create correlation heatmap
- Identify highly correlated pairs (|r| > 0.8)
- Analyze features with most variance across country groups
- Document multicollinearity concerns

**3.4** Categorical Features Analysis
- Value counts for each categorical feature
- Distribution bar charts
- Cross-tabulation with target variable
- Identify patterns and relationships
- Plan encoding strategy

---

### Section 4: Feature Engineering ❌

**4.1** Create Deviation Features
- `deviation_cleanliness = review_score_cleanliness - hotel_cleanliness_base`
- Repeat for: comfort, facilities, location, staff, value_for_money
- Document reasoning: captures if hotel exceeded/fell short of baseline

**4.2** Create Aggregate Features
- `avg_review_score`: mean of all review_score_* columns
- `avg_hotel_baseline`: mean of all hotel_*_base columns
- Document reasoning

**4.3** Create Interaction Features (Optional)
- age_group × traveler_type combinations
- Test if they improve performance

**4.4** Final Feature Set
- List all features being used (15-25 features)
- Justify each feature with evidence
- Document features excluded and why

---

### Section 5: Data Preprocessing ❌

**5.1** Categorical Encoding
- One-hot encode: user_gender, user_age_group, user_traveller_type
- Target/frequency encode: user_country (high cardinality)
- Label encode target: country_group
- Show before/after shape

**5.2** Numerical Scaling
- Apply StandardScaler to numerical features
- Show distribution before/after scaling
- Save scaler for inference function

**5.3** Train-Test-Validation Split
- 70% train, 15% validation, 15% test
- Use stratified split to maintain class balance
- Verify class distribution in each split
- Print shapes

**5.4** Handle Class Imbalance
- Choose strategy: class weights or SMOTE
- Implement chosen approach
- Document reasoning

---

### Section 6: Model Development ❌

**6.1** Train Baseline Models
- Model 1: Logistic Regression (simple baseline)
- Model 2: Random Forest (ensemble method)
- Model 3: XGBoost (gradient boosting)
- Model 4: Shallow Neural Network (2-3 layers, required)
- Document training time for each

**6.2** Hyperparameter Tuning
- Use GridSearchCV or RandomizedSearchCV
- Define search space for each model
- Show best parameters found
- Compare performance before/after tuning

**6.3** Model Comparison
- Create table comparing all models
- Include: Accuracy, Precision, Recall, F1, Training Time
- Identify best performing model

**6.4** Final Model Selection
- Choose best model
- Justify decision (accuracy vs speed vs interpretability)
- Document trade-offs

---

### Section 7: Model Evaluation ❌

**7.1** Test Set Performance
- Evaluate best model on unseen test data
- Report: Accuracy, Precision, Recall, F1-Score
- Use both macro and weighted averaging
- Per-class metrics for all 11 country groups

**7.2** Confusion Matrix
- Create confusion matrix heatmap
- Analyze misclassification patterns
- Identify which country groups are confused

**7.3** Classification Report
- Generate full sklearn classification report
- Identify classes with low recall/precision
- Discuss why certain classes perform poorly

**7.4** Error Analysis
- Sample 5-10 misclassified examples
- Analyze why model made mistakes
- Identify systematic errors

---

### Section 8: Model Explainability (XAI) ❌

**8.1** SHAP Analysis - Global
- Create SHAP summary plot (feature importance)
- Create SHAP bar plot (mean absolute values)
- Create dependence plots for top 3-5 features
- Interpret which features matter most globally

**8.2** SHAP Analysis - Local
- Pick 3-5 test instances (diverse examples)
- Create SHAP force plots
- Create SHAP waterfall plots
- Explain how features contribute to each prediction

**8.3** LIME Analysis
- Explain same 3-5 instances as SHAP
- Create LIME plots
- Compare SHAP vs LIME interpretations

**8.4** Business Insights
- Translate XAI findings into business language
- Which features drive country group predictions?
- Actionable recommendations for hotels/travelers

---

### Section 9: Inference Function ❌

**9.1** Build Inference Function
- Accept raw input (all feature values)
- Apply same preprocessing pipeline
- Make prediction with trained model
- Return natural language output
- Include confidence scores

**9.2** Test with Examples
- Example 1: Business traveler, high scores
- Example 2: Family traveler, mixed scores
- Example 3: Edge case with unusual inputs
- Show predictions and confidence

**9.3** SHAP Explanation for Predictions
- Use SHAP to explain each example prediction
- Show which features drove the prediction

---

### Section 10: Conclusions ❌

**10.1** Summary of Achievements
- What was accomplished in each section
- Key deliverables completed

**10.2** Key Findings
- Most important insights from EDA
- Best performing model and why
- Most influential features from XAI

**10.3** Model Performance
- Final accuracy and metrics
- Model strengths and limitations
- Classes where model performs well/poorly

**10.4** Future Improvements
- Use review_text for NLP/sentiment analysis
- Incorporate temporal features (seasonality)
- Try deep learning architectures
- Build real-time recommendation system
- Collect more data for underrepresented classes

---

## 📦 Deliverables Checklist

- [ ] Jupyter Notebook (runs end-to-end, well-documented)
- [ ] Cleaned dataset CSV with `country_group` column
- [ ] Analytical report (separate document with all analyses)
- [ ] Trained model file (.pkl or .h5)
- [ ] XAI visualizations (SHAP and LIME plots saved)
- [ ] Inference function (demonstrated with examples)
- [ ] GitHub repository (organized, README, .gitignore)

---

## ⏰ Time Estimates

| Section | Estimated Time |
|---------|----------------|
| 3. EDA | 3-4 hours |
| 4. Feature Engineering | 2-3 hours |
| 5. Preprocessing | 2 hours |
| 6. Model Development | 6-8 hours |
| 7. Model Evaluation | 2 hours |
| 8. XAI | 3-4 hours |
| 9. Inference Function | 1-2 hours |
| 10. Documentation | 2-3 hours |
| **Total** | **~20-25 hours** |

---

## 🎯 Workflow Recommendation

**Week 1:**
- Complete Section 3 (EDA)
- Complete Section 4 (Feature Engineering)
- Complete Section 5 (Preprocessing)
- Start Section 6 (train 2-3 models)

**Week 2:**
- Finish Section 6 (all 4 models + tuning)
- Complete Section 7 (Evaluation)
- Start Section 8 (SHAP analysis)

**Week 3:**
- Finish Section 8 (LIME analysis)
- Complete Section 9 (Inference Function)
- Complete Section 10 (Conclusions)
- Final testing and documentation

---

## 📚 Key Requirements

- **Models:** At least 1 statistical ML + 1 shallow FFNN (required)
- **Metrics:** Accuracy, Precision, Recall, F1-Score (all required)
- **XAI:** Both SHAP (global + local) and LIME (local) required
- **Inference:** Function must accept raw input, return natural language

---

## 📞 Resources

- **Project Description:** `Milestone 1/Milestone 1 - Description.pdf`
- **Checklist:** `Milestone 1/Check List.pdf`
- **Dataset:** `Dataset [Original]/` folder
- **Notebook:** `Milestone 1/Milestone 1.ipynb`
- **Deadline:** October 22, 2025, 11:59 PM

---

## 👥 Team

[Add your team member names and IDs here]

---

**Last Updated:** October 2025
