from src.modules.health.domain.entities import Health
from src.modules.health.presentation.schemas import HealthResponse


async def health_mapper(health: Health) -> HealthResponse:
    return HealthResponse(status=health.status)
