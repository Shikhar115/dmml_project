# Data Versioning Strategy

## Why Version Data?
- Ensures reproducibility of experiments
- Tracks changes in raw and transformed datasets
- Provides metadata (timestamp, source, change log)

## Tools Used
- **Git** → Tracks code, metadata, and `.dvc` files
- **DVC** → Manages large raw/processed datasets without storing them directly in Git

## Workflow
1. Initialize repository:
   ```bash
   git init
   dvc init
