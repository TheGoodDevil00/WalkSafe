from fastapi import APIRouter, HTTPException, Depends
from app.database import database
from app.models import Node, Edge
from typing import List, Dict

from pydantic import BaseModel

from app.services.risk_engine import RiskEngine


router = APIRouter()
risk_engine = RiskEngine()


class Coordinate(BaseModel):
    lat: float
    lon: float


class RouteCoordinates(BaseModel):
    coordinates: List[Coordinate]


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
    Returns a simple mock route annotated with safety scores and risk per segment,
    using the dummy safety dataset and the global risk formula:

        risk = distance_weight + (100 - safety_score)
    """
    # For now we mirror the mock "safest" route shape from /route.
    path = [
        {"lat": start_lat, "lon": start_lon},
        {"lat": (start_lat + end_lat) / 2.0, "lon": (start_lon + end_lon) / 2.0},
        {"lat": end_lat, "lon": end_lon},
    ]

    return risk_engine.score_route(path)


@router.post("/route/risk")
async def score_osrm_route(body: RouteCoordinates):
    """
    Accepts a decoded OSRM route polyline (list of coordinates) and returns
    per-segment safety metrics + aggregate risk using the dummy safety dataset.
    """
    coordinates = [{"lat": c.lat, "lon": c.lon} for c in body.coordinates]
    return risk_engine.score_route(coordinates)
