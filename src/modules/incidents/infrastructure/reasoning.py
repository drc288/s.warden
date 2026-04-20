import json

from groq import AsyncGroq
from pydantic import BaseModel, Field

from src.core.settings import settings
from src.modules.incidents.application.enums import Action
from src.modules.incidents.application.interfaces import IReasoningEngine
from src.modules.incidents.domain.entities import Decision, Incident
from src.modules.incidents.domain.value_object import Confidence


class _GroqDecisionPayload(BaseModel):
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(min_length=1)
    safe_to_auto: bool


_SYSTEM_PROMPT = """Eres un SRE experto. Analiza incidentes y recomienda acciones.
Responde SIEMPRE solo con JSON valido con esta forma exacta:
{
  "action": "rollback" | "restart" | "scale_up" | "notify_human" | "no_action",
  "confidence": <float 0.0-1.0>,
  "reasoning": "<explicacion breve>",
  "safe_to_auto": <bool>
}
Criterios:
- rollback: problema inmediato tras un deploy.
- restart: memory leak / conexiones colgadas.
- scale_up: saturacion de CPU/memoria.
- notify_human: causa ambigua.
- no_action: transitorio o ya resuelto.
"""


class GroqReasoningEngine(IReasoningEngine):
    def __init__(self, client: AsyncGroq | None = None) -> None:
        self._client = client or AsyncGroq(
            api_key=settings.GROQ_API_KEY,
            timeout=settings.GROQ_TIMEOUT_SECONDS,
        )

    async def reason(self, incident: Incident) -> Decision:
        user_prompt = (
            f"project_id: {incident.project_id}\n"
            f"environment_id: {incident.environment_id.value}\n"
            f"severity: {incident.severity.value}\n"
            f"signal: {incident.signal}\n"
            f"context: {json.dumps(incident.context, ensure_ascii=False)}\n"
            f"timestamp: {incident.timestamp.isoformat()}"
        )

        response = await self._client.chat.completions.create(
            model=settings.GROQ_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        payload = _GroqDecisionPayload.model_validate_json(
            response.choices[0].message.content
        )

        return Decision(
            action=payload.action,
            confidence=Confidence(value=payload.confidence),
            reasoning=payload.reasoning,
            safe_to_auto=payload.safe_to_auto,
        )
