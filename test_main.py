"""
Unit tests for AI Research Agent tools and components.

These tests demonstrate understanding of testing AI systems, including:
- Mocking external API calls
- Testing tool behavior in isolation
- Validating structured outputs
- Handling edge cases

SETUP:
------
Install test dependencies:
    pip install pytest pytest-cov

Optional (for Wikipedia tests):
    pip install wikipedia

RUNNING TESTS:
--------------
Run all tests:
    pytest test_main.py -v

Run specific test class:
    pytest test_main.py::TestDuckDuckGoTool -v

Run with coverage report:
    pytest test_main.py --cov=. --cov-report=html

Skip integration tests (default):
    pytest test_main.py -v

Run integration tests (requires API keys):
    pytest test_main.py -m integration -v

NOTES:
------
- External APIs are mocked, so tests run offline
- No API keys needed for unit tests
- Integration tests are skipped by default (they cost money)
- Tests use tmp_path fixture for file operations
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pydantic import ValidationError
from tools import duckduckgo_tool, wikipedia_search, save_raw_text, calculator
import os

# Check if optional dependencies are available
try:
    import ddgs
    HAS_DUCKDUCKGO = True
except ImportError:
    HAS_DUCKDUCKGO = False

try:
    import wikipedia
    HAS_WIKIPEDIA = True
except ImportError:
    HAS_WIKIPEDIA = False

# This fixture patches ChatOpenAI globally for all tests
@pytest.fixture(autouse=True)
def patch_llm():
    """
    Mock the ChatOpenAI object in main.py to prevent real API calls.
    Applied automatically to all tests (autouse=True).
    """
    with patch("main.ChatOpenAI") as mock_llm:
        # Optionally, mock any methods if needed, e.g., mock_llm.return_value.chat.return_value = "mocked"
        mock_llm.return_value.chat.return_value = "Mocked response"
        yield

# =============================================================================
# Tool Tests
# =============================================================================

@pytest.mark.skipif(not HAS_DUCKDUCKGO, reason="duckduckgo_search not installed")
class TestDuckDuckGoTool:
    """Tests for the DuckDuckGo search tool."""
    
    @patch('ddgs.DDGS')
    def test_successful_search(self, mock_ddgs):
        """Test that search returns formatted results."""
        # Mock search results
        mock_results = [
            {
                'title': 'Test Result 1',
                'href': 'https://example.com/1',
                'body': 'This is a test result'
            },
            {
                'title': 'Test Result 2',
                'href': 'https://example.com/2',
                'body': 'Another test result'
            }
        ]
        mock_ddgs.return_value.text.return_value = mock_results
        
        # Execute
        result = duckduckgo_tool.invoke({"query": "test query"})
        
        # Assert
        assert "Test Result 1" in result
        assert "Test Result 2" in result
        assert "https://example.com/1" in result
        
    @patch('ddgs.DDGS')
    def test_empty_search_results(self, mock_ddgs):
        """Test handling of empty search results."""
        mock_ddgs.return_value.text.return_value = []
        
        result = duckduckgo_tool.invoke({"query": "obscure query"})
        
        assert "No results found" in result
        
    @patch('ddgs.DDGS')
    def test_search_exception_handling(self, mock_ddgs):
        """Test graceful handling of search errors."""
        mock_ddgs.return_value.text.side_effect = Exception("API Error")
        
        result = duckduckgo_tool.invoke({"query": "test"})
        
        assert "Error" in result


@pytest.mark.skipif(not HAS_WIKIPEDIA, reason="wikipedia not installed")
class TestWikipediaSearch:
    """Tests for Wikipedia search tool."""
    
    @patch('wikipedia.summary')
    @patch('wikipedia.page')
    def test_successful_search(self, mock_page, mock_summary):
        """Test successful Wikipedia article retrieval."""
        mock_summary.return_value = "This is a test summary"
        mock_page_obj = Mock()
        mock_page_obj.title = "Test Article"
        mock_page_obj.url = "https://en.wikipedia.org/wiki/Test"
        mock_page.return_value = mock_page_obj
        
        result = wikipedia_search.invoke({"query": "test topic"})
        
        assert "Test Article" in result
        assert "This is a test summary" in result
        assert "https://en.wikipedia.org/wiki/Test" in result
        
    @patch('wikipedia.summary')
    @patch('wikipedia.page')
    def test_disambiguation_error(self, mock_page, mock_summary):
        """Test handling of disambiguation pages."""
        from wikipedia import DisambiguationError
        mock_summary.side_effect = DisambiguationError(
            "test", 
            ["Option 1", "Option 2", "Option 3"]
        )
        
        result = wikipedia_search.invoke({"query": "test"})
        
        assert "Multiple Wikipedia articles found" in result
        assert "Option 1" in result
        
    @patch('wikipedia.summary')
    def test_page_not_found(self, mock_summary):
        """Test handling of non-existent pages."""
        from wikipedia import PageError
        mock_summary.side_effect = PageError("test")
        
        result = wikipedia_search.invoke({"query": "nonexistent"})
        
        assert "No Wikipedia article found" in result


class TestSaveRawText:
    """Tests for text saving tool."""
    
    def test_save_to_default_file(self, tmp_path):
        """Test saving to default filename in outputs directory."""
        # Change to temp directory
        os.chdir(tmp_path)
        
        result = save_raw_text.invoke({
            "text": "Test content",
            "filename": None
        })
        
        assert "Successfully saved" in result
        assert os.path.exists("outputs/research_notes.txt")
        
        with open("outputs/research_notes.txt") as f:
            content = f.read()
            assert "Test content" in content
            
    def test_save_with_custom_filename(self, tmp_path):
        """Test saving with custom filename in outputs directory."""
        os.chdir(tmp_path)
        
        result = save_raw_text.invoke({
            "text": "Custom content",
            "filename": "custom.txt"
        })
        
        assert "outputs/custom.txt" in result
        assert os.path.exists("outputs/custom.txt")
        
    def test_append_to_existing_file(self, tmp_path):
        """Test that saves append rather than overwrite."""
        os.chdir(tmp_path)
        
        save_raw_text.invoke({"text": "First", "filename": "test.txt"})
        save_raw_text.invoke({"text": "Second", "filename": "test.txt"})
        
        with open("outputs/test.txt") as f:
            content = f.read()
            assert "First" in content
            assert "Second" in content
    
    def test_outputs_directory_created(self, tmp_path):
        """Test that outputs directory is created automatically."""
        os.chdir(tmp_path)
        
        # Ensure directory doesn't exist
        assert not os.path.exists("outputs")
        
        save_raw_text.invoke({"text": "Test", "filename": "test.txt"})
        
        # Directory should now exist
        assert os.path.exists("outputs")
        assert os.path.isdir("outputs")


class TestCalculator:
    """Tests for calculator tool."""
    
    def test_simple_addition(self):
        """Test basic addition."""
        result = calculator.invoke({"expression": "2 + 2"})
        assert "4" in result
        
    def test_complex_expression(self):
        """Test complex mathematical expression."""
        result = calculator.invoke({"expression": "(10 * 5) - 3 + 8"})
        assert "55" in result
        
    def test_invalid_characters(self):
        """Test rejection of dangerous input."""
        result = calculator.invoke({"expression": "import os"})
        assert "invalid" in result.lower()
        
    def test_division_by_zero(self):
        """Test handling of division by zero."""
        result = calculator.invoke({"expression": "10 / 0"})
        assert "Error" in result


# =============================================================================
# Pydantic Model Tests
# =============================================================================

class TestResearchResponse:
    """Tests for ResearchResponse model validation."""
    
    def test_valid_response(self):
        """Test creation of valid response."""
        from main import ResearchResponse
        
        response = ResearchResponse(
            topic="Climate Change",
            summary="Test summary",
            sources=["source1", "source2"],
            tools_used=["tool1"]
        )
        
        assert response.topic == "Climate Change"
        assert len(response.sources) == 2
        
    def test_missing_required_field(self):
        """Test that missing fields raise validation error."""
        from main import ResearchResponse
        
        with pytest.raises(ValidationError):
            ResearchResponse(
                topic="Test",
                summary="Test"
                # Missing sources and tools_used
            )
            
    def test_wrong_type(self):
        """Test that wrong types raise validation error."""
        from main import ResearchResponse
        
        with pytest.raises(ValidationError):
            ResearchResponse(
                topic="Test",
                summary="Test",
                sources="not a list",  # Should be List[str]
                tools_used=["tool1"]
            )


# =============================================================================
# Integration Tests
# =============================================================================

class TestAgentIntegration:
    """Integration tests for the full agent."""
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires full agent setup and API keys")
    def test_agent_uses_multiple_tools(self):
        """Test that agent can orchestrate multiple tools."""
        # This would be a full integration test with the agent
        # Requires actual LLM calls or extensive mocking
        # Skip in CI/CD, run manually with: pytest -m integration
        pass
        
    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires API keys and costs money")
    def test_agent_returns_structured_output(self):
        """Test that agent always returns valid structured output."""
        # Would test the full agent with real API calls
        pass


# =============================================================================
# Test Configuration
# =============================================================================

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls for testing."""
    with patch('openai.OpenAI') as mock:
        yield mock


# Run tests with: pytest test_main.py -v
# Run with coverage: pytest test_main.py --cov=. --cov-report=html