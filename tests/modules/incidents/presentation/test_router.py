from src.modules.incidents.application.enums import Action
from src.modules.incidents.domain.entities import Decision
from src.modules.incidents.domain.value_object import Confidence


class TestRouterHappyPath:
    def test_valid_payload_returns_201_with_decision(
        self, client, fake_engine, valid_webhook_payload
    ):
        # LLM dice restart + auto=True + high confidence
        fake_engine._decision = Decision(
            action=Action.RESTART,
            confidence=Confidence(0.9),
            reasoning="memory leak suspected",
            safe_to_auto=True,
        )
        # Cambiamos env a qa para que no dispare regla 3
        valid_webhook_payload["environment_id"] = "qa"

        response = client.post("/webhooks/incidents", json=valid_webhook_payload)

        assert response.status_code == 201
        body = response.json()
        assert body["action"] == "restart"
        assert body["confidence"] == 0.9
        assert body["safe_to_auto"] is True


class TestRouterSafetyPolicyEndToEnd:
    def test_critical_forces_safe_to_auto_false(
        self, client, fake_engine, valid_webhook_payload
    ):
        """Regla 1 aplicada por el use case al response del LLM."""
        fake_engine._decision = Decision(
            action=Action.RESTART,
            confidence=Confidence(0.95),
            reasoning="urgent",
            safe_to_auto=True,
        )
        valid_webhook_payload["severity"] = "critical"
        valid_webhook_payload["environment_id"] = "qa"

        response = client.post("/webhooks/incidents", json=valid_webhook_payload)

        assert response.status_code == 201
        assert response.json()["safe_to_auto"] is False

    def test_prod_rollback_forces_safe_to_auto_false(
        self, client, fake_engine, valid_webhook_payload
    ):
        """Regla 3 aplicada end-to-end."""
        fake_engine._decision = Decision(
            action=Action.ROLLBACK,
            confidence=Confidence(0.9),
            reasoning="deploy regression",
            safe_to_auto=True,
        )
        valid_webhook_payload["environment_id"] = "prod"

        response = client.post("/webhooks/incidents", json=valid_webhook_payload)

        assert response.status_code == 201
        body = response.json()
        assert body["action"] == "rollback"
        assert body["safe_to_auto"] is False


class TestRouterValidation:
    def test_invalid_severity_returns_422(self, client, valid_webhook_payload):
        valid_webhook_payload["severity"] = "super-bad"

        response = client.post("/webhooks/incidents", json=valid_webhook_payload)

        assert response.status_code == 422
        assert "detail" in response.json()

    def test_extra_field_returns_422(self, client, valid_webhook_payload):
        valid_webhook_payload["foo"] = "bar"

        response = client.post("/webhooks/incidents", json=valid_webhook_payload)

        assert response.status_code == 422

    def test_missing_required_field_returns_422(self, client, valid_webhook_payload):
        valid_webhook_payload.pop("project_id")

        response = client.post("/webhooks/incidents", json=valid_webhook_payload)

        assert response.status_code == 422
