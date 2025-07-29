# Testing Guide

This document explains how to run and manage tests for the InvestEasy Web API.

## Test Discovery in VS Code

Tests should be automatically discovered in VS Code. If they're not appearing:

1. Ensure you have the Python extension installed
2. Check that the Python interpreter is correctly set to Conda (/opt/homebrew/Caskroom/miniconda/base/bin/python)
3. Look at the test explorer panel (View → Testing)
4. If tests don't appear, try:
   - Reload VS Code window (Cmd+Shift+P → "Developer: Reload Window")
   - Clear pytest cache: `python -m pytest --cache-clear`
   - Restart the Python language server

## Running Tests

### From VS Code
- Open the Test Explorer (View → Testing)
- Click on individual tests to run them
- Use the "Run Tests" button to run all tests
- Use "Debug Tests" to run with debugging

### From Command Line

```bash
# Run all tests
cd invest-easy-webapi
python -m pytest

# Run specific test file
python -m pytest tests/infrastructure/test_akshare_service.py

# Run specific test class
python -m pytest tests/infrastructure/test_akshare_service.py::TestAkshareService

# Run specific test method
python -m pytest tests/infrastructure/test_akshare_service.py::TestAkshareService::test_parse_code

# Run with verbose output
python -m pytest -v

# Run with coverage
python -m pytest --cov=app --cov-report=html
```

### Using the Test Runner Script

```bash
# Run all tests
cd invest-easy-webapi
python test_runner.py

# Run specific tests
python test_runner.py tests/infrastructure/test_akshare_service.py -v
```

## Test Structure

```
tests/
├── README.md          # This file
├── infrastructure/
│   └── test_akshare_service.py  # Tests for Akshare service
└── (other test modules will go here)
```

## Writing New Tests

1. Create test files in the appropriate subdirectory under `tests/`
2. Name test files with `test_` prefix
3. Name test classes with `Test` prefix
4. Name test methods with `test_` prefix
5. Use pytest fixtures and parametrization where appropriate

Example test structure:

```python
import pytest

class TestExample:
    def test_something(self):
        # Arrange
        # Act
        # Assert
        assert True
```

## Test Dependencies

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

## Continuous Integration

Tests are run automatically in CI/CD pipelines. Ensure all tests pass before pushing changes.

## Troubleshooting

### Tests Not Discovered
1. Check VS Code Python interpreter setting
2. Verify pytest is installed in the environment
3. Check `.vscode/settings.json` configuration
4. Try running `python -m pytest --collect-only` to see if pytest can find tests

### Import Errors
1. Ensure you're running tests from the `invest-easy-webapi` directory
2. Check that `__init__.py` files exist in package directories
3. Verify Python path includes the project root

### Async Test Issues
1. Tests use `pytest-asyncio` plugin
2. Async tests should be marked as `async def`
3. Use appropriate asyncio mode (currently set to strict)

## Configuration

- `pytest.ini`: Main pytest configuration
- `.vscode/settings.json`: VS Code specific settings
- `requirements-test.txt`: Test dependencies
