from engine.rule_registry import load_rules

from engine.rule_executor import execute_rule

from engine.audit_logger import log_execution


# Load rules from registry

rules = load_rules()


# Execute enabled rules

for rule in rules:

    if not rule.get("enabled", False):

        continue

    try:

        result = execute_rule(rule)

        log_execution(result)

        print(
            f"Executed: {rule['rule_name']}"
        )

    except Exception as e:

        print(
            f"Failed: {rule['rule_name']} - {e}"
        )