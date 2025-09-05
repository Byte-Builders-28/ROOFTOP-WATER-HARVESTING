import numpy as np

def predict_dry_spell(location: str, current_date: str) -> tuple[int, float]:
    if location.lower() == "pune":
        return 30, 0.8
    else:
        return 20, 0.7

def calculate_daily_budget(storage_capacity, current_level, dwellers, location, current_date):
    dry_days, confidence = predict_dry_spell(location, current_date)

    base_budget = current_level / dry_days
    safety_margin = 0.75 if confidence < 0.75 else 0.9
    adjusted_budget = base_budget * safety_margin
    per_person = adjusted_budget / dwellers

    # Define tips per usage mode
    tips = {
        "🟢 Liberal Use": [
            "Water level is safe. Still, avoid wastage.",
            "Use stored water for gardening instead of fresh supply.",
            "Check for leaks — small drips add up."
        ],
        "🟡 Recommended Use": [
            "Moderate supply: Use bucket instead of shower.",
            "Collect kitchen rinse water for cleaning floors.",
            "Limit washing machine runs — use full loads only."
        ],
        "🔴 Conservative Use": [
            "Critical level! Prioritize drinking & cooking only.",
            "Postpone car/bike washing until refill.",
            "Store leftover RO water for plants.",
            "If forecast says no rain — alert family members."
        ]
    }

    # Pick mode based on budget
    if per_person >= 100:
        mode = "🟢 Liberal Use"
    elif per_person >= 50:
        mode = "🟡 Recommended Use"
    else:
        mode = "🔴 Conservative Use"

    return {
        "predicted_dry_days": dry_days,
        "confidence": confidence,
        "adjusted_daily_budget": round(adjusted_budget, 2),
        "per_person_budget": round(per_person, 2),
        "mode": mode,
        "suggestions": tips[mode]  # attach relevant tips
    }
