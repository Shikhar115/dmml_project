# src/modeling/train.py

import os
import logging
import joblib
import mlflow
import mlflow.sklearn
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)

# ---------------- Logging ---------------- #
logging.basicConfig(
    filename="modeling.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def plot_confusion_matrix(y_true, y_pred, model_name, save_dir):
    """Generate and save confusion matrix heatmap."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Churn", "Churn"],
                yticklabels=["No Churn", "Churn"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix - {model_name}")
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f"{model_name}_confusion_matrix.png"))
    plt.close()


def plot_classification_report(y_true, y_pred, model_name, save_dir):
    """Save classification report as text file."""
    report = classification_report(y_true, y_pred)
    report_path = os.path.join(save_dir, f"{model_name}_classification_report.txt")
    with open(report_path, "w") as f:
        f.write(report)


def plot_roc_curve(y_true, y_proba, model_name, save_dir):
    """Generate and save ROC curve with AUC score."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color="blue", lw=2, label=f"AUC = {roc_auc:.4f}")
    plt.plot([0, 1], [0, 1], color="red", linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve - {model_name}")
    plt.legend(loc="lower right")

    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f"{model_name}_roc_curve.png"))
    plt.close()

    return roc_auc


def train_and_evaluate():
    """
    Train and evaluate multiple ML models for churn prediction.
    Models: Logistic Regression, Random Forest, Gradient Boosting, SVM, Decision Tree, KNN, XGBoost
    Metrics: Accuracy, Precision, Recall, F1, AUC
    Saves: Best model (.pkl), performance reports, confusion matrices, classification reports, ROC curves
    """

    try:
        # ---------------- Load Data ---------------- #
        data_path = os.path.join("data", "processed", "clean_churn.csv")
        df = pd.read_csv(data_path)

        X = df.drop("Churn", axis=1)   # Features
        y = df["Churn"]               # Target

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # ---------------- Models to Try ---------------- #
        models = {
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
            "GradientBoosting": GradientBoostingClassifier(random_state=42),
            "SVM": SVC(probability=True, random_state=42),
            "DecisionTree": DecisionTreeClassifier(random_state=42),
            "KNN": KNeighborsClassifier(),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
        }

        best_model = None
        best_score = 0
        report_lines = []
        metrics_records = []

        # Directories
        os.makedirs("models", exist_ok=True)
        os.makedirs("reports/plots", exist_ok=True)

        # ---------------- Train & Evaluate ---------------- #
        for name, model in models.items():
            logging.info(f"Training model: {name}")
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            # Predict probabilities for ROC
            if hasattr(model, "predict_proba"):
                y_proba = model.predict_proba(X_test)[:, 1]
            else:  # SVM fallback (uses decision_function)
                y_proba = model.decision_function(X_test)
                y_proba = (y_proba - y_proba.min()) / (y_proba.max() - y_proba.min())

            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds)
            rec = recall_score(y_test, preds)
            f1 = f1_score(y_test, preds)
            auc_score = plot_roc_curve(y_test, y_proba, name, "reports/plots")

            report_lines.append(
                f"{name}: Accuracy={acc:.4f}, Precision={prec:.4f}, Recall={rec:.4f}, F1={f1:.4f}, AUC={auc_score:.4f}"
            )
            logging.info(report_lines[-1])

            metrics_records.append({
                "Model": name,
                "Accuracy": acc,
                "Precision": prec,
                "Recall": rec,
                "F1": f1,
                "AUC": auc_score
            })

            # Save plots and reports
            plot_confusion_matrix(y_test, preds, name, "reports/plots")
            plot_classification_report(y_test, preds, name, "reports/plots")

            if f1 > best_score:  # Select best by F1
                best_score = f1
                best_model = model
                best_name = name

        # ---------------- Save Best Model ---------------- #
        model_path = f"models/{best_name}_churn_model.pkl"
        joblib.dump(best_model, model_path)
        logging.info(f"Saved best model: {best_name} at {model_path}")

        # ---------------- Save Report ---------------- #
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_report_path = f"reports/model_performance_{timestamp}.txt"
        csv_report_path = f"reports/model_performance_{timestamp}.csv"

        with open(txt_report_path, "w") as f:
            f.write("\n".join(report_lines))

        pd.DataFrame(metrics_records).to_csv(csv_report_path, index=False)

        logging.info(f"Model performance reports saved: {txt_report_path}, {csv_report_path}")

        # ---------------- MLflow Logging ---------------- #
        mlflow.set_experiment("ChurnPrediction")
        with mlflow.start_run():
            mlflow.log_params({"best_model": best_name})
            mlflow.log_metrics({
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1,
                "auc": auc_score
            })
            mlflow.sklearn.log_model(best_model, best_name)

        print(f"✅ Training complete. Best model: {best_name}, F1={best_score:.4f}")

    except Exception as e:
        logging.error(f"Error in model training: {str(e)}")
        raise


if __name__ == "__main__":
    train_and_evaluate()
