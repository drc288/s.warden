from fastapi import APIRouter, Depends

from src.modules.incidents.application.use_cases import ProcessIncidentUseCase
from src.modules.incidents.domain.mappers import (
    decision_to_response,
    webhook_to_incident,
)
from src.modules.incidents.presentation.dependencies import (
    get_process_incident_use_case,
)
from src.modules.incidents.presentation.schemas import (
    DecisionResponse,
    IncidentWebhookRequest,
)

router = APIRouter(prefix="/webhooks/incidents", tags=["Incident"])


@router.post("", response_model=DecisionResponse, status_code=201)
async def ingest_incident(
    payload: IncidentWebhookRequest,
    use_case: ProcessIncidentUseCase = Depends(get_process_incident_use_case),
) -> DecisionResponse:
    incident = webhook_to_incident(payload)
    decision = await use_case.execute(incident)
    return decision_to_response(decision)
