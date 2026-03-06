from datetime import datetime, timedelta
from typing import List, Dict

class RiskEngine:
    def __init__(self):
        # Configuration weights
        self.w_lighting = 0.4
        self.w_crime = 0.4
        self.w_crowd = 0.2
        self.decay_halflife_hours = 24.0

    def calculate_edge_risk(self, edge_data: Dict, current_time: datetime = None) -> float:
        """
        Calculates a risk score between 0.0 (Safe) and 1.0 (Dangerous)
        """
        if current_time is None:
            current_time = datetime.now()

        # 1. Static Factors
        lighting_risk = edge_data.get('lighting_score', 0.5) # Default to medium if unknown
        base_risk = edge_data.get('base_risk_score', 0.0)

        # 2. Dynamic Factors (Incidents)
        # In a real system, we'd query recent incidents near this edge here
        # For now, we assume edge_data might have a 'recent_incident_severity' field pre-aggregated
        incident_severity = edge_data.get('recent_incident_severity', 0)
        incident_time_hours_ago = edge_data.get('hours_since_incident', 9999)
        
        # Time Decay: Risk = InitialRisk * (0.5 ^ (t / half_life))
        incident_risk = 0.0
        if incident_severity > 0:
            normalized_severity = min(incident_severity / 5.0, 1.0)
            decay_factor = 0.5 ** (incident_time_hours_ago / self.decay_halflife_hours)
            incident_risk = normalized_severity * decay_factor

        # 3. Crowd / Time of Day (Simple heuristic: Night is riskier if lighting is poor)
        hour = current_time.hour
        is_night = hour < 6 or hour > 19
        night_multiplier = 1.2 if is_night and lighting_risk > 0.6 else 1.0

        # Weighted Sum
        total_risk = (
            (lighting_risk * self.w_lighting) +
            (incident_risk * self.w_crime) + 
            (base_risk * 0.2) # Base risk component
        ) * night_multiplier

        return min(max(total_risk, 0.0), 1.0)
