# Problem Formulation – Telecom Customer Churn Prediction

## 1. Business Problem
Telecom companies face customer churn, where customers leave their service for competitors. The business problem is to **predict which customers are likely to churn** so that the company can take proactive retention measures.

---

## 2. Business Objectives
- Reduce overall churn rate by identifying at-risk customers.
- Enable targeted retention campaigns.
- Improve customer lifetime value and revenue retention.
- Optimize marketing and customer engagement strategies.

---

## 3. Key Data Sources and Attributes
### Data Sources
1. **CSV File:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`  
2. **API JSON:** Remote GitHub dataset (`telecom_churn.json`)  

### Key Attributes
| Column Name       | Description                              |
|------------------|------------------------------------------|
| customerID        | Unique identifier for each customer      |
| gender            | Male/Female                               |
| SeniorCitizen     | 0 = No, 1 = Yes                           |
| Partner           | Customer has a partner?                   |
| Dependents        | Customer has dependents?                  |
| tenure            | Number of months with the company        |
| PhoneService      | Customer has phone service?               |
| MultipleLines     | Multiple lines subscription               |
| InternetService   | Type of internet service                  |
| OnlineSecurity    | Online security subscription              |
| OnlineBackup      | Online backup subscription                |
| DeviceProtection  | Device protection subscription            |
| TechSupport       | Tech support subscription                 |
| StreamingTV       | Streaming TV subscription                  |
| StreamingMovies   | Streaming Movies subscription             |
| Contract          | Contract type (Month-to-month, One year) |
| PaperlessBilling  | Paperless billing?                        |
| PaymentMethod     | Payment method (Credit card, Bank, etc.) |
| MonthlyCharges    | Monthly subscription charge               |
| TotalCharges      | Total charges to date                     |
| Churn             | Target: Yes = customer churned           |

---

## 4. Expected Pipeline Outputs
1. **Cleaned dataset for exploratory analysis**
   - `data/processed/clean_churn.csv`
2. **Transformed features for machine learning**
   - SQLite DB: `transformed_churn.db`
   - CSV for feature store: `transformed_churn.csv`
3. **Trained deployable ML model**
   - `models/<best_model_name>_churn_model.pkl` (versioned via MLflow)

---

## 5. Evaluation Metrics
- **Accuracy** – Proportion of correctly predicted churn/non-churn.  
- **Precision** – Correctly predicted churns out of all predicted churns.  
- **Recall** – Correctly predicted churns out of all actual churns.  
- **F1-score** – Harmonic mean of precision and recall.  
- **ROC-AUC** – Measure of model’s ability to distinguish classes.  
- **Confusion Matrix** – Visual summary of TP, FP, TN, FN.  

All metrics are saved in `reports/model_performance_<timestamp>.txt/.csv` and visualized with ROC and confusion matrix plots.

---

## 6. Deliverables
- **Source code:** Modular Python scripts (`src/` and `dags/`)  
- **Cleaned dataset:** `data/processed/clean_churn.csv`  
- **Feature store exports:** `transformed_churn.csv` and `transformed_churn.db`  
- **Trained model:** `models/<best_model_name>_churn_model.pkl`  
- **Reports:** Model performance metrics and plots (`reports/`)  
- **Documentation:** This file and `README.md`  
- **Video walkthrough:** 5–10 minute demonstration of the full pipeline

---
