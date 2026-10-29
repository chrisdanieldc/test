# Orders CSV Duplicate Removal - Simple Approach

## Goal
Remove duplicates from `data/raw/orders.csv` when CI/CD runs.

## Current Data
**File:** `data/raw/orders.csv`
```csv
order_id,customer,amount,order_date,country,status
1,Alice,120.50,2026-01-05,in,paid
2,Bob,,2026-01-06,US,paid
3,Carol,80.00,2026-01-06,in,paid
3,Carol,80.00,2026-01-06,in,paid  ← DUPLICATE
4,Dave,-15.00,2026-01-07,UK,refunded
5,Erin,200.00,2026-01-08,us,paid
6,Frank,45.25,2026-01-08,IN,pending
```

**Identified Duplicates:**
- Row 5 is exact duplicate of row 4 (order_id 3)

## What We Did

### ✅ Step 1: Manual Approach (COMPLETED)
1. ✅ Created simple Python script `remove_duplicates.py`
2. ✅ Reads CSV, removes exact duplicates, keeps first occurrence
3. ✅ Saves cleaned version to `data/processed/orders_clean.csv`
4. ✅ Tested manually - found and removed 1 duplicate!

### ✅ Step 2: CI/CD Approach (COMPLETED)
1. ✅ **CI (Pull Requests):** `.github/workflows/check-duplicates.yml` - Fails if duplicates exist
2. ✅ **CD (Main branch):** `.github/workflows/clean-data.yml` - Auto-removes duplicates and commits

### ✅ Step 3: Cleanup (COMPLETED)
Deleted overcomplicated files:
- ✅ `engine/` folder (rule engine - too complex)
- ✅ `rules/` folder (registry system - unnecessary)
- ✅ `tests/` folder (engine tests)
- ✅ `requirements.txt` (unnecessary dependencies)
- ✅ `.github/workflows/ci.yml` (complex CI)
- ✅ `.github/workflows/cd.yml` (complex CD)

Kept:
- ✅ `data/raw/orders.csv` (source data)
- ✅ `remove_duplicates.py` (simple script)
- ✅ Simple CI/CD workflows

## Current Structure
```
.
├── CLAUDE.md                               # This file - tracks everything
├── README.md                               # Simple instructions
├── remove_duplicates.py                    # Script to remove duplicates
├── data/
│   ├── raw/
│   │   └── orders.csv                      # Source data (may have duplicates)
│   └── processed/
│       └── orders_clean.csv                # Cleaned data (no duplicates)
└── .github/workflows/
    ├── check-duplicates.yml                # CI: Fails if duplicates found in PR
    └── clean-data.yml                      # CD: Auto-cleans on main branch
```

## How It Works

### Manual Usage
```bash
python3 remove_duplicates.py
```
- Reads `data/raw/orders.csv`
- Removes duplicate rows (keeps first occurrence)
- Writes to `data/processed/orders_clean.csv`
- Exits with code 1 if duplicates found, 0 if clean

### CI/CD Workflow
1. **On Pull Request:** CI runs and checks for duplicates
   - If duplicates exist → CI fails ❌
   - If no duplicates → CI passes ✅

2. **On Merge to Main:** CD runs automatically
   - Removes any duplicates
   - Commits cleaned file back to repo
   - Creates downloadable artifact

## Test Results (Manual Run)
```
============================================================
Removing duplicates from orders.csv
============================================================

  Duplicate found (line 5): 3,Carol,80.00,2026-01-06,in,paid

✓ Processed data/raw/orders.csv
  Total rows (excluding header): 7
  Duplicates removed: 1
  Unique rows: 6
  Output: data/processed/orders_clean.csv

⚠️  Warning: Duplicates were found and removed!
```

## Notes
- **Simple:** Just removes exact duplicate rows, nothing fancy
- **Keeps first:** First occurrence stays, subsequent duplicates removed
- **No dependencies:** Pure Python, no pip packages needed
- **Human readable:** Clear code that anyone can understand
- **Automatic:** CI/CD handles it after merge to main
