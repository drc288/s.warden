from src.modules.incidents.application.enums import Action, Environment, Severity
from src.modules.incidents.domain.services import SafetyPolicy


class TestRule1Critical:
    """Regla 1: severity=critical siempre fuerza safe_to_auto=False."""

    def test_critical_overrides_llm_true(self, incident_factory, decision_factory):
        incident = incident_factory(
            severity=Severity.CRITICAL,
            environment_id=Environment.QA,
        )
        decision = decision_factory(
            action=Action.RESTART,
            confidence=0.95,
            safe_to_auto=True,
        )

        result = SafetyPolicy.enforce(incident, decision)

        assert result.safe_to_auto is False

    def test_critical_in_prod_with_rollback_still_false(
        self, incident_factory, decision_factory
    ):
        incident = incident_factory(
            severity=Severity.CRITICAL,
            environment_id=Environment.PROD,
        )
        decision = decision_factory(action=Action.ROLLBACK, confidence=0.95)

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is False


class TestRule2LowConfidence:
    """Regla 2: confidence < 0.7 fuerza safe_to_auto=False."""

    def test_low_confidence_forces_false(self, incident_factory, decision_factory):
        incident = incident_factory(severity=Severity.LOW, environment_id=Environment.QA)
        decision = decision_factory(confidence=0.5, safe_to_auto=True)

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is False

    def test_exact_threshold_passes(self, incident_factory, decision_factory):
        incident = incident_factory(severity=Severity.LOW, environment_id=Environment.QA)
        decision = decision_factory(
            action=Action.RESTART, confidence=0.7, safe_to_auto=True
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is True


class TestRule3ProdRiskyAction:
    """Regla 3: prod + (rollback|scale_up) fuerza False."""

    def test_prod_rollback_forces_false(self, incident_factory, decision_factory):
        incident = incident_factory(
            severity=Severity.HIGH, environment_id=Environment.PROD
        )
        decision = decision_factory(
            action=Action.ROLLBACK, confidence=0.9, safe_to_auto=True
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is False

    def test_prod_scale_up_forces_false(self, incident_factory, decision_factory):
        incident = incident_factory(
            severity=Severity.HIGH, environment_id=Environment.PROD
        )
        decision = decision_factory(
            action=Action.SCALE_UP, confidence=0.9, safe_to_auto=True
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is False

    def test_prod_restart_remains_true(self, incident_factory, decision_factory):
        """restart NO esta en el set de acciones bloqueadas en prod."""
        incident = incident_factory(
            severity=Severity.HIGH, environment_id=Environment.PROD
        )
        decision = decision_factory(
            action=Action.RESTART, confidence=0.9, safe_to_auto=True
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is True

    def test_qa_rollback_remains_true(self, incident_factory, decision_factory):
        """rollback esta permitido fuera de prod."""
        incident = incident_factory(
            severity=Severity.HIGH, environment_id=Environment.QA
        )
        decision = decision_factory(
            action=Action.ROLLBACK, confidence=0.9, safe_to_auto=True
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is True


class TestHappyPath:
    """Sin ninguna regla disparada, safe_to_auto queda como decidio el LLM."""

    def test_llm_true_passes_through(self, incident_factory, decision_factory):
        incident = incident_factory(
            severity=Severity.MEDIUM, environment_id=Environment.QA
        )
        decision = decision_factory(
            action=Action.RESTART, confidence=0.9, safe_to_auto=True
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is True

    def test_llm_false_passes_through(self, incident_factory, decision_factory):
        incident = incident_factory(
            severity=Severity.MEDIUM, environment_id=Environment.QA
        )
        decision = decision_factory(
            action=Action.RESTART, confidence=0.9, safe_to_auto=False
        )

        assert SafetyPolicy.enforce(incident, decision).safe_to_auto is False


class TestImmutability:
    def test_original_decision_is_not_mutated(self, incident_factory, decision_factory):
        incident = incident_factory(severity=Severity.CRITICAL)
        decision = decision_factory(safe_to_auto=True)

        result = SafetyPolicy.enforce(incident, decision)

        assert decision.safe_to_auto is True, "original mutado"
        assert result.safe_to_auto is False
        assert result is not decision
