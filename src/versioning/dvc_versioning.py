import os
import subprocess
from datetime import datetime

# ------------------------------
# Helper: run shell commands
# ------------------------------
def run_cmd(cmd):
    """Run shell command with logging"""
    print(f"👉 Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# ------------------------------
# Initialize DVC if not already
# ------------------------------
def init_dvc():
    if not os.path.exists(".dvc"):
        run_cmd("dvc init")
        run_cmd("git add .dvc .gitignore")
        run_cmd('git commit -m "Initialize DVC repository"')
    else:
        print("✅ DVC already initialized.")

# ------------------------------
# Track files with metadata
# ------------------------------
def track_dvc(metadata_dir="src/versioning/metadata"):
    os.makedirs(metadata_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1️⃣ Dynamically find all CSVs in raw_data/
    raw_dir = "raw_data"
    raw_files = [os.path.join(raw_dir, f) for f in os.listdir(raw_dir) if f.endswith(".csv")]

    # 2️⃣ Add merged CSV
    merged_csv = "data/processed/merged_churn.csv"
    files_to_track = [(f, "Raw churn CSV ingested from source") for f in raw_files]
    if os.path.exists(merged_csv):
        files_to_track.append((merged_csv, "Merged churn CSV for preprocessing & modeling"))

    if not files_to_track:
        print("⚠ No files found to track in DVC. Ensure ingestion.py has run.")
        return

    # 3️⃣ Track files and generate metadata
    for file_path, description in files_to_track:
        if os.path.exists(file_path):
            run_cmd(f"dvc add {file_path}")
            base_name = os.path.basename(file_path).replace(".", "_")
            meta_file = os.path.join(metadata_dir, f"{base_name}_version_{ts}.txt")
            with open(meta_file, "w") as f:
                f.write(f"File: {file_path}\n")
                f.write(f"Description: {description}\n")
                f.write(f"Timestamp: {ts}\n")
            print(f"✅ Metadata written: {meta_file}")
        else:
            print(f"⚠ File not found, skipping: {file_path}")

    # 4️⃣ Commit DVC changes and metadata to Git
    run_cmd("git add .")
    run_cmd(f'git commit -m "DVC: data versioning update at {ts}"')

# ------------------------------
# Main execution
# ------------------------------
if __name__ == "__main__":
    init_dvc()
    track_dvc()
