from dataclasses import dataclass, field                                                              
from datetime import datetime                         
from uuid import UUID, uuid4

@dataclass
class Incident:
    project_id: UUID = field(default_factory=uuid4)
    environment_id: str
    severity: str
    signal: str
    context: dict[str]
    timestamp: datetime = field(default_factory=datetime.now)
