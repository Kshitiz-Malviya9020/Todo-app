# CLAUDE.md --- Todo Application

> Project guide for Claude Code and contributors. Treat this file as the
> source of truth for project-level decisions. If implementation details
> are not yet specified, ask before introducing a new architectural
> decision.

## 1. Project Overview

Build a modern Todo application with a reliable backend-first
development process. The product will begin with a focused Minimum
Viable Product (MVP), then expand with advanced functionality in later
phases.

### Product goals

-   Let users securely manage their tasks.
-   Provide a maintainable API and a simple, responsive browser
    interface.
-   Integrate with Google Calendar as a planned calendar capability.
-   Keep the codebase modular so features can be developed
    independently.
-   Prioritize correctness, security, readability, and testability over
    premature complexity.

## 2. Confirmed Technology Decisions

  -----------------------------------------------------------------------
  Area                                Decision
  ----------------------------------- -----------------------------------
  Backend                             Python + FastAPI

  Frontend                            Vanilla JavaScript, HTML, and CSS

  Authentication                      JWT stored in secure HttpOnly
                                      cookies

  Calendar integration                Google Calendar

  Delivery strategy                   MVP first, then advanced features

  Implementation order                Backend first, then
                                      frontend/integration as appropriate
  -----------------------------------------------------------------------

Do not replace these choices with another framework or authentication
approach without discussing it first.

### Important implementation note

JWTs must not be placed in `localStorage` or `sessionStorage`. Use
HttpOnly cookies so browser JavaScript cannot read the token. Configure
cookie security deliberately: - `HttpOnly: true` - `Secure: true` in
HTTPS environments - An appropriate `SameSite` policy - A deliberate
path, expiry, and domain policy - CSRF protection appropriate to the
chosen cookie and request design

Never hard-code secrets, OAuth credentials, or API keys. Load them from
environment variables or a suitable secret store.

## 3. Architecture Principles

### Backend

-   Use FastAPI for HTTP APIs.
-   Keep routing, business logic, persistence, schemas, and
    configuration separated.
-   Use Pydantic models for request validation and response
    serialization.
-   Keep database access behind a clear persistence/data-access layer.
-   Use dependency injection for shared concerns such as database
    sessions and authenticated-user access.
-   Make authorization checks on the server for every user-owned
    resource.
-   Return consistent HTTP status codes and predictable error responses.
-   Add automated tests for business logic, API behavior,
    authentication, and authorization.

The database engine, ORM, migration tool, and deployment platform have
not yet been finalized. Do not silently assume them; propose options and
get agreement before locking them in.

### Frontend

-   Use plain HTML, CSS, and JavaScript. Do not introduce a frontend
    framework without approval.
-   Keep markup, styles, and JavaScript organized rather than placing
    the whole application in one file.
-   Encapsulate API communication in a small reusable client/module.
-   Use `credentials: "include"` for fetch requests that need the
    authentication cookie.
-   Do not attempt to read the JWT from JavaScript.
-   Handle loading, empty, success, and error states.
-   Keep the interface accessible: semantic HTML, labels, keyboard
    support, and visible focus states.
-   Avoid unsafe DOM insertion. Prefer `textContent` for user-provided
    text; sanitize content if HTML rendering is genuinely required.

### Google Calendar

Google Calendar is a planned integration. Treat it as a separate
integration boundary rather than coupling Google-specific logic to core
Todo business logic.

Before implementing it, confirm: - OAuth consent and redirect
configuration - Required Google Calendar scopes - Token storage and
refresh strategy - How application tasks map to calendar events - Sync
direction, conflict handling, and deletion behavior - User consent and
disconnect/revocation behavior

Do not expose Google OAuth tokens to frontend JavaScript or commit
credentials.

## 4. MVP-First Product Strategy

Implement a small, complete, testable MVP before advanced features.

The exact MVP feature list is still to be agreed. A sensible
implementation sequence to discuss and finalize is:

