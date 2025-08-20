# Data Versioning Workflow with DVC + Git

This document explains how we apply **data versioning** for churn datasets.

---

## Why?
- Ensure reproducibility of experiments
- Track changes in raw & transformed data
- Allow easy rollback to older versions

---

## Tools
- **Git** → version control for code + metadata
- **DVC** → version control for datasets & models

---

## Workflow

1. **Initialize DVC (one-time setup)**
```bash
git init
dvc init
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```

2. **Track a dataset**
```bash
dvc add raw_data/raw_churn_csv_20250820.csv
git add raw_data/raw_churn_csv_20250820.csv.dvc .gitignore
git commit -m "Add raw churn dataset (CSV)"
```

3. **Track transformed data**
```bash
dvc add clean_churn_csv.csv
dvc add transformed_churn.db
git add *.dvc .gitignore
git commit -m "Add cleaned + transformed churn datasets"
```

4. **Push data to remote storage (optional)**
```bash
dvc remote add -d myremote gdrive://<folder-id>   # example
dvc push
```

5. **Update datasets**
- Re-run pipeline (Airflow) → generates new CSV/DB
- Run `dvc add` again → creates new version
- Update `CHANGELOG.md` with description of change
- Commit changes:
```bash
git add CHANGELOG.md
git commit -m "Update dataset to v1.1.0 with August churn data"
dvc push
```

---

## Versioning Strategy
- **Raw data** is tracked exactly as ingested
- **Cleaned + transformed datasets** are also versioned
- Each dataset update = new entry in `CHANGELOG.md`
- Use Git tags to mark dataset releases:
```bash
git tag -a v1.1.0 -m "Dataset version 1.1.0"
git push origin v1.1.0
```

---

## Example
- `v1.0.0` = Initial dataset (CSV + API)
- `v1.1.0` = Added new monthly churn data
- `v2.0.0` = Major schema change in features
