# Project: API Testing with Python and pytest
# For SDET who knows Java

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Run with coverage
pytest --cov=api_client --cov-report=html -v

# Run specific test file
pytest test_basic.py -v

# Run tests with marker
pytest -m smoke

# Run slow tests
pytest -m slow

# Show print statements
pytest -s
```

## Project Structure
```
rest/
├── api_client.py          # API client for JSONPlaceholder
├── conftest.py            # Pytest fixtures
├── test_basic.py          # Basic endpoint tests
├── test_advanced.py       # Advanced fixture usage
├── test_validation.py     # Response validation tests
├── test_helpers.py        # Custom assertions and helpers
├── test_performance.py    # Performance and concurrency tests
├── test_integration.py    # End-to-end workflow tests
├── conftest_reporting.py  # Reporting configuration
└── requirements.txt       # Dependencies
```

## Key Concepts for Java SDETs

### Fixtures (like Test Rules/Extensions)
```python
# pytest fixtures are like JUnit's @Rule or @Extension
# They provide test fixtures (data, clients, setup/teardown)

@pytest.fixture
def api_client():
    return JSONPlaceholderClient()

@pytest.fixture
def new_post(api_client, data):
    post = api_client.create_post(**data)
    yield post  # Test runs here
    api_client.delete_post(post['id'])  # Cleanup after test
```

### Parametrization (like JUnit @ParameterizedTest)
```python
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post(post_id):
    post = client.get_post(post_id)
    assert post['id'] == post_id
```

### Markers (like @Tag)
```python
@pytest.mark.smoke
@pytest.mark.validation
@pytest.mark.slow
def test_something():
    pass
```

### Assertions (like AssertJ/FluentAssertions)
```python
# Built-in assertions (like assertj)
assert post['id'] == 1
assert 'title' in post
assert len(posts) > 0

# Custom assertions (like AssertJ's fluent API)
api_assert.assert_post_has_fields(post, ['id', 'title', 'body'])
api_assert.assert_post_data_matches(post, expected_data)
```

## Running Tests

```bash
# All tests
pytest -v

# With coverage
pytest --cov=api_client --cov-report=html -v

# Specific marker
pytest -m smoke

# Verbose with print statements
pytest -vs

# Stop at first failure
pytest -x

# Run specific test file
pytest test_validation.py -v

# Show fixture help
pytest --fixtures
```

## Best Practices Demonstrated

1. **Separation of Concerns**: Client layer vs test layer
2. **Fixtures for Setup/Cleanup**: Auto-cleanup resources
3. **Parametrization**: Test multiple scenarios
4. **Custom Assertions**: Domain-specific validation
5. **Performance Testing**: Response times, concurrency
6. **Integration Tests**: Complete workflows
7. **Error Handling**: Validate error responses

## Comparison: Java vs Python

| Java (JUnit)              | Python (pytest)           |
|---------------------------|---------------------------|
| @Test                     | def test_name():          |
| @ParameterizedTest        | @pytest.mark.parametrize  |
| @BeforeEach               | @pytest.fixture           |
| @BeforeAll                | @pytest.fixture(scope="module") |
| Assertions.assertTrue()   | assert                    |
| @Tag("smoke")             | @pytest.mark.smoke        |
| @Timeout                  | pytest.importorskip()     |
| Extension API             | conftest.py fixtures      |

## Notes

- Python uses duck typing, so type verification is at runtime
- Fixtures can depend on other fixtures (dependency injection)
- pytest automatically discovers test files (test_*.py, *_test.py)
- Use yield in fixtures for teardown code (after the yield)
- JSONPlaceholder is a fake REST API for testing
