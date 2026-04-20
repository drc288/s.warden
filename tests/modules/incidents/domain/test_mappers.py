from datetime import datetime, timezone

from src.modules.incidents.application.enums import Action, Environment, Severity
from src.modules.incidents.domain.mappers import (
    decision_to_response,
    webhook_to_incident,
)
from src.modules.incidents.presentation.schemas import IncidentWebhookRequest


class TestWebhookToIncident:
    def test_all_fields_copied(self):
        payload = IncidentWebhookRequest(
            project_id="payments-api",
            environment_id=Environment.PROD,
            severity=Severity.HIGH,
            signal="latency spike",
            context={"cpu": "85%"},
            timestamp=datetime(2026, 4, 20, 12, 0, 0, tzinfo=timezone.utc),
        )

        incident = webhook_to_incident(payload)

        assert incident.project_id == "payments-api"
        assert incident.environment_id == Environment.PROD
        assert incident.severity == Severity.HIGH
        assert incident.signal == "latency spike"
        assert incident.context == {"cpu": "85%"}
        assert incident.timestamp == datetime(2026, 4, 20, 12, 0, 0, tzinfo=timezone.utc)

    def test_id_is_auto_generated(self):
        payload = IncidentWebhookRequest(
            project_id="x",
            environment_id=Environment.PROD,
            severity=Severity.LOW,
            signal="s",
            context={},
            timestamp=datetime(2026, 4, 20, tzinfo=timezone.utc),
        )

        incident_a = webhook_to_incident(payload)
        incident_b = webhook_to_incident(payload)

        assert incident_a.id is not None
        assert incident_a.id != incident_b.id

    def test_empty_context_preserved(self):
        payload = IncidentWebhookRequest(
            project_id="x",
            environment_id=Environment.PROD,
            severity=Severity.LOW,
            signal="s",
            context={},
            timestamp=datetime(2026, 4, 20, tzinfo=timezone.utc),
        )

        assert webhook_to_incident(payload).context == {}


class TestDecisionToResponse:
    def test_confidence_vo_extracted_to_float(self, decision_factory):
        decision = decision_factory(confidence=0.87)

        response = decision_to_response(decision)

        assert response.confidence == 0.87
        assert isinstance(response.confidence, float)

    def test_all_other_fields_one_to_one(self, decision_factory):
        decision = decision_factory(
            action=Action.ROLLBACK,
            reasoning="deploy regression",
            safe_to_auto=False,
        )

        response = decision_to_response(decision)

        assert response.action == Action.ROLLBACK
        assert response.reasoning == "deploy regression"
        assert response.safe_to_auto is False
