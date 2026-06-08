# AIAP Batch 24 Technical Assessment - Session Summary

**Generated:** 2026-06-08 10:06  
**Assessment Deadline:** 2026-06-08 19:00 SGT  
**Status:** ⚠️ CRITICAL: 60% complete, ML Pipeline missing

---

## 1. ASSESSMENT REQUIREMENTS (4 Deliverables)

### ✅ COMPLETE
- **Data Exploration & Preparation** — All datasets processed and analyzed
  - Merged deliveries + feedback (151,023 rows × 22 columns)
  - 24 export files in `data_exports/` (Excel, CSV, PNG)
  - Monthly breakdown with trends
  - Driver performance rankings

### ⚠️ IN-PROGRESS / INCOMPLETE
- **decision_log.md** — Template only (Q1-Q5 need candidate answers)
- **prompt_chat_history.md** — Template only (needs AI chat transcripts & share-links)
- **eda.ipynb** — Jupyter notebook created but incomplete
  - Data load: ✅ Done
  - Analysis cells: ❌ Need completion
  - Visualizations: ❌ Need implementation
  - Findings documentation: ❌ Missing

### ❌ NOT STARTED
- **ML Pipeline** — No `src/` folder or pipeline code
  - `requirements.txt` — MISSING
  - `run.sh` — MISSING
  - README.md — MISSING
  - Python model code — MISSING

---

## 2. DATA PROCESSING COMPLETED ✅

### Source Data
- **Deliveries DB:** 150,750 records
- **Feedback DB:** 54,972 records
- **Date Range:** Nov 28, 2025 - May 27, 2026 (7 months)

### Merged Dataset
- **File:** `data_exports/Deliveries_Main.xlsx`
- **Size:** 151,023 rows × 22 columns
- **Columns:** delivery_id, branch, client_id, booking_datetime, pickup_datetime, promised_delivery_datetime, delivery_datetime, distance_km, parcel_weight_kg, parcel_value_sgd, parcel_category, delivery_priority, num_stops_on_route, driver_id, driver_experience_months, vehicle_type, payment_method, recipient_postal_code, feedback_id, rating, comment, feedback_datetime

### Key Findings
1. **On-time Delivery Rate:** 89% overall
2. **Feedback Coverage:** 35% of deliveries have ratings (53,007 / 151,023)
3. **Average Rating:** 4.30/5.0
4. **Critical Correlation:** On-time deliveries avg 4.63★ vs late deliveries avg 2.97★
5. **Trend Alert:** Rating declining from 4.50 (Nov 2025) → 4.08 (May 2026)

### Data Quality Issues Identified
- Branch names: Mixed case variants (Cnetral, EAST, Noth, west)
- Weight values: -1 entries (data errors)
- Parcel value: -1 entries (data errors)
- Stops on route: -1 entries (data errors)

---

## 3. DATA EXPORTS (24 FILES)

### Main Files
| File | Format | Rows | Purpose |
|------|--------|------|---------|
| Deliveries_Main | .xlsx | 151,023 | Full merged dataset with formatting |
| deliveries_feedback_merged | .csv | 151,023 | Raw merged data for ML pipeline |
| Monthly_Feedback_Scores | .xlsx | 7 | Monthly avg ratings & delivery metrics |
| Monthly_Feedback_Details | .xlsx | 7 | Breakdown by on-time/late status |
| Depot_OnTime_Performance | .xlsx | 4 | Branch performance analysis |
| all_drivers_ranked | .csv | 500+ | Driver performance rankings |

### Analysis Dashboards
- `delivery_analysis_dashboard.png` — 9-chart overview
- `delivery_key_metrics.png` — 4 key branch metrics  
- `monthly_analysis_dashboard.png` — Trend visualizations

---

## 4. WHAT'S DONE ✅

### Phase 1: Problem Understanding & Data Exploration
- ✅ Extracted requirements from assessment PDF
- ✅ Queried delivery.db and feedback tables
- ✅ Identified target: **Predict delivery delays (on-time vs late)**
- ✅ Created data summary with key metrics
- ✅ Generated visualizations showing data patterns

### Phase 2: Data Processing & Cleaning
- ✅ Merged deliveries + feedback on delivery_id
- ✅ Exported to Excel with formatting (borders, headers, frozen rows)
- ✅ Created CSV versions for Python pipeline
- ✅ Identified data quality issues (branch names, missing values)
- ✅ Generated monthly breakdown and trends

### Phase 3: Exploratory Analysis
- ✅ Branch distribution: Central (29.8%), East (24.8%), West (23.0%), North (21.9%)
- ✅ Vehicle types: Van (55.3%), Bike (30.4%), Truck (9.6%)
- ✅ Delivery priority: Standard (55.2%), Express (27.8%), Premium (12.9%), VIP (4.0%)
- ✅ Driver experience range: -1 to 120 months (avg 17.66)
- ✅ On-time correlation: Rating drops 1.66 points for late deliveries

---

## 5. WHAT'S MISSING ❌

### Critical for Submission (Must Do Before 19:00)

#### A. **ML Prediction Pipeline** (50% of assessment)
- [ ] Create `src/` folder with Python modules
- [ ] Data preprocessing script (handle missing values, feature engineering)
- [ ] Model training script (classification: on-time vs late)
- [ ] Model evaluation (accuracy, precision, recall, F1)
- [ ] Prediction inference script
- [ ] SQL data loading (fetch from delivery.db)
- [ ] Error handling & logging

