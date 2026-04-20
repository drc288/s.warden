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
- `GET /docs` — Swagger UI
