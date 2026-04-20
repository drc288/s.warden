from src.modules.incidents.domain.entities import Decision, Incident
from src.modules.incidents.presentation.schemas import (
    DecisionResponse,
    IncidentWebhookRequest,
)


def webhook_to_incident(payload: IncidentWebhookRequest) -> Incident:
    return Incident(
        project_id=payload.project_id,
        environment_id=payload.environment_id,
        severity=payload.severity,
        signal=payload.signal,
        context=payload.context,
        timestamp=payload.timestamp,
     )


def decision_to_response(decision: Decision) -> DecisionResponse:
    return DecisionResponse(
        action=decision.action,
        confidence=decision.confidence.value,
        reasoning=decision.reasoning,
        safe_to_auto=decision.safe_to_auto,
    )