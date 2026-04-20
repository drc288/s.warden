from src.modules.incidents.application.interfaces import IIncidentRepository
from src.modules.incidents.domain.entities import Incident, Decision


class InMemoryIncidentRepository(IIncidentRepository):
    def __init__(self):
        self._store: dict[str, Incident] = {}

    async def save(self, incident: Incident) -> Incident:
        self._store[incident.id] = incident
        return incident

    async def get_by_id(self, incident_id: str) -> Incident | None:
        return self._store.get(incident_id)