#### B. **CI/CD Configuration**
- [ ] `requirements.txt` with all dependencies
- [ ] `run.sh` bash script to execute pipeline
- [ ] README.md with usage instructions

#### C. **Jupyter Notebook (EDA)**
- [ ] Complete exploratory analysis in eda.ipynb
- [ ] Add visualizations for key features
- [ ] Document findings and patterns
- [ ] Include markdown explanations

#### D. **Decision Log** (Assessment Logic)
- [ ] Q1: Clarifying questions (How would you refine the problem?)
- [ ] Q2: Problem statement (What exactly are you solving?)
- [ ] Q3: Key decisions (Options considered, choice made, rationale)
- [ ] Q4: AI assistant usage (3 specific examples of changes/rejections)
- [ ] Q5: Next steps (If you had 1 more week, what would you do?)

#### E. **Prompt Chat History**
- [ ] Share-links from Claude/ChatGPT/GitHub Copilot chats
- [ ] Raw transcripts (not edited, not summarized)
- [ ] [User] / [AI] format, one blank line between turns

---

## 6. FASTEST PATH TO SUBMISSION ⚡

### Time Budget (≈9 hours remaining)
**Priority 1 (2-3 hours):** ML Pipeline
- Skeleton: 30 min (folder structure, imports)
- Data loading: 30 min (SQL queries, preprocessing)
- Model training: 1 hour (simple logistic regression or XGBoost)
- Evaluation: 30 min (metrics, confusion matrix)
- Inference script: 30 min

**Priority 2 (1-2 hours):** Configuration
- requirements.txt: 15 min (pip freeze or manual list)
- run.sh: 15 min (simple bash wrapper)
- README.md: 30 min (document what pipeline does)

**Priority 3 (1.5-2 hours):** Documentation
- eda.ipynb: 45 min (add analysis & visualizations)
- decision_log.md: 45 min (reflect on work done)
- prompt_chat_history.md: 30 min (compile chat transcripts)

### Recommended Order
1. **Now (10:06):** Start ML pipeline skeleton + data loading
2. **By 13:00:** Complete model training & evaluation
3. **By 14:00:** Create requirements.txt, run.sh, README.md
4. **By 15:00:** Finalize eda.ipynb
5. **By 17:00:** Complete decision_log.md
6. **By 18:00:** Compile prompt_chat_history.md
7. **By 18:45:** Final review & commit

---

## 7. RECOMMENDATION FOR ML PIPELINE

### Problem Definition (Finalized)
**Binary Classification:** Predict on-time delivery (1) vs late delivery (0)

### Target Variable
- On-time: `delivery_datetime <= promised_delivery_datetime`
- Late: `delivery_datetime > promised_delivery_datetime`
- Class balance: 89% on-time, 11% late (imbalanced → use F1, recall)

### Recommended Features
| Feature | Type | Reason |
|---------|------|--------|
| distance_km | numeric | Longer distances = higher risk |
| parcel_weight_kg | numeric | Heavier = slower |
| driver_experience_months | numeric | More experience = faster |
| delivery_priority | categorical | VIP/Premium = faster delivery |
| vehicle_type | categorical | Van/Truck vs Bike different speeds |
| parcel_category | categorical | Fragile/Oversized need care |
| num_stops_on_route | numeric | More stops = longer time |
| branch | categorical | Different depot efficiency |
| booking_hour | numeric | Time of day booked |

### Model Suggestions
1. **Logistic Regression** — Simple, interpretable, baseline
2. **XGBoost** — Better performance with feature interactions
3. **RandomForest** — Feature importance analysis

### Data Handling
- Missing values: Impute with median (numeric) or mode (categorical)
- Branch names: Standardize (Central, East, West, North)
- Data errors: Remove rows with weight/value/stops < 0
- Train/test split: 80/20 or time-based (earlier = train, recent = test)

---

## 8. FILES TO CREATE IMMEDIATELY

### Core ML Pipeline (`src/` folder)
```
src/
├── __init__.py
├── data_loader.py          # Load from delivery.db
├── preprocessing.py        # Feature engineering, handle missing values
├── model.py               # Train & evaluate models
├── predictor.py           # Load model & make predictions
└── utils.py               # Helper functions
```

### Config Files (repo root)
```
requirements.txt           # pip install -r requirements.txt
run.sh                     # bash run.sh (execute pipeline)
README.md                  # Documentation
```

---

## 9. NEXT IMMEDIATE STEP

**User Action Required:**
1. Review this summary (confirm understanding)
2. Begin ML pipeline creation (data_loader.py first)
3. Use existing merged CSV: `data_exports/deliveries_feedback_merged.csv`
4. Test on small subset first (1,000 rows)

**Copilot Action:**
Ready to implement when you confirm:
- [ ] Should I create the ML pipeline skeleton now?
- [ ] Preferred model: Logistic Regression (fast) or XGBoost (better)?
- [ ] Any specific evaluation metrics you want to emphasize?

---

**Current Time:** 10:06 SGT  
**Deadline:** 19:00 SGT (≈8 hours 54 minutes remaining)  
**Status:** Actionable — All data ready, pipeline implementation required
