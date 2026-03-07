from fastapi import APIRouter, HTTPException, Depends
from app.database import database
from app.models import Node, Edge
from typing import List, Dict

from app.services.risk_engine import RiskEngine
from app.services.safety_index import nearest_segment

router = APIRouter()
risk_engine = RiskEngine()

@router.get("/route", response_model=Dict[str, List[Dict]])
async def get_routes(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    """
    Returns multiple routes: Safest, Fast, Balanced.
    Currently returns mock data until A* is implemented.
    """
    # TODO: Implement actual A* or Dijkstra on PostGIS pgRouting
    return {
        "safest": [
            {"lat": start_lat, "lon": start_lon},
            {"lat": (start_lat + end_lat)/2, "lon": (start_lon + end_lon)/2}, 
            {"lat": end_lat, "lon": end_lon}
        ],
        "fastest": [
            {"lat": start_lat, "lon": start_lon},
            {"lat": end_lat, "lon": end_lon}
        ]
    }


@router.get("/route/safety")
async def get_route_safety(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    """
    Returns a simple mock route annotated with safety scores and risk per segment.

    This uses the precomputed safety dataset (GeoJSON + spatial index) and the
    global risk formula: risk = distance_weight + (100 - safety_score).
    """
    # For now we mirror the mock "safest" route shape from /route.
    path = [
        {"lat": start_lat, "lon": start_lon},
        {"lat": (start_lat + end_lat) / 2.0, "lon": (start_lon + end_lon) / 2.0},
        {"lat": end_lat, "lon": end_lon},
    ]

    segments: List[Dict] = []
    total_distance = 0.0
    total_risk = 0.0

    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]

        # Query safety at the segment midpoint.
        mid_lat = (start["lat"] + end["lat"]) / 2.0
        mid_lon = (start["lon"] + end["lon"]) / 2.0

        segment_row, distance_to_query = nearest_segment(lat=mid_lat, lon=mid_lon)

        safety_score = float(segment_row.get("safety_score", 50.0))
        segment_distance = float(segment_row.get("distance", 0.0))

        segment_risk = risk_engine.calculate_segment_risk(
            distance_weight=segment_distance,
            safety_score=safety_score,
        )

        total_distance += segment_distance
        total_risk += segment_risk

        segments.append(
            {
                "start": start,
                "end": end,
                "segment_id": segment_row.get("segment_id"),
                "safety_score": safety_score,
                "distance": segment_distance,
                "distance_to_query_meters": round(distance_to_query, 2),
                "risk": segment_risk,
            }
        )

    return {
        "segments": segments,
        "summary": {
            "total_distance": total_distance,
            "total_risk": total_risk,
        },
    }
