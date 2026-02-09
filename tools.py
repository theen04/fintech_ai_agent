"""
Custom tools for the AI Research Agent.

Each tool is decorated with @tool to make it compatible with LangChain agents.
The docstring of each function is crucial - it tells the LLM when and how to use the tool.
"""

from langchain_classic.tools import tool
from typing import Optional
import os


@tool
def duckduckgo_tool(query: str) -> str:
    """
    Search DuckDuckGo for current information on a topic.
    
    Use this tool when you need:
    - Current events or news
    - Recent developments
    - Web-based information
    - Multiple perspectives on a topic
    
    Args:
        query: The search query string
        
    Returns:
        Formatted search results with titles and snippets
    """
    try:
        from ddgs import DDGS
        
        # Perform search
        results = DDGS().text(query, max_results=5)
        
        # Format results
        if not results:
            return f"No results found for query: {query}"
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   {result['body']}\n"
            )
        
        return "\n".join(formatted_results)
        
    except ImportError:
        return (
            "DuckDuckGo search is not available. "
            "Install it with: pip install duckduckgo-search"
        )
    except Exception as e:
        return f"Error performing search: {str(e)}"


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for detailed, encyclopedic information on a topic.
    
    Use this tool when you need:
    - Historical information
    - Scientific concepts
    - Biographical information
    - Detailed explanations of topics
    - Well-established facts
    
    Args:
        query: The topic to search for on Wikipedia
        
    Returns:
        Summary of the Wikipedia article (first few sentences)
    """
    try:
        import wikipedia
        
        # Set language to English
        wikipedia.set_lang("en")
        
        # Search and get summary
        try:
            summary = wikipedia.summary(query, sentences=5, auto_suggest=True)
            page = wikipedia.page(query, auto_suggest=True)
            
            return (
                f"Wikipedia Article: {page.title}\n"
                f"URL: {page.url}\n\n"
                f"Summary:\n{summary}\n"
            )
        except wikipedia.DisambiguationError as e:
            # Multiple options found
            options = e.options[:5]
            return (
                f"Multiple Wikipedia articles found for '{query}'.\n"
                f"Please be more specific. Options include:\n"
                + "\n".join(f"- {opt}" for opt in options)
            )
        except wikipedia.PageError:
            return f"No Wikipedia article found for '{query}'"
            
    except ImportError:
        return (
            "Wikipedia search is not available. "
            "Install it with: pip install wikipedia"
        )
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


@tool
def save_raw_text(text: str, filename: Optional[str] = None) -> str:
    """
    Save research notes or findings to a text file for future reference.
    
    Use this tool to:
    - Store important findings
    - Keep track of sources
    - Build a research knowledge base
    - Save intermediate results
    
    Args:
        text: The text content to save
        filename: Optional filename (defaults to 'research_notes.txt')
        
    Returns:
        Confirmation message with the filename
    """
    try:
        # Create outputs directory if it doesn't exist
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Default filename
        if filename is None:
            filename = "research_notes.txt"
        
        # Ensure safe filename
        filename = os.path.basename(filename)
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Full path with output directory
        filepath = os.path.join(output_dir, filename)
        
        # Create a header with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"\n{'='*60}\n[{timestamp}]\n{'='*60}\n"
        
        # Append to file
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(header)
            f.write(text)
            f.write("\n")
        
        return f"Successfully saved research notes to '{filepath}'"
        
    except Exception as e:
        return f"Error saving file: {str(e)}"


# Optional: Add more tools as needed

@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    
    Use this tool when you need to:
    - Calculate numbers
    - Perform arithmetic operations
    - Evaluate mathematical expressions
    
    Args:
        expression: A mathematical expression (e.g., "2 + 2", "10 * 5 - 3")
        
    Returns:
        The result of the calculation
        
    Example:
        calculator("100 / 4 + 10") returns "35.0"
    """
    try:
        # Security: Only allow safe mathematical operations
        # Using eval is dangerous, so we restrict to numbers and basic operators
        allowed_chars = set("0123456789+-*/()%. ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"
        
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
        
    except Exception as e:
        return f"Error calculating: {str(e)}"


# Export all tools for easy import
__all__ = [
    'duckduckgo_tool',
    'wikipedia_search',
    'save_raw_text',
    'calculator',
]