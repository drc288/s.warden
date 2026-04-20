import pytest

from src.modules.incidents.application.enums import Action, Environment, Severity
from src.modules.incidents.application.use_cases import ProcessIncidentUseCase


class TestProcessIncidentOrchestration:
    async def test_calls_engine_with_incident(
        self, fake_engine, fake_repo, incident_factory
    ):
        use_case = ProcessIncidentUseCase(reasoning=fake_engine, repository=fake_repo)
        incident = incident_factory()

        await use_case.execute(incident)

        assert fake_engine.calls == [incident]

    async def test_returns_post_policy_decision(
        self, fake_engine, fake_repo, incident_factory, decision_factory
    ):
        """Regla 1 (critical) aplicada end-to-end via use case."""
        fake_engine._decision = decision_factory(
            action=Action.RESTART, confidence=0.95, safe_to_auto=True
        )
        use_case = ProcessIncidentUseCase(reasoning=fake_engine, repository=fake_repo)
        incident = incident_factory(severity=Severity.CRITICAL)

        result = await use_case.execute(incident)

        assert result.safe_to_auto is False

    async def test_persists_post_policy_decision(
        self, fake_engine, fake_repo, incident_factory, decision_factory
    ):
        """Lo que se guarda es la decision DESPUES de policy, no la raw."""
        fake_engine._decision = decision_factory(
            action=Action.ROLLBACK, confidence=0.9, safe_to_auto=True
        )
        use_case = ProcessIncidentUseCase(reasoning=fake_engine, repository=fake_repo)
        incident = incident_factory(environment_id=Environment.PROD)

        await use_case.execute(incident)

        stored = await fake_repo.get_by_id(incident.id)
        assert stored is not None
        _, stored_decision = stored
        assert stored_decision.safe_to_auto is False

    async def test_engine_error_propagates(
        self, fake_repo, incident_factory
    ):
        class BrokenEngine:
            async def reason(self, incident):
                raise RuntimeError("llm down")

        use_case = ProcessIncidentUseCase(
            reasoning=BrokenEngine(), repository=fake_repo
        )

        with pytest.raises(RuntimeError, match="llm down"):
            await use_case.execute(incident_factory())

    async def test_repo_error_propagates(
        self, fake_engine, incident_factory
    ):
        class BrokenRepo:
            async def save(self, incident, decision):
                raise RuntimeError("db down")

        use_case = ProcessIncidentUseCase(
            reasoning=fake_engine, repository=BrokenRepo()
        )

        with pytest.raises(RuntimeError, match="db down"):
            await use_case.execute(incident_factory())
