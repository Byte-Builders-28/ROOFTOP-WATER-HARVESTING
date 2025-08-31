def dynamic_coefficient(base, humidity):
    """
    Adjust collection efficiency based on humidity (0-100%).
    High humidity → less evaporation → higher efficiency.
    """
    # Normalize humidity to 0-1
    h = humidity / 100.0
    # Scale between base*0.7 (dry) and base*1.1 (humid)
    return max(0, min(1, base * (0.7 + 0.4 * h)))


def evaporation_loss(temp, days, surface_area):
    """
    Estimate evaporation loss (liters) based on temp (°C),
    days in month, and water surface area (m²).
    """
    # Simple empirical rate: higher temp → higher evaporation
    # Evap (mm/day) ≈ 0.5 + 0.05 * (temp - 20)
    evap_rate_mm_day = max(0, 0.5 + 0.05 * (temp - 20))
    evap_mm = evap_rate_mm_day * days
    # mm * m² = liters
    return evap_mm * surface_area


def simulate_system_mounth(
    monthly_rainfall, monthly_temp, monthly_humidity,
    area_m2, population, usage_per_day=135,
    tank_capacity=20000, groundwater_capacity=50000,
    soil_infiltration=0.5  # 0-1 fraction
):
    """Simulate integrated rainwater harvesting + groundwater recharge."""

    demand_monthly = usage_per_day * population * 30
    tank_level, gw_level = 0, groundwater_capacity * 0.5  # start at half full
    total_supply, unmet, reliability = 0, 0, 0

    for m in range(12):
        # Rainwater collected
        efficiency = dynamic_coefficient(0.8, monthly_humidity[m])
        rain_collected = monthly_rainfall[m] * area_m2 * efficiency * 0.001

        # Evaporation loss (tank surface ~10% of area)
        evap = evaporation_loss(monthly_temp[m], 30, area_m2 * 0.1)
        rain_collected = max(0, rain_collected - evap)

        # Add to tank
        tank_level += rain_collected

        # If overflow, recharge groundwater
        if tank_level > tank_capacity:
            recharge = (tank_level - tank_capacity) * soil_infiltration
            gw_level = min(groundwater_capacity, gw_level + recharge)
            tank_level = tank_capacity

        # Meet demand
        if tank_level >= demand_monthly:
            tank_level -= demand_monthly
            total_supply += demand_monthly
            reliability += 1
        else:
            demand_left = demand_monthly - tank_level
            total_supply += tank_level
            tank_level = 0

            if gw_level >= demand_left:
                gw_level -= demand_left
                total_supply += demand_left
                reliability += 1
            else:
                total_supply += gw_level
                unmet += demand_left - gw_level
                gw_level = 0

    reliability_ratio = reliability / 12
    demand_total = demand_monthly * 12
    return total_supply, demand_total, reliability_ratio, unmet, gw_level

def simulate_system_annual(
    avg_rainfall,  # mm/year
    avg_temp,      # °C
    avg_humidity,  # %
    area_m2,
    population,
    usage_per_day=135,
    tank_capacity=20000,
    groundwater_capacity=50000,
    soil_infiltration=0.5
):
    """Simulate rainwater harvesting + groundwater recharge using annual averages (no loop)."""

    # Total annual demand
    days = 365
    demand_total = usage_per_day * population * days

    # Rainwater collected over the year
    efficiency = dynamic_coefficient(0.8, avg_humidity)
    rain_collected = avg_rainfall * area_m2 * efficiency * 0.001  # mm*m² → liters

    # Evaporation loss (tank surface ~10% of area)
    evap = evaporation_loss(avg_temp, days, area_m2 * 0.1)
    rain_collected = max(0, rain_collected - evap)

    # Start tank and groundwater
    tank_level = rain_collected
    gw_level = groundwater_capacity * 0.5

    # Handle tank overflow
    if tank_level > tank_capacity:
        recharge = (tank_level - tank_capacity) * soil_infiltration
        gw_level = min(groundwater_capacity, gw_level + recharge)
        tank_level = tank_capacity

    # Supply demand from tank first
    if tank_level >= demand_total:
        tank_level -= demand_total
        total_supply = demand_total
        unmet = 0
        reliability_ratio = 1
    else:
        demand_left = demand_total - tank_level
        total_supply = tank_level
        tank_level = 0

        if gw_level >= demand_left:
            gw_level -= demand_left
            total_supply += demand_left
            unmet = 0
            reliability_ratio = 1
        else:
            total_supply += gw_level
            unmet = demand_left - gw_level
            gw_level = 0
            reliability_ratio = total_supply / demand_total

    return total_supply, demand_total, reliability_ratio, unmet, gw_level
