---
name: python-fastapi-uv
description: Python project setup and development using uv package manager and FastAPI conventions. Use when creating new Python projects, setting up FastAPI applications, managing dependencies, or configuring development environments.
---

# Python + uv + FastAPI Best Practices

## When This Skill Applies

Activate this skill when:
- Creating a new Python project or FastAPI application
- Adding, removing, or updating dependencies
- Setting up virtual environments or workspaces
- Running Python scripts or tools
- Configuring pyproject.toml

## Project Setup with uv

### Initialize New Project
```bash
uv init <project-name>
cd <project-name>
uv add fastapi uvicorn[standard]
```

### Required pyproject.toml Structure
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Clear, concise description"
requires-python = ">=3.11"
dependencies = []

[project.scripts]
project-name = "project_name.main:main"

[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.27",  # For FastAPI TestClient
    "ruff>=0.4",
]
```

### Standard Project Structure
```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py          # FastAPI app factory
│       ├── config.py        # Settings with pydantic-settings
│       ├── routers/         # API route modules
│       ├── models/          # Pydantic models
│       ├── services/        # Business logic
│       └── dependencies.py  # Shared dependencies
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── pyproject.toml
└── README.md
```

## Dependency Management

### Adding Dependencies
```bash
uv add <package>              # Production dependency
uv add --dev <package>        # Development dependency
uv add "package>=1.0,<2.0"    # With version constraints
```

### Syncing Environment
```bash
uv sync                       # Install all dependencies from lock
uv sync --frozen              # Fail if lock file outdated
```

### Lock File
- Always commit `uv.lock` to version control
- Run `uv lock` after modifying pyproject.toml
- Use `uv lock --upgrade` to update all dependencies

## Running Code

### Scripts and Commands
```bash
uv run python script.py       # Run with project's Python
uv run pytest                  # Run project tools
uv run uvicorn app.main:app --reload  # Run FastAPI dev server
```

### Inline Script Dependencies
```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
```

## FastAPI Application Pattern

### App Factory (main.py)
```python
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="Project Name",
        version="0.1.0",
    )

    # Include routers
    from .routers import items, users
    app.include_router(items.router, prefix="/items", tags=["items"])
    app.include_router(users.router, prefix="/users", tags=["users"])

    return app

app = create_app()
```

### Router Pattern
```python
from fastapi import APIRouter, Depends, HTTPException, status
from ..models.item import ItemCreate, ItemResponse
from ..services.item_service import ItemService

router = APIRouter()

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    service: ItemService = Depends(),
) -> ItemResponse:
    """Create a new item."""
    return await service.create(item)
```

### Pydantic Models
```python
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    model_config = {"from_attributes": True}
```

## Do NOT

- Use `pip install` directly - always use `uv add`
- Create requirements.txt - use pyproject.toml
- Skip type hints on function signatures
- Use sync functions where async is appropriate
- Put all code in a single file - use proper project structure
- Hardcode configuration - use pydantic-settings
- Skip Pydantic models for request/response validation
