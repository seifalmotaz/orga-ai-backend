## Project Roadmap

_This document enumerates the high-level phases and concrete tasks required to turn the current data-model skeleton into a complete, production-ready application._

### Legend
- [ ] – Task not started
- [~] – In progress
- [x] – Completed

---

## Phase 0 – Project Foundation

> Goal: establish the baseline developer experience, quality gates and workflow.

- [ ] Pin a supported Python version (&#8805; 3.11); update `requires-python` in `pyproject.toml` if needed.
- [ ] Configure **Poetry**/PDM lock-file reproducibility & virtual-env automation.
- [ ] Add **pre-commit** with `ruff`, `mypy`, `black`, `isort`.
- [ ] Create `README.md` sections for local setup, common commands & project vision.
- [ ] Configure git hooks & CI (GitHub Actions) to run lint, type-check, tests on PRs.

## Phase 1 – Database Layer

> Goal: make the models operational and version controlled via migrations.

- [x] Write `src/database/__init__.py` exposing `TORTOISE_ORM` settings (DB URL env var, apps, models).
- [x] Decide on SQLite (dev) & Postgres (prod) strategy; document env variables.
- [x] Generate initial Aerich migrations for **all** models (currently only the `aerich` table exists).
- [ ] Add seed/fixture scripts under `src/tools/seed.py` to create test data.
- [ ] Add Alembic‐style data migrations folder (if business data migrations are expected).

## Phase 2 – API & Application Server

Folder: `src/server/`

> Goal: expose REST/GraphQL endpoints that manipulate the domain objects.

### 2.1 Infrastructure
- [ ] Add **Robyn** application factory in `src/server/app.py`.
- [ ] Integrate Tortoise with Robyn (init on startup, shutdown hook).
- [ ] Add `settings.py` (pydantic-based) for configuration.
- [ ] Enable CORS, Logging, Error handling middleware.

### 2.2 Authentication & Accounts (using Clerk)
- [ ] Integrate Clerk SDK for authentication.
- [ ] Create middleware to validate Clerk JWT tokens.
- [ ] Sync Clerk user data with local `User` model (clerk_id, email, etc.).
- [ ] Device registration endpoint to persist `UserDevice` & push tokens.

### 2.3 Task Management API
- [ ] CRUD endpoints for `Task`, nested `Subtasks`.
- [ ] Endpoints for changing status, progress, priority.
- [ ] Time-log start/stop endpoints mapping to `TaskTimeLog`.
- [ ] Dependency management: add/remove prerequisites.
- [ ] Reminder CRUD (`TaskReminder`).

### 2.4 Calendar & Event API
- [ ] CRUD for `Calendar`.
- [ ] CRUD for `Event`, recurring logic (respect `RecurrencePattern`).
- [ ] Endpoint to list computed `EventInstance` range (calendar view).
- [ ] Category assignment via `EventCategoryMapping`.
- [ ] Reminder CRUD (`EventReminder`).

### 2.5 Habit Tracking API
- [ ] CRUD for `HabitTemplate` (admin) & browse list for users.
- [ ] CRUD for `Habit` for a user.
- [ ] Endpoint to mark completion; maintains `HabitCompletion` & streak calculation.

### 2.6 Miscellaneous
- [ ] Category CRUD.
- [ ] Notification queue listing endpoint (admin/support).
- [ ] OpenAPI docs hardened with security schemes & examples.

## Phase 3 – Background Services & Notifications

Folder: `src/tools/` (utility scripts) and optional `src/worker/` (celery/apscheduler)

- [ ] Select async scheduler (**APScheduler** or **Celery + Beat**).
- [ ] Service to evaluate upcoming reminders & populate `NotificationQueue`.
- [ ] Push/Email dispatcher that consumes `NotificationQueue`, sends messages and updates status.
- [ ] Recurring event instance generator (fill `EventInstance` table ahead X months).
- [ ] Habit streak evaluator & encouragement message producer.

## Phase 4 – Command-Line Interface

Folder: `src/cli/`

- [ ] Scaffold CLI with **Typer**.
- [ ] Commands:
  - `serve` – start Robyn server.
  - `worker` – start background worker.
  - `migrate` – run Aerich migrations.
  - `createsuperuser` – prompt for admin user.
  - `seed` – populate demo data.

## Phase 5 – Testing & Quality Assurance

> Goal: guarantee reliability through automated checks.

- [ ] Configure **pytest** & `pytest-asyncio`.
- [ ] Factory-boy fixtures for models.
- [ ] Integration tests for each API module (Robyn test client).
- [ ] Property-based tests for recurrence & streak algorithms.
- [ ] 90% coverage gate in CI.

## Phase 6 – Documentation & Developer Experience

- [ ] Autogenerate API reference docs with `mkdocs`.
- [ ] Diagram data model (Mermaid) in `/docs/architecture.md`.
- [ ] How-to guides: running locally, adding a model, deploying.

## Phase 7 – Deployment & Operations

- [ ] Dockerfile for app & worker images.
- [ ] docker-compose with postgres, redis, smtp relay.
- [ ] Production config templates (Gunicorn + Uvicorn workers).
- [ ] GitHub Actions workflow: build, test, push image, apply migrations.
- [ ] Monitoring hooks (Prometheus metrics, health checks).

---

### Nice-to-Have / Future Phases

- Mobile clients (Flutter/React Native) using the REST API.
- Web dashboard (ReactJS) for end users.
- OAuth social login providers. (clerk)
- Multi-tenancy support.
- ML-based habit suggestion engine. 