def get_health_score(temp, speed):
    """
    Abhirami's Advanced Fuzzy Logic Combinatorial Inference Algorithm.
    Calculates dynamic engine fire threat metrics based on combinatorial parameter matrices.
    """
    # 1. Evaluate Target Heat Membership Curves
    if temp < 80:
        temp_weight = 0.0
    elif temp < 100:
        temp_weight = (temp - 80) / 20.0
    else:
        temp_weight = 1.0 + ((temp - 100) / 50.0)

    # 2. Evaluate Velocity Airflow Draft Dispersal Bounds
    if speed > 40:
        draft_efficiency = 1.0
    elif speed > 10:
        draft_efficiency = (speed - 10) / 30.0
    else:
        draft_efficiency = 0.0 

    # 3. Multi-Variable Output Inferences Integration Logic
    raw_risk = temp_weight * (1.0 - draft_efficiency) * 100.0

    return min(max(raw_risk, 5.0), 99.5)