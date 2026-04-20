from uuid import UUID

from src.modules.incidents.application.interfaces import IIncidentRepository
from src.modules.incidents.domain.entities import Decision, Incident


class InMemoryIncidentRepository(IIncidentRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, tuple[Incident, Decision]] = {}

    async def save(self, incident: Incident, decision: Decision) -> None:
        self._store[incident.id] = (incident, decision)

    async def get_by_id(self, incident_id: UUID) -> tuple[Incident, Decision] | None:
        return self._store.get(incident_id)
