from nt import replace
from src.modules.incidents.application.enums import Environment, Severity, Action
from src.modules.incidents.domain.entities import Incident, Decision



class SafePolicy:
    @staticmethod
    def enforce(incident: Incident, decision: Decision) -> Decision:
        # Critical siempre False
        if incident.severity == Severity.CRITICAL:
            return replace(decision, safe_to_auto=False)

        # If Confidence is low 0.7, always false
        if not decision.confidence.is_high:
            return replace(decision, safe_to_auto=False)

        # If environment is PROD and action is ROLLBACK or SCALE_UP, always false
        if (
            incident.environment_id == Environment.PROD
            and decision.action == {Action.ROLLBACK, Action.SCALE_UP}
        ):
            return replace(decision, safe_to_auto=False)

        return decision