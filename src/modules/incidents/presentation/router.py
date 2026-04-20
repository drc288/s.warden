from fastapi import APIRouter, Depends

from src.modules.incidents.application.use_cases import IncidentUseCases
from src.modules.incidents.domain.mappers import incident_to_response
from src.modules.incidents.presentation.dependencies import get_incident_use_cases
from src.modules.incidents.presentation.schemas import RegistryIncidentRequest, IncidentResponse

router = APIRouter(prefix="/incidents", tags=["Incident"])

@router.post("", response_model=IncidentResponse, status_code=201)
async def register_incident(
    payload: RegistryIncidentRequest,
    use_cases: IncidentUseCases = Depends(get_incident_use_cases)
) -> IncidentResponse:
    incident = await use_cases.register(
        description=payload.description, severity=payload.severity.value
    )
    return await incident_to_response(incident)