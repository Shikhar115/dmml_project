import logging

logging.basicConfig(filename="ingestion.log", level=logging.INFO)

def export_to_feast_csv():
    """
    Export engineered features from SQLite (transformed_churn.db)
    to a CSV file (transformed_churn.csv) for the Feast feature store.
    """
    import sqlite3
    import pandas as pd
    from datetime import datetime

    con = sqlite3.connect("transformed_churn.db")
    df = pd.read_sql_query("SELECT * FROM customer_features", con)
    df["event_timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv("transformed_churn.csv", index=False)
    con.close()

    logging.info("Exported engineered features to transformed_churn.csv")
