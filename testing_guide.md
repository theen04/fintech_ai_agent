# Testing Guide

This document provides the steps and code required to run automated test scripts.

## Setup

### Install Testing Tools

``` bash
# If you haven't already
pip install pytest pytest-cov

# Or install everything from requirements.txt
pip install -r requirements.txt
```

### Verify Installation

``` bash
pytest --version
# Should show: pytest 8.3.4 or similar
```

------------------------------------------------------------------------

## Running Tests

### Basic Usage

``` bash
# Run all tests
pytest test_main.py

# Run with verbose output (shows each test name)
pytest test_main.py -v

# Run with extra verbose output (shows print statements)
pytest test_main.py -vv
```

### Run Specific Tests

``` bash
# Run one test class
pytest test_main.py::TestDuckDuckGoTool -v

# Run one specific test
pytest test_main.py::TestDuckDuckGoTool::test_successful_search -v

# Run tests matching a pattern
pytest test_main.py -k "search" -v
```

### Coverage Reports

``` bash
# Run with coverage
pytest test_main.py --cov=tools --cov=main

# Generate HTML coverage report
pytest test_main.py --cov=tools --cov=main --cov-report=html

# Open the report
open htmlcov/index.html  # Mac
# or
start htmlcov/index.html  # Windows
# or
xdg-open htmlcov/index.html  # Linux
```

------------------------------------------------------------------------

## Understanding the Tests

### Test Structure

Our tests follow the **Arrange-Act-Assert** pattern:

``` python
def test_example():
    # ARRANGE: Set up test data and mocks
    mock_data = {"key": "value"}
    
    # ACT: Execute the function being tested
    result = my_function(mock_data)
    
    # ASSERT: Verify the result
    assert result == expected_value
```

### Testing Scope

#### 1. Tool Tests (Unit Tests)

**Purpose**: Test each tool in isolation

``` python
class TestDuckDuckGoTool:
    """Tests the search functionality without hitting real API"""
    
    @patch('duckduckgo_search.DDGS')  # Mock the external API
    def test_successful_search(self, mock_ddgs):
        # Arrange: Set up mock response
        mock_ddgs.return_value.text.return_value = [...]
        
        # Act: Call the tool
        result = duckduckgo_tool.invoke({"query": "test"})
        
        # Assert: Check the result
        assert "expected text" in result
```

**Why Mock?**

-  Tests run offline (no internet needed)
-  Tests are fast (no API delays)
-  Tests are free (no API costs)
-  Tests are reliable (no API downtime)

#### 2. Validation Tests

**Purpose**: Ensure Pydantic models catch bad data

``` python
def test_missing_required_field():
    """Pydantic should raise error for missing fields"""
    with pytest.raises(ValidationError):
        ResearchResponse(topic="Test")  # Missing other required fields
```

#### 3. Integration Tests (Skipped by Default)

**Purpose**: Test the whole agent with real APIs

``` python
@pytest.mark.integration
@pytest.mark.skip(reason="Costs money and requires API keys")
def test_full_agent():
    # Would test everything together
    pass
```

These are skipped because: 
- They cost money (real API calls) 
- They're slow (network delays) 
- They require API keys 
- They can be flaky (network issues)

------------------------------------------------------------------------

## Test Output Explained

### Successful Test Run

```         
test_main.py::TestDuckDuckGoTool::test_successful_search PASSED     [10%]
test_main.py::TestDuckDuckGoTool::test_empty_search_results PASSED  [20%]
test_main.py::TestCalculator::test_simple_addition PASSED           [30%]

========================== 15 passed in 0.24s ==========================
```

**What this means**: 
- ✅ All tests passed 
- ✅ Took 0.24 seconds (very fast!) 
- ✅ 15 tests ran successfully

### Failed Test Run

```         
test_main.py::TestDuckDuckGoTool::test_successful_search FAILED     [10%]

_________________________________ FAILURES __________________________________
__________ TestDuckDuckGoTool.test_successful_search ___________

    def test_successful_search(self, mock_ddgs):
>       assert "Test Result 1" in result
E       AssertionError: assert 'Test Result 1' in 'Error: ...'

test_main.py:45: AssertionError
========================== 1 failed, 14 passed in 0.26s =================
```

**What this means**: 
- ❌ One test failed 
- ✅ 14 tests passed 
- The failure shows exactly what went wrong (line 45) 
- The `E` line shows the actual vs expected

------------------------------------------------------------------------

## Writing Your Own Tests

### Testing a New Tool

