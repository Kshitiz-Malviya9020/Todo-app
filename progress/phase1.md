# Todo Application --- Phase 1: Project Setup

**Status:** Completed\
**Project:** Todo Application\
**Phase:** 1 --- Backend Project Setup\
**Last documented:** 17 November 2026

> This document consolidates the decisions, structure, configuration,
> implementation, and checks completed during the Phase 1 discussion.
------------------------------------------------------------------------

## 1. Project Overview

The Todo application is being developed incrementally, starting with the
backend. The goal of Phase 1 was to establish a clean FastAPI backend
foundation, configure the development environment, expose basic API
endpoints, and verify that the application and tests run successfully.

### Finalized technology decisions

  -----------------------------------------------------------------------
  Area                                Decision
  ----------------------------------- -----------------------------------
  Backend framework                   FastAPI

  Backend language                    Python

  Frontend                            Vanilla JavaScript, HTML, and CSS

  Authentication                      JWT stored in secure HttpOnly
                                      cookies

  Database                            MySQL

  ORM                                 SQLAlchemy

  Database migrations                 Alembic

  MySQL driver                        PyMySQL

  Configuration and validation        Pydantic and pydantic-settings

  Dependency management               `uv` with `pyproject.toml` and
                                      `uv.lock`

  Testing                             pytest, FastAPI TestClient, and
                                      `httpx2`

  Calendar                            Independent calendar display/date
                                      navigation; no synchronization with
                                      Todo tasks

  Delivery approach                   MVP first, then advanced features
  -----------------------------------------------------------------------

### MVP data-model scope agreed so far

The initial database scope is deliberately small:

-   `users`
-   `todos`

------------------------------------------------------------------------

## 2. Development and Git Workflow

The agreed development workflow is feature-branch based:

1.  Start from an up-to-date `main` branch.
2.  Create a separate branch for one feature.
3.  Implement the feature and its tests.
4.  Run the relevant checks.
5.  Commit the completed work.
6.  Merge the feature branch into `main`.
7.  Push the updated `main` branch to the remote repository.
8.  Delete the feature branch after the merge.
9.  Sync/pull the latest repository state before starting the next
    feature.

The project was being worked on in this branch during Phase 1:

``` bash
feature/setup
```

**Git checkpoint:** Before starting the next feature branch, confirm
that `feature/setup` has been committed, pushed, and merged into
`main` according to the workflow above. The conversation ended while
this confirmation was still pending.

------------------------------------------------------------------------

## 3. Backend Directory Structure

The initial backend structure was created as follows:

``` text
todo-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── health.py
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── __init__.py
│   │   ├── db/
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   ├── main.py
│   │   └── __init__.py
│   ├── tests/
│   │   └── test_main.py
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   └── .gitkeep
├── .gitignore
└── README.md
```

### Purpose of the main directories

  -----------------------------------------------------------------------
  Path                                Responsibility
  ----------------------------------- -----------------------------------
  `app/main.py`                       Creates the FastAPI application and
                                      registers routers

  `app/api/v1/`                       Contains versioned HTTP API
                                      routers/endpoints

  `app/core/`                         Shared configuration and core
                                      application concerns

  `app/db/`                           Database engine, session, and
                                      database-related setup (to be
                                      implemented in Phase 2)

  `app/models/`                       SQLAlchemy database models (to be
                                      implemented as needed)

  `app/schemas/`                      Pydantic request and response
                                      schemas

  `app/services/`                     Business logic, separate from HTTP
                                      route handling

  `tests/`                            Automated tests

  `frontend/`                         Vanilla HTML/CSS/JavaScript client
  -----------------------------------------------------------------------

`__init__.py` files mark Python package directories. 

------------------------------------------------------------------------

## 4. Python Environment and Dependencies

The project uses `uv` for dependency and virtual-environment management.

The backend project configuration is stored in `backend/pyproject.toml`.
The lock file `backend/uv.lock` records resolved dependency versions so
that the environment can be reproduced more consistently.

