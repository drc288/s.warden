from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.modules.incidents.presentation.schemas import IncidentWebhookRequest


class TestValidPayloads:
    def test_documented_payload_parses(self, valid_webhook_payload):
        schema = IncidentWebhookRequest(**valid_webhook_payload)

        assert schema.project_id == "payments-api"
        assert schema.environment_id.value == "prod"
        assert schema.severity.value == "high"
        assert schema.signal.startswith("P99")
        assert schema.context["last_deploy"] == "v2.3.1"

    def test_context_absent_defaults_to_empty_dict(self, valid_webhook_payload):
        valid_webhook_payload.pop("context")
        schema = IncidentWebhookRequest(**valid_webhook_payload)

        assert schema.context == {}

    def test_context_allows_mixed_types(self, valid_webhook_payload):
        valid_webhook_payload["context"] = {
            "string_key": "v2.3.1",
            "int_key": 42,
            "nested": {"level": 2},
        }
        schema = IncidentWebhookRequest(**valid_webhook_payload)

        assert schema.context["int_key"] == 42
        assert schema.context["nested"]["level"] == 2


class TestSeverityValidation:
    def test_rejects_unknown_severity(self, valid_webhook_payload):
        valid_webhook_payload["severity"] = "super-bad"

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)

    def test_rejects_missing_severity(self, valid_webhook_payload):
        valid_webhook_payload.pop("severity")

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)

    @pytest.mark.parametrize("value", ["low", "medium", "high", "critical"])
    def test_accepts_all_documented_severities(self, valid_webhook_payload, value):
        valid_webhook_payload["severity"] = value
        assert IncidentWebhookRequest(**valid_webhook_payload).severity.value == value


class TestEnvironmentValidation:
    def test_accepts_prod(self, valid_webhook_payload):
        valid_webhook_payload["environment_id"] = "prod"
        assert (
            IncidentWebhookRequest(**valid_webhook_payload).environment_id.value
            == "prod"
        )

    def test_accepts_qa(self, valid_webhook_payload):
        valid_webhook_payload["environment_id"] = "qa"
        assert (
            IncidentWebhookRequest(**valid_webhook_payload).environment_id.value == "qa"
        )

    def test_accepts_dev(self, valid_webhook_payload):
        """Documento define dev como valido. Test falla si el enum no lo tiene."""
        valid_webhook_payload["environment_id"] = "dev"
        assert (
            IncidentWebhookRequest(**valid_webhook_payload).environment_id.value
            == "dev"
        )

    def test_accepts_stg(self, valid_webhook_payload):
        """Documento usa 'stg', no 'staging'. Test falla si el enum tiene 'staging'."""
        valid_webhook_payload["environment_id"] = "stg"
        assert (
            IncidentWebhookRequest(**valid_webhook_payload).environment_id.value
            == "stg"
        )

    def test_rejects_unknown_environment(self, valid_webhook_payload):
        valid_webhook_payload["environment_id"] = "mars"

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)


class TestStringFields:
    def test_rejects_empty_project_id(self, valid_webhook_payload):
        valid_webhook_payload["project_id"] = ""

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)

    def test_rejects_empty_signal(self, valid_webhook_payload):
        valid_webhook_payload["signal"] = ""

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)


class TestTimestampValidation:
    def test_rejects_invalid_datetime(self, valid_webhook_payload):
        valid_webhook_payload["timestamp"] = "no-es-fecha"

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)

    def test_accepts_iso_format_with_z(self, valid_webhook_payload):
        valid_webhook_payload["timestamp"] = "2026-04-20T14:45:00Z"
        schema = IncidentWebhookRequest(**valid_webhook_payload)

        assert schema.timestamp == datetime(
            2026, 4, 20, 14, 45, 0, tzinfo=timezone.utc
        )


class TestExtraFields:
    def test_rejects_extra_field(self, valid_webhook_payload):
        valid_webhook_payload["foo"] = "bar"

        with pytest.raises(ValidationError):
            IncidentWebhookRequest(**valid_webhook_payload)
