from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.reports import ReportCreate, ReportResponse
from app.services.reporting_service import reporting_service

router = APIRouter()

@router.post("/reports", response_model=dict)
async def submit_report(report: ReportCreate):
    report_id = await reporting_service.create_report(report)
    return {"id": report_id, "status": "received", "message": "Thank you for your report. It will be verified."}

@router.get("/reports/recent")
async def get_recent_reports():
    return await reporting_service.get_recent_reports()