### `pyproject.toml`

The intended configuration at the end of Phase 1 was:

``` toml
[project]
name = "todo-backend"
version = "0.1.0"
description = "FastAPI backend for the Todo application"
readme = "../README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "sqlalchemy",
    "alembic",
    "pymysql",
    "pydantic",
    "pydantic-settings",
    "python-dotenv",
]

[dependency-groups]
dev = [
    "pytest",
    "httpx2",
    "ruff",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### Important commands

Run these from the `backend/` directory:

``` powershell
uv sync
uv run uvicorn app.main:app --reload
uv run pytest -v
```

-   `uv sync` installs the dependencies declared by the project and
    synchronizes the environment.
-   `uv run ...` runs a command inside the project's managed
    environment.
-   Uvicorn runs the ASGI application.
-   `pytest -v` discovers and runs the tests with verbose output.

The project uses `httpx2` for compatibility with the Starlette
TestClient setup in this environment. The earlier Starlette deprecation
warning was addressed by switching the development dependency from
`httpx` to `httpx2`.

------------------------------------------------------------------------

## 5. Environment Configuration

Application configuration is defined using Pydantic Settings.

### `app/core/config.py`

``` python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Todo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
```

### `.env.example`

``` env
APP_NAME=Todo API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development
```

A local `.env` file was also created with the corresponding development
values.

**Security rule:** `.env` contains local environment configuration and
must remain ignored by Git. Commit `.env.example` so another developer
knows which environment variables are required, but do not commit real
secrets or credentials.

### Backend `.gitignore`

The backend ignore rules include:

``` gitignore
.venv/
venv/
.env
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
.vscode/
.idea/
.DS_Store
Thumbs.db
.claude/
```

------------------------------------------------------------------------

## 6. FastAPI Application and API Versioning

### `app/main.py`

The intended application setup at the end of the setup work was:

``` python
from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Backend API for the Todo Application",
)

app.include_router(api_router, prefix="/api/v1")

```

The API router is registered under `/api/v1`,
which gives the API a versioned URL prefix.

### `app/api/v1/health.py`

``` python
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "Todo API is running",
    }
```

### `app/api/v1/router.py`

``` python
from fastapi import APIRouter

from app.api.v1.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
```

Because `main.py` includes this router with the `/api/v1` prefix, the
health endpoint is:

``` text
GET /api/v1/health
```

------------------------------------------------------------------------

## 7. Tests

The test suite uses FastAPI's `TestClient`. It can make requests against
the application in tests without starting a separate Uvicorn server.

### `tests/test_main.py`

The test file was set up to cover the root and health endpoints:

``` python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

If the root endpoint returns `"Welcome to Todo API"`, change the root
assertion accordingly. The test must assert the actual contract
implemented by the endpoint.

### What was verified

-   pytest discovers test files in the configured `tests/` directory.
-   Test functions use the `test_` prefix.
-   `TestClient` can call the FastAPI application.
-   The root endpoint returns HTTP 200.
-   The health endpoint returns HTTP 200 and a healthy status.
-   The earlier test-discovery/path issue was corrected.
-   The Starlette deprecation warning was addressed by using `httpx2`.
-   The user confirmed that the setup and tests were working
    successfully without warnings.

Run the suite with:

``` powershell
uv run pytest -v
```

------------------------------------------------------------------------

## 8. Concepts Covered During Phase 1

The following concepts were discussed as part of learning the project
architecture:

### FastAPI and Uvicorn

-   **FastAPI** is the Python web framework used to define API routes,
    validate data, and build the backend.
-   **Uvicorn** is the ASGI server that runs the FastAPI application and
    accepts incoming HTTP requests.

### Layered application structure

-   **API/router layer:** receives HTTP requests and returns HTTP
    responses.
-   **Schema layer:** defines and validates request/response data using
    Pydantic.
-   **Service layer:** contains application/business rules.
-   **Model layer:** represents database tables and records using
    SQLAlchemy.
