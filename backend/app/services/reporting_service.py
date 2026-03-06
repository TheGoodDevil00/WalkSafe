from app.database import database
from app.schemas.reports import ReportCreate
from datetime import datetime

class ReportingService:
    def __init__(self):
        # Configuration for scoring
        self.base_confidence = 0.5

    async def create_report(self, report: ReportCreate) -> int:
        # TODO: Implement Rate Limiting Check
        # TODO: Check for nearby recent duplicate reports (Corroboration)
        
        query = """
        INSERT INTO user_reports (user_hash, location, incident_type, confidence_score, timestamp)
        VALUES (:user_hash, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326), :incident_type, :confidence, NOW())
        RETURNING id
        """
        values = {
            "user_hash": report.user_hash,
            "lon": report.lon,
            "lat": report.lat,
            "incident_type": report.incident_type,
            "confidence": self.base_confidence
        }
        
        report_id = await database.execute(query=query, values=values)
        return report_id
    
    async def get_recent_reports(self):
        query = "SELECT id, ST_X(location::geometry) as lon, ST_Y(location::geometry) as lat, incident_type, confidence_score FROM user_reports ORDER BY timestamp DESC LIMIT 50"
        return await database.fetch_all(query)

reporting_service = ReportingService()
