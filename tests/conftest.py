from datetime import datetime, timezone
from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.modules.incidents.application.enums import (
    Action,
    Environment,
    Severity,
)
from src.modules.incidents.domain.entities import Decision, Incident
from src.modules.incidents.domain.value_object import Confidence
from src.modules.incidents.application.use_cases import ProcessIncidentUseCase
from src.modules.incidents.infrastructure.repositories import (
    InMemoryIncidentRepository,
)
from src.modules.incidents.presentation.dependencies import (
    get_process_incident_use_case,
)
from tests.fakes.reasoning import FakeReasoningEngine


@pytest.fixture
def incident_factory():
    def _make(
        project_id: str = "payments-api",
        environment_id: Environment = Environment.PROD,
        severity: Severity = Severity.HIGH,
        signal: str = "latency spike",
        context: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> Incident:
        return Incident(
            project_id=project_id,
            environment_id=environment_id,
            severity=severity,
            signal=signal,
            context=context if context is not None else {},
            timestamp=timestamp or datetime(2026, 4, 20, 12, 0, 0, tzinfo=timezone.utc),
        )

    return _make


@pytest.fixture
def decision_factory():
    def _make(
        action: Action = Action.RESTART,
        confidence: float = 0.9,
        reasoning: str = "test reasoning",
        safe_to_auto: bool = True,
    ) -> Decision:
        return Decision(
            action=action,
            confidence=Confidence(confidence),
            reasoning=reasoning,
            safe_to_auto=safe_to_auto,
        )

    return _make


@pytest.fixture
def fake_engine():
    return FakeReasoningEngine()


@pytest.fixture
def fake_repo():
    return InMemoryIncidentRepository()


@pytest.fixture
def client(fake_engine, fake_repo):
    def _override_use_case() -> ProcessIncidentUseCase:
        return ProcessIncidentUseCase(reasoning=fake_engine, repository=fake_repo)

    app.dependency_overrides[get_process_incident_use_case] = _override_use_case
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def valid_webhook_payload():
    return {
        "project_id": "payments-api",
        "environment_id": "prod",
        "severity": "high",
        "signal": "P99 latency spiked to 4s after the 14:30 deploy",
        "context": {
            "last_deploy": "v2.3.1",
            "cpu_usage": "85%",
            "error_rate": "12%",
        },
        "timestamp": "2026-04-20T14:45:00Z",
    }
