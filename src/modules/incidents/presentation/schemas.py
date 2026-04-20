from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from src.modules.incidents.application.enums import Severity


class RegistryIncidentRequest(BaseModel):
    description: str = Field(min_length=1, max_length=500)
    severity: Severity

class IncidentResponse(BaseModel):
    id: UUID
    description: str
    severity: Severity
    created_at: datetime