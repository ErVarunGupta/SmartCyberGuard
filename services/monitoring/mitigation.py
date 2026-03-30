# core/mitigation.py

def get_auto_mitigation_suggestions(cpu, ram, disk, pred, battery_pct):
    suggestions = []

    if ram > 80:
        suggestions.append(
            "Close unused browser tabs or restart the browser."
        )

    if cpu > 75:
        suggestions.append(
            "Close background applications or restart heavy apps."
        )

    if disk > 85:
        suggestions.append(
            "Free up disk space or clear temporary files."
        )

    if pred == 2:
        suggestions.append(
            "Save your work immediately and avoid opening new applications."
        )
        suggestions.append(
            "Consider restarting the system to stabilize performance."
        )

    if battery_pct != -1 and battery_pct < 20:
        suggestions.append(
            "Enable power saver mode or plug in the charger."
        )

    if not suggestions:
        suggestions.append(
            "System is stable. No immediate action required."
        )

    return suggestions
