

from  .sim_rainwater import dynamic_coefficient, evaporation_loss, simulate_system_annual

def estimate_rainwater_potential(area_m2, rainfall_mm, humidity, temp, coefficient=0.8):
    """Estimate annual harvestable rainwater (liters) considering humidity & evaporation."""
    efficiency = dynamic_coefficient(coefficient, humidity)
    rain_collected = area_m2 * rainfall_mm * efficiency

    # evaporation loss (tank surface ≈ 10% of roof area, assume 365 days)
    evap = evaporation_loss(temp, 365, area_m2 * 0.1)
    return max(0, rain_collected - evap)


def estimate_water_demand(population, usage_per_day=135):
    """Estimate annual water demand (liters)."""
    return population * usage_per_day * 365


def estimate_tank_size(potential, demand):
    """Suggest tank size (liters)."""
    return min(potential, demand)


def estimate_cost(tank_size, cost_per_liter=2.5):
    """Rough cost based on tank size."""
    return tank_size * cost_per_liter


def feasibility_score(area_m2, rainfall_mm, temp, humidity, population,
                      budget=None, tank_capacity=20000, groundwater_capacity=50000):
    """
    Compute feasibility using the detailed annual simulation.
    Returns a score (0-100) and key stats.
    """
    total_supply, demand_total, reliability_ratio, unmet, gw_left = simulate_system_annual(
        avg_rainfall=rainfall_mm,
        avg_temp=temp,
        avg_humidity=humidity,
        area_m2=area_m2,
        population=population,
        tank_capacity=tank_capacity,
        groundwater_capacity=groundwater_capacity
    )

    cost = estimate_cost(tank_capacity)

    score = 0
    # Supply vs demand
    if total_supply >= 0.8 * demand_total:
        score += 40
    elif total_supply >= 0.5 * demand_total:
        score += 20

    # Reliability
    if reliability_ratio >= 0.9:
        score += 30
    elif reliability_ratio >= 0.7:
        score += 20
    else:
        score += 10

    # Budget
    if budget and cost <= budget:
        score += 30
    else:
        score += 10

    return {
        "score": min(score, 100),
        "supply": total_supply,
        "demand": demand_total,
        "unmet": unmet,
        "reliability": reliability_ratio,
        "cost_estimate": cost,
        "gw_left": gw_left
    }

def recommend_system(area_m2, rainfall_mm, temp, humidity, population,
                     budget=None, tank_capacity=None, groundwater_capacity=50000):

    # Step 1: estimate potential & demand
    potential = estimate_rainwater_potential(area_m2, rainfall_mm, humidity, temp)
    demand = estimate_water_demand(population)

    # Step 2: estimate required tank size if not provided
    # if not tank_capacity:
    tank_capacity = estimate_tank_size(potential, demand)

    # Step 3: get feasibility with this tank size
    result = feasibility_score(area_m2, rainfall_mm, temp, humidity,
                               population, budget, tank_capacity, groundwater_capacity)

    supply = result["supply"]
    gw_left = result["gw_left"]

    # Step 4: decision rules
    if supply >= demand * 0.9:
        system_type = "storage"
        reason = "Rainwater supply can meet most of the demand."
    elif gw_left < groundwater_capacity * 0.5:
        system_type = "recharge"
        reason = "Groundwater is being overused, recharge is needed."
    else:
        system_type = "hybrid"
        reason = "Rainwater alone is not enough; recharge + storage recommended."

    # Final output
    result.update({
        "system_type": system_type,
        "reason": reason,
        "tank_size": tank_capacity,
        # "cost_estimate": estimate_cost(tank_capacity)
    })

    return result

