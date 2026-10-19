
def detect_conflicts(claims: list[dict]) -> list[dict]:
    conflicts = []

    for i, first in enumerate(claims):
        for second in claims[i + 1:]:
            same_metric = (
                first.get("metric") == second.get("metric")
            )

            different_values = (
                first.get("value") != second.get("value")
            )

            if same_metric and different_values:
                conflicts.append({
                    "metric": first.get("metric"),
                    "claim_1": first,
                    "claim_2": second,
                    "message": (
                        "Conflicting values found. "
                        "Check report scope, year, and methodology."
                    ),
                })

    return conflicts
