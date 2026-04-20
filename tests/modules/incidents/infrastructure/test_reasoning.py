import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from src.modules.incidents.domain.value_object import Confidence
from src.modules.incidents.infrastructure.reasoning import GroqReasoningEngine


def _mock_client_returning(content: str) -> AsyncMock:
    client = AsyncMock()
    client.chat.completions.create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
        )
    )
    return client


class TestGroqReasoningEngineHappyPath:
    async def test_valid_json_response_parses_to_decision(self, incident_factory):
        content = json.dumps(
            {
                "action": "rollback",
                "confidence": 0.87,
                "reasoning": "deploy regression",
                "safe_to_auto": True,
            }
        )
        client = _mock_client_returning(content)
        engine = GroqReasoningEngine(client=client)

        decision = await engine.reason(incident_factory())

        assert decision.action.value == "rollback"
        assert isinstance(decision.confidence, Confidence)
        assert decision.confidence.value == 0.87
        assert decision.reasoning == "deploy regression"
        assert decision.safe_to_auto is True

    async def test_sends_json_object_response_format(self, incident_factory):
        content = json.dumps(
            {
                "action": "no_action",
                "confidence": 0.5,
                "reasoning": "transitorio",
                "safe_to_auto": False,
            }
        )
        client = _mock_client_returning(content)
        engine = GroqReasoningEngine(client=client)

        await engine.reason(incident_factory())

        kwargs = client.chat.completions.create.call_args.kwargs
        assert kwargs["response_format"] == {"type": "json_object"}
        assert len(kwargs["messages"]) == 2
        assert kwargs["messages"][0]["role"] == "system"
        assert kwargs["messages"][1]["role"] == "user"


class TestGroqReasoningEngineValidation:
    async def test_out_of_range_confidence_rejected(self, incident_factory):
        content = json.dumps(
            {
                "action": "restart",
                "confidence": 1.5,
                "reasoning": "x",
                "safe_to_auto": True,
            }
        )
        engine = GroqReasoningEngine(client=_mock_client_returning(content))

        with pytest.raises(ValidationError):
            await engine.reason(incident_factory())

    async def test_invalid_action_rejected(self, incident_factory):
        content = json.dumps(
            {
                "action": "invalid_action",
                "confidence": 0.9,
                "reasoning": "x",
                "safe_to_auto": True,
            }
        )
        engine = GroqReasoningEngine(client=_mock_client_returning(content))

        with pytest.raises(ValidationError):
            await engine.reason(incident_factory())

    async def test_missing_field_rejected(self, incident_factory):
        content = json.dumps(
            {
                "action": "restart",
                "confidence": 0.9,
                "reasoning": "x",
                # safe_to_auto ausente
            }
        )
        engine = GroqReasoningEngine(client=_mock_client_returning(content))

        with pytest.raises(ValidationError):
            await engine.reason(incident_factory())

    async def test_empty_reasoning_rejected(self, incident_factory):
        content = json.dumps(
            {
                "action": "restart",
                "confidence": 0.9,
                "reasoning": "",
                "safe_to_auto": True,
            }
        )
        engine = GroqReasoningEngine(client=_mock_client_returning(content))

        with pytest.raises(ValidationError):
            await engine.reason(incident_factory())