``` python
from tools import your_new_tool
from unittest.mock import patch

class TestYourNewTool:
    """Tests for your new tool."""
    
    @patch('module.ExternalAPI')  # Mock external dependency
    def test_successful_operation(self, mock_api):
        """Test the happy path."""
        # Arrange
        mock_api.return_value.method.return_value = "expected data"
        
        # Act
        result = your_new_tool.invoke({"param": "value"})
        
        # Assert
        assert "expected data" in result
        
    def test_error_handling(self):
        """Test that errors are handled gracefully."""
        # Arrange
        bad_input = {"invalid": "data"}
        
        # Act
        result = your_new_tool.invoke(bad_input)
        
        # Assert
        assert "Error" in result
```

### Testing Best Practices

1.  **Test One Thing Per Test**

    ``` python
    # ❌ Bad: Tests multiple things
    def test_everything():
        assert tool_works()
        assert tool_handles_errors()
        assert tool_validates_input()

    # ✅ Good: Separate tests
    def test_tool_works():
        assert tool_works()

    def test_tool_handles_errors():
        assert tool_handles_errors()
    ```

2.  **Use Descriptive Names**

    ``` python
    # ❌ Bad
    def test_1():
        pass

    # ✅ Good
    def test_successful_search_returns_formatted_results():
        pass
    ```

3.  **Test Edge Cases**

    ``` python
    def test_empty_input():
        """What happens with empty string?"""

    def test_none_input():
        """What happens with None?"""

    def test_very_long_input():
        """What happens with 10,000 characters?"""
    ```

------------------------------------------------------------------------

## Test Coverage

### What is Coverage?

Coverage shows what percentage of your code is tested:

```         
Name         Stmts   Miss  Cover
--------------------------------
tools.py        45      5    89%
main.py         60     15    75%
--------------------------------
TOTAL          105     20    81%
```

**What this means**:   
- **Stmts**: Total lines of code 
- **Miss**: Lines not tested 
- **Cover**: Percentage tested

**Good targets**: 
- 80%+ coverage is excellent 
- 60-80% is good 
- <60% needs more tests

### Improving Coverage

``` bash
# See which lines aren't tested
pytest test_main.py --cov=tools --cov-report=term-missing

# Output shows:
tools.py    89%    45-47, 89
           ^      ^
           |      Lines not covered
           Coverage %
```

Then write tests for those lines!

------------------------------------------------------------------------

## Common Testing Patterns

### 1. Mocking External APIs

``` python
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"data": "value"}
    result = my_function()
    assert result == "value"
```

### 2. Testing File Operations

``` python
def test_file_save(tmp_path):  # tmp_path is a pytest fixture
    filepath = tmp_path / "test.txt"
    save_file(filepath, "content")
    assert filepath.read_text() == "content"
```

### 3. Testing Exceptions

``` python
def test_raises_error():
    with pytest.raises(ValueError):
        dangerous_function("bad input")
```

### 4. Parameterized Tests

``` python
@pytest.mark.parametrize("input,expected", [
    ("2+2", "4"),
    ("10*5", "50"),
    ("100/4", "25"),
])
def test_calculator(input, expected):
    assert calculator(input) == expected
```

------------------------------------------------------------------------

## Continuous Integration (CI)

### GitHub Actions Example

Create `.github/workflows/test.yml`:

``` yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest test_main.py --cov=tools --cov=main
```

This runs your tests automatically on every commit!

------------------------------------------------------------------------

## Troubleshooting

### Problem: ImportError

```         
ImportError: No module named 'pytest'
```

**Solution**:

``` bash
pip install pytest
```

### Problem: Tests Can't Find Modules

```         
ModuleNotFoundError: No module named 'tools'
```

**Solution**:

``` bash
# Run from project root directory
cd /path/to/ai_agent
pytest test_main.py
```

### Problem: Fixtures Not Working

```         
fixture 'tmp_path' not found
```

**Solution**: Update pytest:

``` bash
pip install --upgrade pytest
```

------------------------------------------------------------------------

## Quick Reference

``` bash
# Run all tests
pytest test_main.py -v

# Run with coverage
pytest test_main.py --cov=tools --cov=main

# Run specific test
pytest test_main.py::TestDuckDuckGoTool::test_successful_search -v

# Run tests matching pattern
pytest test_main.py -k "search" -v

# Show print statements
pytest test_main.py -s

# Stop on first failure
pytest test_main.py -x

# Run last failed tests
pytest test_main.py --lf

# Show slowest tests
pytest test_main.py --durations=10
```

------------------------------------------------------------------------
