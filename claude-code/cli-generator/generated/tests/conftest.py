"""Pytest fixtures for md_convert tests."""

import pytest
from pathlib import Path
import tempfile


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_markdown(temp_dir: Path) -> Path:
    """Create a sample markdown file for testing."""
    md_file = temp_dir / "sample.md"
    md_file.write_text("""# Sample Document

This is a sample markdown document.

## Code Example

```python
def hello():
    print("Hello, World!")
```

## Lists

- Item 1
- Item 2
- Item 3
""")
    return md_file


@pytest.fixture
def sample_markdown_dir(temp_dir: Path) -> Path:
    """Create a directory with multiple markdown files."""
    docs_dir = temp_dir / "docs"
    docs_dir.mkdir()

    # Create multiple markdown files
    for i in range(3):
        (docs_dir / f"doc{i}.md").write_text(f"# Document {i}\n\nContent for document {i}.")

    # Create a subdirectory with more files
    subdir = docs_dir / "subdir"
    subdir.mkdir()
    (subdir / "nested.md").write_text("# Nested Document\n\nNested content.")

    return docs_dir
