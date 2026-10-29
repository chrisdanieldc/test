# Orders CSV - Duplicate Removal

Simple project to remove duplicate rows from `orders.csv`.

## Quick Start

**Remove duplicates manually:**
```bash
python3 remove_duplicates.py
```

**What it does:**
- Reads `data/raw/orders.csv`
- Removes duplicate rows (keeps first occurrence)
- Saves cleaned data to `data/processed/orders_clean.csv`

## Files

```
data/raw/orders.csv              → Source data (may have duplicates)
data/processed/orders_clean.csv  → Cleaned data (no duplicates)
remove_duplicates.py             → Script to remove duplicates
```

## CI/CD

- **Pull Requests:** CI checks for duplicates, fails if found
- **Main Branch:** CD auto-removes duplicates and commits cleaned file

## See Also

- `CLAUDE.md` - Detailed documentation and decision log
