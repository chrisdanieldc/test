# Data Quality Pipeline - Development Log

##  Architecture

```
config/
  └── rules/
      └── remove_duplicates.yml    # Self-contained rule definitions

engine/
  ├── __init__.py
  ├── rule_registry.py             # load_rules() function
  ├── rule_executor.py             # execute_rule() function
  └── audit_logger.py              # log_execution() function

data/
  ├── raw/orders.csv               # Source data
  ├── processed/orders.csv         # Cleaned data
  └── logs/audit.csv               # Audit trail

main.py                            # Simple orchestrator (35 lines)
requirements.txt                   # pandas, pyyaml
```

## How It Works

### 1. Rule Definition (YAML)

Each rule is a **self-contained YAML file** with all configuration:

```yaml
rule_id: DQ-001
rule_name: remove_duplicates
description: Remove duplicate rows from the input dataset.
enabled: true

source:
  file: data/raw/orders.csv

destination:
  file: data/processed/orders.csv

operation:
  type: drop_duplicates

parameters:
  subset: null      # Which columns to check (null = all)
  keep: first       # Which duplicate to keep
```

**Key insight:** Rule knows its source, destination, and operation - fully declarative!

### 2. Engine Functions (Pure Functions)

**`rule_registry.py`** - 26 lines
```python
def load_rules():
    """Loads all .yml files from config/rules/"""
    # Returns list of rule dictionaries
```

**`rule_executor.py`** - 81 lines
```python
def execute_rule(rule):
    """
    Reads source file, applies operation, saves to destination
    Returns execution metadata (rows_before, rows_after, etc.)
    """
    # Supports: drop_duplicates (more operations can be added)
```

**`audit_logger.py`** - 21 lines
```python
def log_execution(audit_record):
    """Appends execution record to data/logs/audit.csv"""
```

### 3. Main Orchestrator (Simple Loop)

```python
rules = load_rules()

for rule in rules:
    if not rule.get("enabled", False):
        continue

    try:
        result = execute_rule(rule)
        log_execution(result)
        print(f"Executed: {rule['rule_name']}")
    except Exception as e:
        print(f"Failed: {rule['rule_name']} - {e}")
```

That's it! No classes, no complexity.

## Adding a New Rule

**Step 1:** Create YAML file (`config/rules/validate_amount.yml`)
```yaml
rule_id: DQ-002
rule_name: validate_amount
description: Ensure amount is positive
enabled: true

source:
  file: data/processed/orders.csv

destination:
  file: data/processed/orders.csv

operation:
  type: filter_positive

parameters:
  column: amount
  min_value: 0
```

**Step 2:** Add operation to `rule_executor.py`
```python
def execute_rule(rule):
    # ... existing code ...

    if operation == "drop_duplicates":
        df = df.drop_duplicates(...)

    elif operation == "filter_positive":  # Add this
        column = parameters.get("column")
        min_value = parameters.get("min_value", 0)
        df = df[df[column] >= min_value]

    else:
        raise ValueError(f"Unsupported operation: {operation}")
```

**Step 3:** Run pipeline
```bash
python main.py
```

Done! No need to touch main.py or other files.

## Current Data

**Source:** `data/raw/orders.csv`
- 7 rows (1 duplicate found)
- Duplicate: order_id 3 (Carol, 80.00)

**After Processing:** `data/processed/orders.csv`
- 6 rows (duplicate removed)
- Added metadata: `rule_id`, `run_id`, `run_timestamp`

## CI/CD

**Workflow:** `.github/workflows/clean-data.yml`

**Triggers:**
- Push to main when `data/raw/orders.csv` changes
- Manual dispatch

**Steps:**
1. Install dependencies: `pip install -r requirements.txt`
2. Run pipeline: `python main.py`
3. Commit cleaned data and audit log
4. Upload artifact

## Design Principles

✅ **Simplicity First**
- Functions, not classes
- No inheritance, no abstractions
- 35-line main.py

✅ **Declarative Config**
- Rules are self-contained YAML
- Source/destination in config, not hardcoded
- Easy to read and understand

✅ **Functional Approach**
- Pure functions with clear inputs/outputs
- No global state
- Easy to test

✅ **Human Readable**
- ~150 lines total engine code
- No magic, no frameworks
- Anyone can understand it

## Key Decisions

**Why functional instead of classes?**
- Simpler, fewer lines of code
- No need for object state
- Easier to understand flow

**Why source/destination in YAML?**
- Rules are self-contained
- Can process different files with same operation
- More flexible

**Why operation types?**
- Easy to add new operations
- Clear separation of what vs. how
- Extensible without complexity

**Why no unit tests yet?**
- Keep it simple first
- Add tests when needed
- Can test functions easily (they're pure)

## File Locations

**Config:** `config/rules/*.yml`
- Each rule is independent YAML file
- Place in `config/rules/` directory
- Loaded automatically by `load_rules()`

**Engine:** `engine/*.py`
- `rule_registry.py` - Discovers and loads rules
- `rule_executor.py` - Executes operations on data
- `audit_logger.py` - Logs execution history

**Data:** `data/*`
- `raw/` - Source data (input)
- `processed/` - Cleaned data (output)
- `logs/` - Audit trail (CSV)

**Entry Point:** `main.py`
- Simple 35-line orchestrator
- Loads → Execute → Log → Print

## Usage

**Local execution:**
```bash
python main.py
```

**Output:**
```
Executed: remove_duplicates
```

**Check results:**
- Cleaned data: `data/processed/orders.csv`
- Audit log: `data/logs/audit.csv`

## Dependencies

```
pandas>=2.0.0   # DataFrame operations
pyyaml>=6.0     # YAML parsing
```

Install: `pip install -r requirements.txt`

## Common Issues

**Issue:** `load_rules()` returns empty list in notebook
**Solution:** Don't use `~` in paths. Use relative path `"config/rules"` not `"~/Users/..."`

**Issue:** Module not found errors
**Solution:** Run from project root, install dependencies: `pip install -r requirements.txt`

## Future Enhancements

- [ ] Add more operations (filter, validate, transform)
- [ ] Support multiple file formats (JSON, Excel)
- [ ] Add dry-run mode
- [ ] Generate execution reports
- [ ] Add unit tests
- [ ] Support rule dependencies (run in order)
