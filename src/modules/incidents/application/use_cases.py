from src.modules.incidents.application.interfaces import IReasoningEngine, IIncidentRepository
from src.modules.incidents.domain.entities import Incident


class IncidentUseCases:
    def __init__(self, incident_repository: IIncidentRepository):
        self.repository = incident_repository

    async def register(self, description: str, severity: str) -> Incident:
        incident = Incident(description=description, severity=severity)
        return await self.repository.save(incident)
