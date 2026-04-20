from src.modules.incidents.application.enums import Action
from src.modules.incidents.application.interfaces import IReasoningEngine
from src.modules.incidents.domain.entities import Decision, Incident
from src.modules.incidents.domain.value_object import Confidence


class FakeReasoningEngine(IReasoningEngine):
    def __init__(self, decision: Decision | None = None) -> None:
        self._decision = decision
        self.calls: list[Incident] = []

    async def reason(self, incident: Incident) -> Decision:
        self.calls.append(incident)
        return self._decision or Decision(
            action=Action.NO_ACTION,
            confidence=Confidence(0.9),
            reasoning="fake reasoning",
            safe_to_auto=True,
        )
