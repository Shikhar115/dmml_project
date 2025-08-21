📦 Data Versioning Strategy

This project uses DVC (Data Version Control) together with Git to version raw and transformed datasets. This ensures reproducibility, auditability, and traceability of all data changes.

🔄 Workflow
1. Initialize Git & DVC
git init
dvc init

2. Add Local DVC Storage

We use local storage to avoid storing large data files in GitHub.

dvc remote add -d local_storage C:/Users/shikh/Desktop/dvc_storage

3. Version Raw Data
dvc add ./raw_data
git add raw_data.dvc .gitignore
git commit -m "Track raw data with DVC"

4. Version Transformed Data
dvc add clean_churn_csv.csv clean_churn_api.csv
git add clean_churn_csv.csv.dvc clean_churn_api.csv.dvc
git commit -m "Track cleaned/transformed data with DVC"

5. Push Data to Remote Storage
dvc push


This ensures dataset files are stored safely in C:/Users/shikh/Desktop/dvc_storage, while Git only tracks metadata.

📑 Metadata Stored

Each .dvc file contains:

MD5 hash (unique fingerprint of the file)

File size

Path reference

Timestamp (from commit history)

This allows us to reproduce any dataset version exactly.

✅ Deliverables

Git + DVC repository: Shows dataset versions, changes, and history.

Local storage (dvc_storage/): Stores actual dataset files.

This document: Explains versioning workflow and strategy.

👉 With this setup:

Raw data and cleaned/transformed data are fully versioned.

Any past dataset version can be reproduced by checking out the corresponding Git commit and running:

dvc pull
