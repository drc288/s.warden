from src.modules.incidents.domain.entities import Incident
from src.modules.incidents.presentation.schemas import IncidentResponse


async def incident_to_response(incident: Incident) -> IncidentResponse:
    return IncidentResponse(
        id=incident.id,
        description=incident.description,
        severity=incident.severity,
        created_at=incident.timestamp
    )