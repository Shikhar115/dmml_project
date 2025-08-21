import os
import subprocess
from datetime import datetime

def run_cmd(cmd):
    """Run shell command with logging"""
    print(f"👉 Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def setup_dvc():
    # Initialize DVC repo (idempotent)
    if not os.path.exists(".dvc"):
        run_cmd("dvc init")

    # Create metadata folder
    os.makedirs("metadata", exist_ok=True)

    # Add raw data to DVC
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = "./raw_data/raw_churn.csv"
    clean_file = "./clean_churn.csv"

    if os.path.exists(raw_file):
        run_cmd(f"dvc add {raw_file}")
        with open(f"metadata/raw_version_{ts}.txt", "w") as f:
            f.write(f"Raw data added at {ts}\nSource: churn CSV\n")

    if os.path.exists(clean_file):
        run_cmd(f"dvc add {clean_file}")
        with open(f"metadata/clean_version_{ts}.txt", "w") as f:
            f.write(f"Clean data added at {ts}\nTransformation: preprocessing\n")

    # Commit changes to Git
    run_cmd("git add .")
    run_cmd(f'git commit -m "Data versioning update at {ts}"')

if __name__ == "__main__":
    setup_dvc()
