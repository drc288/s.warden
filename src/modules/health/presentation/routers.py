from fastapi import APIRouter

from src.modules.health.application.use_cases import HealthUseCases
from src.modules.health.domain.mappers import health_mapper
from src.modules.health.presentation.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health() -> HealthResponse:
    use_case = HealthUseCases()
    domain = await use_case.health()
    return await health_mapper(domain)
