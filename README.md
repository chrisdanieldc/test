# Data Quality Pipeline

Clean, modular data quality engine for CSV processing.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Architecture

```
config/
  └── rules/
      └── remove_duplicates.yml    # Rule definitions (WHAT to run)

engine/
  ├── rule_registry.py             # Loads rules from config
  ├── rule_executor.py             # Rule implementations (HOW to do it)
  └── audit_logger.py              # Tracks execution history

main.py                            # Pipeline orchestrator
```

## Adding New Rules

**1. Define rule config** (`config/rules/my_rule.yml`):
```yaml
id: DQ-002
name: validate_amount
enabled: true
description: Ensure amount is positive
params:
  min_value: 0
```

**2. Implement rule** (`engine/rule_executor.py`):
```python
def validate_amount(self, df, params):
    min_value = params.get('min_value', 0)
    # Your validation logic here
    return df
```

**3. Register in executor**:
```python
self.rule_functions = {
    'remove_duplicates': self.remove_duplicates,
    'validate_amount': self.validate_amount,  # Add here
}
```

**4. Run pipeline**: `python main.py`

## Current Rules

- **DQ-001**: Remove duplicate rows

## Data Flow

```
data/raw/orders.csv
    ↓ [rules applied]
data/processed/orders.csv
    ↓ [audit trail]
data/logs/audit.csv
```

## CI/CD

- **Trigger:** Changes to `data/raw/orders.csv` on main branch
- **Action:** Auto-runs pipeline and commits cleaned data

## See Also

- `CLAUDE.md` - Full documentation and design decisions
