# Documentation Patterns and Examples

Complete templates, before/after transformations, and anti-patterns to avoid.

## Table of Contents

1. [Code Documentation Templates](#code-documentation-templates)
2. [Architecture Documentation Templates](#architecture-documentation-templates)
3. [README Template](#readme-template)
4. [Before/After Examples](#beforeafter-examples)
5. [Common Anti-Patterns](#common-anti-patterns)

---

## Code Documentation Templates

### Function Docstring Template

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    One-sentence description of what this function does.

    Explain WHY this function exists and WHEN to use it. Describe any
    non-obvious behavior, side effects, or important constraints.

    Args:
        param1: Description including expected format and constraints.
        param2: Description. Use "Optional; defaults to X" for defaults.

    Returns:
        Description of return value and its meaning.

    Raises:
        ValueError: When and why this exception is raised.

    Example:
        >>> result = function_name("input", max_items=10)
        >>> result.status
        'success'
    """
```

### Module Header Template

```python
"""
Module Name: brief_description

Why: Explain the purpose and business context. What problem does this module solve?
Scope: What belongs here and what doesn't. Link to related modules.
Architecture: How this module fits into the larger system (2-3 sentences).

Key Components:
    - ClassA: Responsible for X
    - function_b: Handles Y

Usage:
    See docs/usage.md or the Quick Start section in README.md
"""
```

### API Endpoint Documentation Template

```markdown
## POST /api/v1/users

Create a new user account.

### Why Use This

Use this endpoint when a new user completes the registration form.
The endpoint handles validation, password hashing, and sends a welcome email.

### Request

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "secure_password_123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email, max 255 chars |
| name  | string | Yes | Display name, 2-100 chars |
| password | string | Yes | Min 8 chars, must include number |

### Response (201 Created)

```json
{
  "id": "usr_1234567890",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Cases

| Status | Code | When It Happens |
|--------|------|----------------|
| 400 | EMAIL_EXISTS | Email already registered |
| 400 | INVALID_PASSWORD | Password doesn't meet requirements |
| 429 | RATE_LIMITED | More than 10 requests per minute |

### Core Logic Flow

```
Request → Validate JSON schema → Check email uniqueness
  → Hash password → Insert to DB → Send welcome email → Return user
```

Note: Password hashing uses bcrypt (12 rounds). Takes ~250ms by design.
```

---

## Architecture Documentation Templates

### System Overview Template

```markdown
# System Name — Architecture Overview

## In One Sentence

[One-line description of what this system does and who uses it.]

## System Context (C4 Level 1)

```
[External User] --uses--> [Our System]
[Our System] --charges via--> [Payment Provider]
[Our System] --sends emails via--> [Email Service]
[Admin] --manages--> [Our System]
```

- **External User**: End customers who [do what].
- **Payment Provider**: Stripe. Handles card processing and invoicing.
- **Email Service**: SendGrid. Transactional emails and newsletters.
- **Admin**: Internal staff who manage users and view reports.

## Container Diagram (C4 Level 2)

```
[User] --> [Web Frontend : Next.js]
[Admin] --> [Admin Dashboard : React]
[Web Frontend] --REST API--> [API Gateway : Kong]
[Admin Dashboard] --REST API--> [API Gateway]
[API Gateway] --routes to--> [Core API : Python/FastAPI]
[API Gateway] --routes to--> [Auth Service : Go]
[Core API] --reads/writes--> [Primary DB : PostgreSQL]
[Core API] --caches in--> [Cache : Redis]
[Core API] --publishes--> [Message Bus : Redis Streams]
[Worker] --consumes from--> [Message Bus]
[Worker] --writes to--> [Object Storage : S3]
```

### Container Descriptions

| Container | Technology | Responsibility |
|-----------|-----------|----------------|
| Web Frontend | Next.js | Customer-facing UI, SSR, static pages |
| Admin Dashboard | React | Internal admin interface, user management |
| API Gateway | Kong | Rate limiting, auth, request routing |
| Core API | Python/FastAPI | Business logic, CRUD operations |
| Auth Service | Go | JWT issuance, token validation, OAuth |
| Primary DB | PostgreSQL | User data, transactions, relational data |
| Cache | Redis | Session storage, query result caching |
| Message Bus | Redis Streams | Async task queue |
| Worker | Python/Celery | Background jobs: emails, reports, imports |
| Object Storage | S3 | File uploads, exports, static assets |

## Data Flow: User Registration

```
[User] --(1) POST /register--> [Web Frontend]
[Web Frontend] --(2) POST /api/v1/users--> [API Gateway]
[API Gateway] --(3) validate token--> [Auth Service]
[API Gateway] --(4) forward request--> [Core API]
[Core API] --(5) insert--> [Primary DB]
[Core API] --(6) publish event--> [Message Bus]
[Worker] --(7) consume event--> [Message Bus]
[Worker] --(8) send email--> [Email Service]
[Email Service] --(9) deliver--> [User]
```

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| API Framework | FastAPI over Django | Lighter, native async, auto OpenAPI docs |
| Auth Separation | Dedicated Go service | Centralized auth across all services |
| Message Queue | Redis Streams over RabbitMQ | Already running Redis, lower operational cost |
| Frontend | Next.js over plain React | SSR for SEO, built-in API routes |
```

### Architecture Decision Record (ADR) Template

```markdown
# ADR-XXX: [Short Title]

## Status

- Proposed / Accepted / Deprecated / Superseded by ADR-YYY

## Context

What is the problem? What forces are at play? What constraints exist?
Be specific: mention scale, team size, budget, timeline.

## Options Considered

### Option A: [Name]

- Pros: ...
- Cons: ...
- Effort: [Low/Medium/High]

### Option B: [Name]

- Pros: ...
- Cons: ...
- Effort: [Low/Medium/High]

## Decision

We will [specific choice].

## Rationale

[Explain why the chosen option is best given the context. Be honest about trade-offs.]

## Consequences

### Positive
- ...

### Negative
- ...

### Mitigations
- [How we will address the negative consequences]

## References
- [Link to related ADRs, issues, or external resources]
```

---

## README Template

```markdown
# Project Name

One-sentence description: what this project does and who it's for.

## Quick Start (copy-paste to run)

```bash
# Install
git clone https://github.com/org/repo.git
cd repo && npm install

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
npm run dev
# Open http://localhost:3000
```

## What This Does

2-3 paragraphs explaining the core purpose. Use an analogy if helpful.

Example: "Think of this as a smart filing cabinet. You drop in documents,
it automatically categorizes them, and you can find anything in seconds."

## Architecture

```
[Diagram or ASCII art showing 3-5 main components and their relationships]
```

| Component | Purpose |
|-----------|---------|
| Component A | What it does |
| Component B | What it does |

## Core Concepts

### Concept 1

Brief explanation with example.

### Concept 2

Brief explanation with example.

## Documentation

| Document | What You'll Find |
|----------|-----------------|
| [docs/install.md](docs/install.md) | Detailed installation and configuration |
| [docs/architecture.md](docs/architecture.md) | System design and data flows |
| [docs/api.md](docs/api.md) | API reference and examples |
| [docs/development.md](docs/development.md) | Contributing, local setup, testing |

## Project Structure

```
repo/
  src/           # Source code
  tests/         # Test files
  docs/          # Documentation
  scripts/       # Utility scripts
```
```

---

## Before/After Examples

### Example 1: Code Comment

**Before (vague):**
```python
def process_data(data):
    # Process the data
    result = transform(data)
    return result
```

**After (clear):**
```python
def normalize_user_records(raw_records):
    """Convert mixed-format user records into standard User objects.

    Handles three legacy formats from the 2019-2021 migration:
    - v1: flat JSON with snake_case keys
    - v2: nested JSON with camelCase keys  
    - v3: CSV with positional columns

    All formats are normalized to the current User schema.
    See docs/migrations.md for format details.
    """
    normalized = convert_legacy_formats(raw_records)
    return validate_and_create_users(normalized)
```

### Example 2: Architecture Description

**Before (abstract):**
> The system uses a microservices architecture with event-driven
> communication patterns. Services are loosely coupled and communicate
> through a message broker. Data is eventually consistent across the system.

**After (concrete):**
> The system has 4 services: API (handles requests), Orders (processes purchases),
> Inventory (tracks stock), and Notifications (sends emails). They talk through
> Redis Streams.
>
> When a user buys something:
> 1. API receives the request and forwards to Orders
> 2. Orders checks Inventory via API call
> 3. If in stock, Orders saves the order and publishes an "order_placed" event
> 4. Inventory consumes the event and decrements stock
> 5. Notifications consumes the event and sends a confirmation email
>
> Stock numbers may lag behind by a few seconds (eventual consistency).
> This is acceptable because we over-reserve inventory by 5%.

### Example 3: API Documentation

**Before (mechanistic):**
> ## GET /api/v1/items
> Retrieves a list of items from the database. Supports pagination
> and filtering. Returns JSON array of item objects.

**After (purpose-driven):**
> ## GET /api/v1/items
>
> List products with optional filtering and pagination.
>
> Use this to populate product catalog pages, search results, or
> admin inventory views. For real-time stock levels, use the
> WebSocket endpoint instead — this data is cached and may be
> stale by up to 60 seconds.
>
> ```
> GET /api/v1/items?category=electronics&page=1&limit=20
> ```

### Example 4: README Introduction

**Before:**
> This is a high-performance, scalable data processing pipeline built
> with modern technologies. It leverages stream processing and
> distributed computing to handle large volumes of data efficiently.

**After:**
> # Data Pipeline
>
> Takes CSV files from your SFTP server, validates and transforms them,
> and loads the results into your data warehouse. Handles files up to
> 10GB and processes about 1000 rows per second.
>
> Used by the analytics team to load daily sales data.

---

## Common Anti-Patterns

### 1. The Jargon Dump

> "Leveraging synergistic microservices architecture with polyglot persistence..."

**Fix**: Use concrete terms. Say "We use 3 services: API (Python), Database (Postgres), Cache (Redis)."

### 2. The Obvious Comment

```python
i += 1  # Increment i by one
```

**Fix**: Delete it. Comments should explain why, not what.

### 3. The Missing "Why"

```python
# Use timeout of 30 seconds
timeout = 30
```

**Fix**: Explain the reasoning.
```python
# 30s: 99th percentile response time is 8s. 30s allows for 3 retries
# with backoff. See ADR-007 for timeout policy rationale.
timeout = 30
```

### 4. The Wall of Text

A 50-line paragraph describing the architecture with no breaks, no lists, no diagrams.

**Fix**: Break into sections. Use bullet points. Add a diagram. No section should exceed 10 lines.

### 5. The Orphan Document

A design doc that says "The system uses Kafka" with no version, no date, no link to code.

**Fix**: Every document needs: author, date, status, and links to related docs/code.

### 6. The Mixed-Purpose Document

A document that tries to be tutorial, reference, and explanation simultaneously.

**Fix**: Split by purpose. Cross-link between documents. One doc, one job.

### 7. "Simply" and "Just"

> "Simply run the migration" / "Just update the config"

**Fix**: Remove these words. They imply the task is trivial and make readers feel stupid when they struggle.

### 8. Undocumented Assumptions

Code that assumes specific knowledge without stating it.

```python
def calculate_price(items):
    # Apply tiered pricing
    ...
```

**Fix**: Document the business rules.
```python
def calculate_price(items):
    """Apply volume discounts: 100+ items = 10% off, 500+ = 20% off.
    
    Pricing tiers defined by Sales team (see ticket PROJ-1234).
    Updated 2024-03 when enterprise tier was added.
    """
    ...
```
