from fastapi import APIRouter, HTTPException, Depends
from app.database import database
from app.models import Node, Edge
from typing import List, Dict

router = APIRouter()

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
