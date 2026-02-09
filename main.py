from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain_classic.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from tools import duckduckgo_tool, wikipedia_search, save_raw_text

load_dotenv()

# --------------------
# Output Schema
# --------------------
class ResearchResponse(BaseModel):
    topic: str = Field(description="The research topic")
    summary: str = Field(description="A comprehensive summary of findings")
    sources: List[str] = Field(description="List of sources used")
    tools_used: List[str] = Field(description="List of tools utilized")

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# --------------------
# LLM (OpenAI)
# --------------------
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.4
)

# --------------------
# Tools
# --------------------
tools = [duckduckgo_tool, wikipedia_search, save_raw_text]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# --------------------
# Prompt
# --------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
"""You are a research assistant.

Your task:
1. Use search tools to gather information about the topic
2. Save raw research notes using the save_raw_text tool
3. After gathering all information, provide your final answer

IMPORTANT: Your final response MUST be valid JSON matching this schema:
{format_instructions}

Track which tools you use and which sources you find.
"""),
    ("human", "{query}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
]).partial(format_instructions=parser.get_format_instructions())

# --------------------
# Create Agent Chain
# --------------------
agent = (
    {
        "query": lambda x: x["query"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

# --------------------
# Agent Executor
# --------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

# --------------------
# Run
# --------------------
if __name__ == "__main__":
    try:
        result = agent_executor.invoke({
            "query": "Research the adoption of AI and machine learning in FinTech startups. Provide a comprehensive analysis of current trends, key players, and potential future developments."
        })
        
        output_text = result["output"]
        print("\n" + "="*50)
        print("RAW OUTPUT:")
        print(output_text)
        print("="*50 + "\n")
        
        # Try to parse the response
        response = parser.parse(output_text)
        print("PARSED RESPONSE:")
        print(f"Topic: {response.topic}")
        print(f"Summary: {response.summary}")
        print(f"Sources: {', '.join(response.sources)}")
        print(f"Tools Used: {', '.join(response.tools_used)}")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'result' in locals():
            print(f"Raw output: {result.get('output', 'No output')}")