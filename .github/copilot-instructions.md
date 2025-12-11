# Copilot Instructions for ASWE Copilot 2025 Workshop

## Project Overview
This is an educational workshop repository for learning agentic software engineering with GitHub Copilot. Contains a FastAPI+HTMX todo app (`todo-app/`) and structured exercises (`docs/exercises/`).

## Architecture & Tech Stack

### Todo App (`todo-app/`)
- **Backend**: FastAPI with SQLAlchemy ORM, SQLite database
- **Frontend**: HTMX + Shoelace Web Components (no build step)
- **Templates**: Jinja2 with utility functions injected into template globals
- **Auth**: Mock sessions (UUID cookies) - educational only, plain text passwords
- **Package Management**: `uv` (10-100x faster than pip)

### Key Patterns
- **Src Layout**: Code in `src/app/`, tests in `tests/`, follows modern Python conventions
- **Route Organization**: Modular routes in `routes/` (auth, pages, todos, todo_lists)
- **HTMX Integration**: Server-side rendering with SPA-like UX, extensive use of `hx-*` attributes
- **Template Partials**: Reusable components in `templates/partials/` for dynamic updates

## Critical Commands & Workflows

```bash
# Start todo app (from todo-app/ directory)
./run.sh                    # Auto-sync deps + start server
uv run uvicorn app.main:app --reload

# Testing
uv run pytest tests/ -v     # Run all tests
uv run pytest tests/test_specific.py  # Run specific test

# Dependencies
uv add package-name         # Add runtime dependency
uv add --dev package-name   # Add dev dependency
uv sync                     # Install/sync all dependencies
```

## Development Guidelines

### From `docs/rules/`:
- **Critical Rules**: Be concise, make surgical changes, never reformat entire project
- **KISS/YAGNI**: Prefer simple solutions, avoid over-engineering
- **No Broken Windows**: Fix issues immediately, ensure tests pass
- **Src Layout**: Always use `src/` for packages, follow established structure

### Python Specifics
- Use `uv` for all package management (not pip/poetry)
- Type hints required, follow modern Python practices
- Tests use in-memory SQLite with dependency override pattern
- Database models use UUID primary keys, UTC timestamps

## Code Patterns & Conventions

### HTMX Patterns
```html
<!-- Standard HTMX form with OOB swaps -->
<form hx-post="/api/todos" hx-target="#todo-list" hx-swap="innerHTML">
  <!-- Template partials handle dynamic updates -->
</form>

<!-- Out-of-band swaps for side effects -->
<div id="sidebar-count" hx-swap-oob="innerHTML">{{ count }}</div>
```

### FastAPI Route Organization
```python
# Route verification pattern
def _verify_list_access(db: Session, list_id: str, user_id: str) -> TodoList | None:
    """Verify user owns resource and return it."""
    
# Template globals injection (main.py)
templates.env.globals["utility_function"] = utility_function
```

### Testing Patterns
```python
# Dependency override pattern (conftest.py)
app.dependency_overrides[get_db] = override_get_db

# In-memory database per test
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", ...)
```

## File Structure Reference

```
todo-app/src/app/
├── main.py              # FastAPI app, template globals, demo data seeding
├── database.py          # SQLAlchemy models (User, TodoList, Todo)
├── utils.py            # Date formatting, template utilities
├── core/deps.py        # Auth dependencies, session management
├── models/             # Pydantic validation models
├── routes/             # Modular API routes
├── templates/          # Jinja2 templates + partials/
└── static/             # CSS/JS assets
```

## Workshop Context
- Educational focus - prioritize clarity over production practices
- Mock auth system - no real security (documented limitation)  
- SQLite with plain text passwords for simplicity
- Exercises progress from basics → agent mode → complex features
- Follow critical rules in `docs/rules/CRITICAL-RULES-AND-GUARDRAILS.md`

## Integration Points
- **Database**: SQLAlchemy with relationship cascades, indexed queries
- **Templates**: Server-side rendering with HTMX partial updates  
- **Sessions**: In-memory dict with UUID cookies (non-persistent)
- **Static Assets**: Served via FastAPI StaticFiles mount
