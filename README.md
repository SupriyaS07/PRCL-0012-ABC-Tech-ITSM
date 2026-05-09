# 🎫 PRCL-0012 | ABC Tech ITSM — ML Powered Incident Management

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=flat-square&logo=mysql)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-red?style=flat-square&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?style=flat-square&logo=streamlit)
![Flask](https://img.shields.io/badge/Flask-API-black?style=flat-square&logo=flask)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)

---

## 📋 Project Overview

**Client:** ABC Tech  
**Project Ref:** PRCL-0012  
**Domain:** IT Service Management (ITSM)  
**Internship:** Rubixe AI Solutions  
**Developer:** Supriya  

ABC Tech is a mid-size IT organization handling **22,000–25,000 IT incident tickets annually** using the ITIL framework. Despite mature processes, customer satisfaction for incident management was rated as **poor**. This project applies Machine Learning to transform their ITSM system from **reactive to proactive** through prediction and automation.

---

## 🎯 Business Problem

| Problem | Impact |
|---|---|
| Manual priority assignment | Wrong priorities → critical issues ignored |
| Wrong department tagging | Tickets bounce between teams → delays |
| No incident forecasting | Unprepared for high-ticket periods |
| Reactive approach | Problems fixed after they escalate |

---

## 🤖 ML Use Cases

### ✅ Use Case 1 — High Priority Ticket Prediction
- **Goal:** Predict if incoming ticket is Priority 1 or 2 (Critical/High)
- **Type:** Binary Classification
- **Challenge:** Severe class imbalance (only 1.5% high priority tickets)
- **Solution:** SMOTE + Random Forest + GridSearchCV
- **Result:** **99.31% Accuracy | 99.46% Recall**

### ✅ Use Case 2 — Incident Volume Forecasting
- **Goal:** Forecast monthly/quarterly/annual incident volume
- **Type:** Time Series Forecasting
- **Challenge:** Outlier in June 2013 (25,401 tickets — bulk migration)
- **Solution:** ADF Test + ARIMA(2,1,2)
- **Result:** **MAE: 272.93 | RMSE: 319.14**

### ✅ Use Case 3 — Auto Tag Tickets
- **Goal:** Automatically assign correct priority (2/3/4/5) to tickets
- **Type:** Multi-class Classification
- **Challenge:** 4-class imbalance, Priority 1 had only 3 records
- **Solution:** Merged P1+P2, SMOTE + Random Forest + GridSearchCV
- **Result:** **91.92% Accuracy | Priority 2 F1: 0.98**

### ❌ Use Case 4 — RFC Failure Prediction
- **Status:** Not feasible
- **Reason:** Only 1 RFC (Request for Change) record in 46,606 tickets
- **Decision:** Documented as data limitation

---

## 📊 Dataset Details

| Property | Value |
|---|---|
| Total Records | 46,606 |
| Years Covered | 2012, 2013, 2014 |
| Data Source | MySQL Database (Read-Only) |
| Database | project_itsm |
| Table | dataset_list |

### Key Features
`CI_Name` · `CI_Cat` · `CI_Subcat` · `WBS` · `Incident_ID` · `Status` · `Impact` · `Urgency` · `Priority` · `Category` · `KB_number` · `No_of_Reassignments` · `Open_Time` · `Resolved_Time` · `Close_Time` · `Handle_Time_hrs` · `Closure_Code` · `No_of_Related_Interactions`

---

## 📈 Model Performance Summary

| Use Case | Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|---|
| UC1 — High Priority | Random Forest (Tuned) | 99.31% | 99.16% | 99.46% | 99.31% |
| UC2 — Forecasting | ARIMA(2,1,2) | MAE: 272.93 | RMSE: 319.14 | — | — |
| UC3 — Auto Tag | Random Forest (Tuned) | 91.92% | 91.95% | 91.92% | 91.92% |
| UC4 — RFC Failure | Not Built | — | — | — | — |

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.8+ |
| Database | MySQL (mysql-connector-python) |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn, XGBoost |
| Imbalance Handling | imbalanced-learn (SMOTE) |
| Time Series | Statsmodels (ARIMA) |
| Backend API | Flask |
| Frontend App | Streamlit |
| Model Saving | Joblib |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
PRCL_0012_ABC_Tech_ITSM/
│
├── 📓 PRCL_0012_ABC_Tech_ITSM.ipynb   # Main Jupyter Notebook
├── 🐍 app.py                           # Streamlit Frontend App
├── 🐍 flask_api.py                     # Flask Backend REST API
├── 🐍 database.py                      # MySQL Connection Helper
├── 📄 requirements.txt                 # Python Dependencies
├── 📝 README.md                        # Project Documentation
│
└── 📁 models/
    ├── model_uc1.pkl                   # UC1 Random Forest Model
    ├── model_uc2.pkl                   # UC2 ARIMA Model
    ├── model_uc3.pkl                   # UC3 Random Forest Model
    ├── uc1_features.pkl                # UC1 Feature List
    ├── uc3_features.pkl                # UC3 Feature List
    ├── label_mapping.pkl               # UC3 Label Mapping
    └── reverse_mapping.pkl             # UC3 Reverse Mapping
```

---

## 🚀 How to Run

### Step 1 — Clone Repository
```bash
git clone https://github.com/SupriyaS07/PRCL-0012-ABC-Tech-ITSM.git
cd PRCL-0012-ABC-Tech-ITSM
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run Flask API (Terminal 1)
```bash
python flask_api.py
```
You should see:
```
✅ All models loaded!
* Running on http://127.0.0.1:5000
```

### Step 4 — Run Streamlit App (Terminal 2)
```bash
streamlit run app.py
```

### Step 5 — Open Browser
```
http://localhost:8501
```

### Login Credentials
| Username | Password | Role |
|---|---|---|
| admin | itsm2024 | Administrator |
| supriya | rubix123 | Data Scientist |
| analyst | abctech | Analyst |

---

## 🔬 ML Pipeline

```
MySQL Database (46,606 records)
        ↓
Data Extraction (mysql-connector)
        ↓
EDA — Distributions, Trends, Patterns
        ↓
Preprocessing — Null handling, Encoding,
                Feature Engineering
        ↓
    ┌───────────────────────────────┐
    │                               │
   UC1                            UC3
Binary Classification        Multi-class Classification
SMOTE → RF + XGBoost        SMOTE → RF + XGBoost
RandomizedSearchCV          RandomizedSearchCV
GridSearchCV                GridSearchCV
99.31% Accuracy             91.92% Accuracy
    │                               │
    └───────────────────────────────┘
                ↓
              UC2
    Time Series Forecasting
    ADF Test → ARIMA(2,1,2)
    MAE: 272.93
                ↓
         Deployment
    Flask API + Streamlit App
    Login → Dashboard → Predictions
```

---

## 📊 Key Findings from EDA

- Priority 4 dominates dataset (51.7%) — severe class imbalance
- June 2013 had 25,401 tickets (outlier — bulk data migration event)
- Top features: KB_number (20.1%), WBS (17.3%), CI_Subcat (14.7%)
- Q2 (Apr–Jun) consistently highest incident volume quarter
- Only 1.5% of tickets are High Priority (Priority 1 or 2)
- 46,606 records with 21 features after preprocessing

---

## 🏆 Key Achievements

- ✅ Built end-to-end ML pipeline on real enterprise MySQL database
- ✅ Handled severe class imbalance (1.5% minority) using SMOTE
- ✅ Resolved data leakage from Impact/Urgency features
- ✅ Achieved 99.31% accuracy for critical ticket detection
- ✅ Deployed full stack app with Flask REST API + Streamlit UI
- ✅ Live MySQL dashboard with real-time predictions
- ✅ Secure login system with role-based access

---

## 👤 Developer

**Supriya**  
BCA Graducate ,Bangalore  
MCA Present first sem

Data Science Intern — Rubixe AI Solutions (Feb 2026 – Jul 2026)  

[![GitHub](https://img.shields.io/badge/GitHub-SupriyaS07-black?style=flat-square&logo=github)](https://github.com/SupriyaS07)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Supriya-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/supriya-111a3124b)

---

## 📄 License

This project is developed as part of internship at **Rubixe AI Solutions**.  
Dataset provided by **DataMites™ Solutions Pvt Ltd** — for educational purposes only.

---

*Built with ❤️ by Supriya | PRCL-0012 | ABC Tech ITSM*