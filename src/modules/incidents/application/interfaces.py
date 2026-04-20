from typing import Protocol
from src.modules.incidents.domain.entities import Incident, Decision


class IReasoningEngine(Protocol):
    async def reason(self, incident: Incident) -> Decision: ...

class IIncidentRepository(Protocol):
    async def save(self, incident: Incident, decision: Decision) -> None: ...