1.  Project foundation and configuration
2.  Database and persistence foundation
3.  User registration and login
4.  Authentication and authorization
5.  Core task CRUD (create, read, update, delete)
6.  Validation, error handling, and tests
7.  Frontend integration
8.  Google Calendar integration, after the core task flow is stable

Do not assume optional features---such as recurring tasks, reminders,
collaboration, labels, attachments, analytics, or real-time
updates---are part of the MVP unless explicitly approved.

For each feature, define: - User-visible behavior and acceptance
criteria - API contract and data model changes -
Authentication/authorization requirements - Validation and error cases -
Automated tests - Documentation updates

## 5. Git and Branching Workflow

The team uses a feature-branch workflow. Work on one feature or project
setup task at a time.

### Required lifecycle

1.  Start from an up-to-date `main` branch.
2.  Create a dedicated branch for the feature.
3.  Implement the feature on that branch.
4.  Run relevant tests, formatting, and checks.
5.  Review the diff and ensure no secrets, generated files, or unrelated
    changes are included.
6.  Commit the completed work with a clear message.
7.  Merge the feature branch into `main`.
8.  Push the updated `main` branch to the remote.
9.  Delete the feature branch after the merge is confirmed.
10. Update the local checkout from the latest remote `main` before
    starting the next feature.

### Branch naming

Use descriptive, lowercase names with hyphens and a type prefix:

-   `feature/<short-description>` --- new functionality
-   `fix/<short-description>` --- bug fixes
-   `refactor/<short-description>` --- structural changes without
    intended behavior changes
-   `docs/<short-description>` --- documentation-only work
-   `test/<short-description>` --- test-only work
-   `chore/<short-description>` --- tooling or maintenance

Example: `feature/user-authentication`

### Git safety rules

-   Never commit directly to `main`.
-   Never force-push shared branches unless explicitly authorized.
-   Never use destructive Git commands to discard user work.
-   Do not merge with failing tests or unresolved conflicts.
-   Do not delete a feature branch until its changes are safely merged
    and the merge is pushed.
-   Before running a command that may overwrite, reset, clean, or delete
    work, inspect the repository state and explain the impact.
-   Keep commits focused and messages descriptive.

### Typical command sequence

Adapt commands to the actual remote name and repository state:

``` bash
git switch main
git pull --ff-only origin main
git switch -c feature/<short-description>

# Implement the feature, then run tests and checks.

git status
git diff
git add <relevant-files>
git commit -m "feat: describe the feature"

git switch main
git pull --ff-only origin main
git merge --no-ff feature/<short-description>
# Run the relevant checks again after merging.
git push origin main

git branch -d feature/<short-description>
git push origin --delete feature/<short-description>

git pull --ff-only origin main
```

If the project uses a pull-request review process or branch protection,
follow that process instead of bypassing it.

## 6. Coding Standards

-   Prefer simple, explicit, maintainable code.
-   Use meaningful names and small functions with clear
    responsibilities.
-   Avoid unnecessary abstractions and premature optimization.
-   Keep business rules out of route handlers and UI event handlers
    where practical.
-   Validate all external input at system boundaries.
-   Handle expected failures explicitly; do not hide errors with broad
    empty exception handlers.
-   Add type hints to Python code.
-   Keep dependencies minimal and justify new dependencies.
-   Keep configuration environment-specific and out of source code.
-   Update or add tests whenever behavior changes.
-   Document non-obvious decisions and integration constraints.

Follow the formatting, linting, and test tools already configured in the
repository. If none exist, propose a minimal toolchain before adding it.

## 7. API and Data Design Guidelines

-   Use resource-oriented, consistently named endpoints.
-   Version the API if/when a compatibility strategy is needed; do not
    add versioning without a project decision.
-   Use Pydantic request and response schemas; do not expose database
    models directly.
-   Return only fields the caller is authorized to see.
-   Scope every task query and mutation to the authenticated owner.
-   Use pagination for potentially unbounded collections.
-   Define timestamp and timezone behavior consistently.
-   Avoid leaking stack traces, secrets, internal paths, or sensitive
    user information in API responses.

