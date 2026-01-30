def rule_based_prediction(cpu, ram, disk):
    """
    Rule-based fallback prediction
    Returns:
    0 -> Normal
    1 -> High Load
    2 -> Hang Risk
    """

    if cpu > 85 and ram > 85:
        return 2   # Hang Risk

    if cpu > 65 or ram > 75:
        return 1   # High Load

    return 0       # Normal