-   **Database layer:** manages database connectivity and sessions.
-   **Core layer:** contains shared configuration and other
    cross-cutting concerns.

These layers separate responsibilities. For example, a route should not
need to contain all the business rules and SQL queries itself.

### Router registration

A feature router defines endpoints for a particular area. The central
`router.py` collects feature routers, and `main.py` attaches the
combined router to the FastAPI application.

For example:

``` text
/api/v1 + /health = /api/v1/health
```

### API versioning

The `/api/v1` prefix identifies the first API version. A future
`/api/v2` can be introduced if the API contract needs to change
significantly.

### Automated testing

-   pytest automatically discovers test files and test functions that
    follow its naming conventions.
-   `-v` means verbose output.
-   `assert` checks whether an expected condition is true.
-   `TestClient` exercises endpoints without requiring a separately
    running server.

### Request flow (conceptual)

A future Todo creation request will broadly follow this path:

``` text
HTTP request
    |
    v
API router
    |
    v
Schema validation
    |
    v
Service/business logic
    |
    v
SQLAlchemy model + database session
    |
    v
MySQL database
    |
    v
Response returned to client
```

The model describes the database structure, while the database session
manages the interaction/transaction with the database. They have related
but different responsibilities.

------------------------------------------------------------------------

## 9. Phase 1 Completion Checklist

-   [x] Finalized the high-level technology stack.
-   [x] Chose FastAPI for the backend.
-   [x] Chose Vanilla JavaScript for the frontend.
-   [x] Chose JWT authentication with secure HttpOnly cookies.
-   [x] Chose MySQL, SQLAlchemy, Alembic, and PyMySQL for the database
    stack.
-   [x] Set up the backend package/directory structure.
-   [x] Set up `uv`, `pyproject.toml`, and `uv.lock`.
-   [x] Added runtime and development dependencies.
-   [x] Added Pydantic Settings configuration.
-   [x] Created `.env` and `.env.example`.
-   [x] Added ignore rules for local environment files and generated
    files.
-   [x] Created the FastAPI application in `app/main.py`.
-   [x] Created and registered the versioned API router.
-   [x] Added the health endpoint.
-   [x] Added endpoint tests.
-   [x] Corrected pytest test discovery configuration.
-   [x] Resolved the Starlette TestClient deprecation warning by
    switching to `httpx2`.
-   [x] Confirmed that the application and tests work.
-   [x] Confirm that `feature/project-setup` is committed, pushed, and
    merged into `main` (Git checkpoint was still awaiting confirmation).

------------------------------------------------------------------------

## 10. Next Phase --- Database Integration

The next planned phase is **Phase 2: Database Integration**.

The proposed feature branch, after Phase 1 has been safely merged, is:

``` bash
git switch main
git pull origin main
git switch -c feature/database-setup
```

The exact branch creation should happen only after the Phase 1 Git
checkpoint is complete.

### Phase 2 learning and implementation topics

1.  Understand relational databases and the basic MySQL concepts needed
    by this application.
2.  Understand what an ORM is and how SQLAlchemy maps Python classes to
    database tables.
3.  Configure the SQLAlchemy database engine and connection.
4.  Understand database sessions, transactions, and connection pooling.
5.  Configure Alembic for schema migrations.
6.  Create the initial `users` and `todos` table models when their
    requirements are ready.
7.  Generate and apply the first migration.
8.  Add tests that verify database connectivity and the database setup.

**Scope reminder:** The calendar is independent of Todo tasks. Do not
introduce calendar-to-task synchronization as part of this database
phase.

------------------------------------------------------------------------

## 11. Working Agreement for the Next Sessions

-   Continue backend-first.
-   Work on one feature branch at a time.
-   Explain the purpose of a concept before introducing its
    implementation.
-   Work in small checkpoints; run and verify code before moving
    forward.
-   Explain commands and code rather than asking the learner to copy
    large unexplained blocks.
-   Keep the MVP scope controlled and add advanced features later.
-   Test each feature before merging it into `main`.

**End of Phase 1 documentation.**
