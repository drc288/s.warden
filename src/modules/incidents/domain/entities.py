from dataclasses import dataclass, field                                                              
from datetime import datetime
from uuid import UUID, uuid4

from src.modules.incidents.application.enums import Severity, Environment, Action
from src.modules.incidents.domain.value_object import Confidence

@dataclass
class Incident:
    project_id: str
    environment_id: Environment
    severity: Severity
    signal: str
    context: dict[str, any]
    timestamp: datetime
    id: UUID = field(default_factory=uuid4)

@dataclass
class Decision:
    action: Action
    confidence: Confidence
    reasoning: str
    safe_to_auto: bool