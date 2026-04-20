from functools import lru_cache

from src.modules.incidents.application.interfaces import IIncidentRepository
from src.modules.incidents.application.use_cases import IncidentUseCases
from src.modules.incidents.infrastructure.repositories import InMemoryIncidentRepository


_repository = InMemoryIncidentRepository()

def get_incident_repository() -> IIncidentRepository:
    return _repository

def get_incident_use_cases() -> IncidentUseCases:
    return IncidentUseCases(get_incident_repository())