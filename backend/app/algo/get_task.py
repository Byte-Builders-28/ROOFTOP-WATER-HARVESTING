# services/rainfall_engine.py

def estimate_rainwater_potential(area_m2, rainfall_mm, coefficient=0.8):
	"""Estimate annual harvestable rainwater (liters)."""
	return area_m2 * rainfall_mm * coefficient * 0.001  # mm*m² = liters


def estimate_water_demand(population, usage_per_day=135):
	"""Estimate annual water demand (liters)."""
	return population * usage_per_day * 365


def estimate_tank_size(potential, demand):
	"""Suggest tank size (liters)."""
	return min(potential, demand)


def estimate_cost(tank_size, cost_per_liter=2.5):
	"""Rough cost based on tank size."""
	return tank_size * cost_per_liter


def feasibility_score(potential, demand, cost, budget=None):
	"""Return a simple feasibility score (0-100)."""
	score = 0
	if potential >= 0.8 * demand:
		score += 40
	elif potential >= 0.5 * demand:
		score += 20

	if budget and cost <= budget:
		score += 30
	else:
		score += 10

	# Normalize
	return min(score, 100)
