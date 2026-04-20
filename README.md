# Warden

Sistema de remediacion de incidentes con LLM.

## Arquitectura

Clean Architecture + DDD + Hexagonal (Ports & Adapters), organizado en modulos por feature. Cada modulo tiene 4 capas:

- `domain/` — entidades y reglas de negocio puras
- `application/` — casos de uso, interfaces (ports), enums
- `infrastructure/` — adapters concretos (DB, APIs externas)
- `presentation/` — routers FastAPI, schemas Pydantic

## Requisitos

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
cp .env.example .env
```

## Correr el servidor

```bash
uv run fastapi dev src/app.py
```

Endpoints:

- `GET /health` — health check
- `POST /webhooks/incidents` — ingesta de eventos de degradacion
- `GET /docs` — Swagger UI

## Tests

```bash
# Correr todos los tests
uv run pytest

# Solo tests de un modulo
uv run pytest tests/modules/incidents/

# Con reporte de coverage en consola
uv run pytest --cov=src --cov-report=term-missing

# Coverage en HTML (se genera htmlcov/index.html)
uv run pytest --cov=src --cov-report=html
```

### Estructura de tests

```
tests/
├── conftest.py                 ← fixtures globales (factories, client, fakes)
├── fakes/
│   └── reasoning.py            ← FakeReasoningEngine (double del LLM)
└── modules/
    ├── health/
    └── incidents/
        ├── domain/             ← Confidence, SafetyPolicy, mappers
        ├── application/        ← ProcessIncidentUseCase con fakes
        ├── infrastructure/     ← Repos + adapter Groq con AsyncMock
        └── presentation/       ← Schemas Pydantic + router (TestClient)
```

Los tests espejean la estructura de `src/modules/` para navegacion intuitiva.
Cada test es independiente y **no requiere red**: el adapter de Groq se
mockea con `unittest.mock.AsyncMock`, y el flujo HTTP se prueba con
`fastapi.testclient.TestClient` usando `app.dependency_overrides` para
reemplazar el use case real por uno con `FakeReasoningEngine` + repo en
memoria.

### Cobertura por capa

| Capa | Que valida |
|---|---|
| **Domain** | `Confidence` (rango, inmutabilidad), `SafetyPolicy` (3 reglas + combos + no-mutacion), mappers (VO → float, id auto-generado) |
| **Application** | `ProcessIncidentUseCase` orquesta engine + policy + repo; persiste decision post-policy; propaga errores |
| **Infrastructure** | Repo in-memory (UUID keys), adapter Groq (happy path + 4 validaciones del JSON del LLM) |
| **Presentation** | Validacion Pydantic del webhook (severity, environment, extra="forbid", min_length, timestamp), router end-to-end con safety policy aplicada |
