from pydantic import BaseModel, ConfigDict, Field

from src.modules.health.application.enums import HealthType


class HealthResponse(BaseModel):
    status: HealthType = Field(
        title="Health Status",
        description="Estado del sistema.",
        examples=[HealthType.OK.value],
    )

    model_config = ConfigDict(
        title="HealthResponse",
        extra="forbid",
        validate_assignment=True,
    )