The exact task fields and user model are not finalized. Confirm the data
model before implementing migrations or public API contracts.

## 8. Security Requirements

Security is part of the implementation, not a later polish step.

-   Hash passwords using a modern password-hashing algorithm through a
    maintained library. Never store plaintext passwords.
-   Keep JWT signing keys and OAuth secrets outside version control.
-   Validate JWT signature, expiry, issuer/audience where configured,
    and relevant claims.
-   Enforce ownership and authorization checks server-side.
-   Use HTTPS in production.
-   Configure CORS narrowly for the actual frontend origin(s); do not
    use permissive wildcard settings with credentialed requests.
-   Design CSRF defenses for cookie-authenticated state-changing
    requests.
-   Rate-limit sensitive endpoints such as login and registration where
    appropriate.
-   Avoid logging passwords, tokens, session cookies, or OAuth
    credentials.
-   Keep dependencies updated and review security advisories.
-   Provide safe handling for logout, token expiry, and invalid
    credentials.

## 9. Testing and Quality Gates

For each feature:

-   Add unit tests for isolated business logic.
-   Add API/integration tests for endpoint behavior and persistence.
-   Test unauthenticated access and cross-user access denial.
-   Test validation failures and relevant edge cases.
-   Test frontend behavior for loading, success, empty, and error states
    where applicable.
-   Run the complete relevant test suite before merging.

A feature is not complete merely because the happy path works.

## 10. Working Instructions for Claude Code

When working in this repository:

1.  Inspect the current directory, repository status, existing files,
    and project conventions before editing.
2.  Read relevant documentation and code before proposing changes.
3.  Confirm the active branch. Do not work on `main`.
4.  Work only on the feature currently requested; avoid unrelated
    refactors.
5.  Prefer small, reviewable changes.
6.  Do not invent project decisions that are still open. Identify
    assumptions and ask for confirmation when they affect architecture,
    security, data contracts, or dependencies.
7.  Do not overwrite existing files without inspecting their contents.
8.  Do not add secrets, credentials, real user data, or local
    environment files to commits.
9.  Run appropriate tests and checks, and report exactly what was run
    and whether it passed.
10. Summarize changed files, key implementation choices, tests, and any
    remaining work.
11. Do not merge, push, or delete branches unless the user has asked for
    that step or the current task explicitly authorizes it.
12. If a requested operation is destructive or irreversible, explain the
    impact and obtain confirmation first.

### Definition of Done

A feature is complete when: - Acceptance criteria are met. -
Implementation follows the agreed architecture. - Input validation,
authorization, and error handling are covered. - Relevant automated
tests pass. - No secrets or unrelated changes are present. -
Documentation is updated where needed. - The diff has been reviewed. -
The feature is ready to merge through the agreed Git workflow.

## 11. Open Decisions to Finalize

Do not treat these as settled until the project owner confirms them:

-   Database (for example, PostgreSQL or SQLite for local development)
-   ORM and migration tool
-   Exact MVP task and account requirements
-   Task fields, statuses, priorities, due dates, and timezone rules
-   Access-token lifetime and refresh-token/session strategy
-   CSRF approach and cookie `SameSite` policy
-   Frontend directory/build/serving strategy
-   API route naming and versioning policy
-   Test, lint, and formatting toolchain
-   Google Calendar sync behavior and OAuth configuration
-   Deployment, hosting, observability, and backup strategy
-   Whether merges are direct or require pull requests and review

## 12. Current Project Direction

The confirmed starting direction is:

-   Build the backend first.
-   Develop each feature on its own branch.
-   Complete and verify the feature before merging.
-   Merge into `main`, push the updated `main`, and remove the completed
    feature branch.
-   Start the next feature from the latest `main`.
-   Deliver the MVP before moving to advanced features.

When in doubt, preserve these decisions and ask before changing them.
