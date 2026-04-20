from dataclasses import dataclass, field                                                              


@dataclass(frozen=True)
class Confidence:
    value: float
    def __post_init__(self):
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("Confidence debe estar en [0.0, 1.0]")
    
    @property
    def is_high(self) -> bool:
        return self.value >= 0.7
