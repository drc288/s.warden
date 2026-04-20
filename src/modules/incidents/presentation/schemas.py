from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.modules.incidents.application.enums import Action, Environment, Severity

class IncidentWebhookRequest(BaseModel):
    project_id: str = Field(min_length=1)
    environment_id: Environment
    severity: Severity
    signal: str = Field(min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime

    model_config = ConfigDict(extra="forbid")

class DecisionResponse(BaseModel):
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    safe_to_auto: bool