from uuid import uuid4

from src.modules.incidents.infrastructure.repositories import (
    InMemoryIncidentRepository,
)


class TestInMemoryIncidentRepository:
    async def test_save_and_get(self, incident_factory, decision_factory):
        repo = InMemoryIncidentRepository()
        incident = incident_factory()
        decision = decision_factory()

        await repo.save(incident, decision)
        result = await repo.get_by_id(incident.id)

        assert result is not None
        stored_incident, stored_decision = result
        assert stored_incident is incident
        assert stored_decision is decision

    async def test_get_unknown_id_returns_none(self):
        repo = InMemoryIncidentRepository()

        assert await repo.get_by_id(uuid4()) is None

    async def test_store_uses_uuid_keys(self, incident_factory, decision_factory):
        """Guardar con UUID y consultar con string no debe matchear."""
        repo = InMemoryIncidentRepository()
        incident = incident_factory()
        decision = decision_factory()

        await repo.save(incident, decision)

        assert incident.id in repo._store
        assert str(incident.id) not in repo._store
