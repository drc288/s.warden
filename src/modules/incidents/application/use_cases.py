from src.modules.incidents.application.interfaces import (
    IIncidentRepository,
    IReasoningEngine,
)
from src.modules.incidents.domain.entities import Decision, Incident
from src.modules.incidents.domain.services import SafetyPolicy


class ProcessIncidentUseCase:
    def __init__(
        self,
        reasoning: IReasoningEngine,
        repository: IIncidentRepository,
    ) -> None:
        self._reasoning = reasoning
        self._repository = repository

    async def execute(self, incident: Incident) -> Decision:
        raw_decision = await self._reasoning.reason(incident)
        final_decision = SafetyPolicy.enforce(incident, raw_decision)
        await self._repository.save(incident, final_decision)
        return final_decision
