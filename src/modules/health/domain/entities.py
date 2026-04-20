from dataclasses import dataclass

from src.modules.health.application.enums import HealthType


@dataclass
class Health:
    @property
    def status(self) -> HealthType:
        return HealthType.OK
