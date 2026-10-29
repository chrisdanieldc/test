import pandas as pd
import uuid
from datetime import datetime
import os

df = pd.read_csv("data/raw/orders.csv")

rows_before = len(df)


# Rule information
rule_id = "DQ-001"
rule_name = "remove_duplicates"

# Remove duplicate rows
df = df.drop_duplicates()

# Count rows after deduplication
rows_after = len(df)
duplicates_removed = rows_before - rows_after

df["rule_id"] = rule_id
df["run_id"] = str(uuid.uuid4())
df["run_timestamp"] = datetime.now().timestamp()

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/orders.csv", index=False)


# Create an audit record
audit = pd.DataFrame([{
    "rule_id": rule_id,
    "rule_name": rule_name,
    "run_id": df["run_id"].iloc[0],
    "timestamp": df["run_timestamp"].iloc[0],
    "input_file": "data/raw/orders.csv",
    "output_file": "data/processed/orders.csv",
    "rows_before": rows_before,
    "rows_after": rows_after,
    "duplicates_removed": duplicates_removed,
    "status": "SUCCESS"
}])


# Save the audit log
os.makedirs("data/logs", exist_ok=True)

audit_file = "data/logs/audit.csv"

audit.to_csv(
    audit_file,
    mode="a",
    header=not os.path.exists(audit_file),
    index=False
)