from functools import lru_cache

from src.modules.incidents.application.interfaces import (
    IIncidentRepository,
    IReasoningEngine,
)
from src.modules.incidents.application.use_cases import ProcessIncidentUseCase
from src.modules.incidents.infrastructure.reasoning import GroqReasoningEngine
from src.modules.incidents.infrastructure.repositories import InMemoryIncidentRepository


@lru_cache(maxsize=1)
def get_incident_repository() -> IIncidentRepository:
    return InMemoryIncidentRepository()


@lru_cache(maxsize=1)
def get_reasoning_engine() -> IReasoningEngine:
    return GroqReasoningEngine()


def get_process_incident_use_case() -> ProcessIncidentUseCase:
    return ProcessIncidentUseCase(
        reasoning=get_reasoning_engine(),
        repository=get_incident_repository(),
    )
