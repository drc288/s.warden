from src.modules.health.domain.entities import Health


class HealthUseCases:
    @staticmethod
    async def health() -> Health:
        return Health()
