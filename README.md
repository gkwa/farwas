# farwas

## Development Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest
```

## Running Tests

```bash
pytest tests/
```

For coverage report:
```bash
pytest tests/ --cov=farwas --cov-report=term-missing
```
