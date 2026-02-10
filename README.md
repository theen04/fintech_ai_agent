# FinTech AI Research Agent

A production-ready AI research agent that autonomously gathers, synthesizes, and structures information using LangChain and OpenAI's GPT-4. This project demonstrates advanced understanding of agentic AI workflows, tool integration, and structured output generation, with a focus on **FinTech and emerging AI applications in startups**.

---

## 🎯 Project Overview

This research agent autonomously:
- Searches multiple data sources (DuckDuckGo, Wikipedia)
- Synthesizes information from various sources
- Saves research notes for future reference
- Returns structured, validated JSON responses
- Is optimized for domain-specific research, such as FinTech and AI adoption trends

---

## 🛠️ Technologies Used

### Core Framework
- **LangChain / LangGraph**: Industry-standard framework for building LLM applications
- **OpenAI GPT-4**: State-of-the-art language model for reasoning and generation
- **Pydantic**: Data validation and structured output parsing

### Why These Tools?

**LangChain**:
- Provides abstractions for complex agent workflows
- Enables tool/function calling with LLMs
- Handles conversation memory and context management
- Industry standard used by companies like Microsoft, Notion, and Stripe

**LangGraph**:
- Built on top of LangChain for stateful and multi-step agent systems
- Provides better control flow, error handling, and observability
- Future-proof architecture for production AI systems

**Pydantic**:
- Ensures type-safe, structured outputs
- Prevents runtime errors from malformed responses
- Standard in production Python applications

---

## 🚀 Features

- ✅ **Autonomous Tool Selection**: Agent decides when and which tools to use
- ✅ **Structured Output**: JSON response format using Pydantic schema
- ✅ **Multi-Source Research**: Integrates web search and knowledge bases
- ✅ **Research Note Persistence**: Automatically saves raw notes for inspection
- ✅ **Error Handling**: Robust error recovery and parsing fallbacks
- ✅ **Extensible Architecture**: Easy to add new tools and outputs

---

## 📋 Prerequisites

- Python 3.10+
- OpenAI API key

---

## 🔧 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd fintech_ai_agent
```

2. **Create a virtual environment**
```bash
python -m venv ai_venv
source ai_venv/bin/activate  # On Windows: ai_venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📁 Project Structure

```
fintech_ai_agent/
├── main.py              # Main agent implementation
├── tools.py             # Custom tool definitions
├── test_main.py         # Unit and integration tests
├── pytest.ini           # Pytest configuration
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore           # Git ignore patterns
├── outputs/             # Research outputs directory
│   └── .gitkeep         # Keeps directory in git
├── README.md            # Project README (this file)
└── testing_guide.md     # Instructions for testing

```

## 💻 Usage

### Running the Agent

```bash
python main.py
```

Expected output:
```json
{
  "topic": "AI and machine learning in FinTech startups",
  "summary": "AI and ML are transforming FinTech startups by improving predictive analytics, automating processes, enhancing fraud detection, and enabling smarter customer experiences. Current trends include widespread adoption of chatbots, virtual assistants, and GenAI for personalized services. Key players include IBM, Scienaptic, Feedzai, and other emerging startups leveraging ML for credit risk assessment, payments, and investment platforms. The future is expected to see further hyper-personalization, real-time AI decision-making, and greater regulatory compliance solutions.",
  "sources": [
    "https://hqsoftwarelab.com/blog/benefits-use-cases-ml-ai-in-fintech/",
    "https://thefinancialtechnologyreport.com/the-top-25-fintech-ai-companies-of-2025/",
    "https://www.ibm.com/think/topics/ai-in-fintech"
  ],
  "tools_used": [
    "duckduckgo_tool",
    "save_raw_text"
  ]
}
```

### Saved Notes

`outputs/AI_and_ML_in_FinTech.txt`
`outputs/Key_players_in_FinTech_AI_and_ML.txt`


**Note**: Research notes are automatically saved to the `outputs/` directory to keep your project organized.

## 🔍 How It Works

### Agent Architecture

```
User Query → LLM (GPT-4) → Tool Selection → Tool Execution → LLM Processing → Structured JSON Output
                ↑                                                ↓
                └──────────── Iterative ReAct Loop ──────────────┘

```

### Key Components

1. **LLM Layer (OpenAI GPT-4)**
   - Performs reasoning, planning, and response generation
   - Decides when and how to invoke external tools
   - Synthesizes multi-source information into structured outputs

2. **Tooling Layer**
   - `duckduckgo_tool`: Real-time web search
   - `wikipedia_search`: Encyclopedic knowledge retrieval
   - `save_raw_text`: Persistent research logging
   - Designed for extensibility with custom tools

3. **Agent Orchestration (LangGraph)**
   - Manages multi-step reasoning and control flow
   - Implements the ReAct loop (reason → act → observe)
   - Handles retries, error recovery, and state management

4. **Schema & Validation Layer (Pydantic)**
   - Enforces structured JSON output
   - Prevents malformed LLM responses
   - Enables type-safe downstream integration

5. **Persistence & Observability**
   - Saves intermediate research artifacts to disk
   - Facilitates debugging, evaluation, and reproducibility


## 🎓 Technical Deep Dive

### Why Agents Matter

Traditional LLM applications follow a simple pattern:
```
User Input → LLM → Response
```

Agents add **autonomy and reasoning**:
```
User Input → LLM → [Decides: Need more info?]
                ↓
            [Uses Tools]
                ↓
            [Processes Results]
                ↓
            [Decides: Enough info?]
                ↓
            Final Response
```

This enables:
- Dynamic information gathering
- Multi-step reasoning
- Adaptation to unexpected situations
- Integration with external systems

### ReAct Pattern

This agent uses the **ReAct (Reasoning + Acting)** pattern:

1. **Thought**: LLM reasons about what to do next
2. **Action**: LLM calls a tool
3. **Observation**: Tool returns results
4. **Repeat**: Until task is complete

### Code Walkthrough

**Agent Creation (LangGraph)**
```python
agent_executor = create_react_agent(
    llm,              # The "brain"
    tools,            # Available actions
    state_modifier    # System instructions
)
```

**Tool Binding**
```python
llm_with_tools = llm.bind_tools(tools)
```
This tells the LLM what functions it can call and their schemas.

**Structured Output**
```python
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]
```
Pydantic ensures the agent always returns valid, type-safe data.

``` markdown
## Testing

This project includes comprehensive unit tests.

```bash
# Run tests
pytest test_main.py -v

# Run with coverage
pytest test_main.py --cov=tools --cov=main
```

Current test coverage: 81% \`\`\`

## 🔄 Extending the Agent

### Adding New Tools

```python
# tools.py
from langchain.tools import tool

@tool
def your_custom_tool(param: str) -> str:
    """Tool description for the LLM to understand when to use it."""
    # Your implementation
    return "result"
```

Then add to the tools list:
```python
tools = [duckduckgo_tool, wikipedia_search, save_raw_text, your_custom_tool]
```

### Adding New Output Fields

```python
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]
    confidence_score: float  # New field
    related_topics: List[str]  # New field
```

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
- Ensure you're using the correct LangChain version (1.2.9+)
- Use `langchain_classic` for agent imports
- Consider using LangGraph for modern implementations

**API Rate Limits**
- Implement retry logic with exponential backoff
- Use `max_iterations` to prevent infinite loops

**Parsing Failures**
- Use `OutputFixingParser` for automatic correction
- Implement fallback parsing with regex

**Tool Failures**
- Tools should return strings, not objects
- Always handle exceptions in tool implementations
- Provide clear error messages to the agent

## 📊 Performance Considerations

- **Token Usage**: Monitor with `tiktoken` for cost optimization
- **Latency**: Parallel tool execution for faster responses
- **Caching**: Implement result caching for repeated queries
- **Streaming**: Use streaming for real-time user feedback

## 🔐 Security Best Practices

- ✅ Never commit `.env` files
- ✅ Validate all tool inputs
- ✅ Sanitize user queries
- ✅ Implement rate limiting
- ✅ Use environment-specific API keys

## 📈 Future Enhancements

- [ ] Add memory/conversation history
- [ ] Implement multi-agent collaboration
- [ ] Add human-in-the-loop approval
- [ ] Integrate with vector databases (Pinecone, Weaviate)
- [ ] Add streaming responses
- [ ] Implement cost tracking
- [ ] Add evaluation metrics (accuracy, relevance)
- [ ] Create web UI with FastAPI/Streamlit

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Please open an issue to discuss proposed changes.

## 📝 License

MIT License - feel free to use this code for learning and portfolio purposes.

## 👤 Author

**Bobby Nitto**
- Portfolio: Coming soon
- LinkedIn: www.linkedin.com/in/bobby-nitto
- GitHub: https://github.com/theen04

## 🙏 Acknowledgments

This project was initially inspired by the YouTube tutorial:

➡️ https://www.youtube.com/watch?v=bTMPwUgLZf0

I used the video as a *learning foundation* to understand agent workflows with LangChain and OpenAI. From there, I extended the architecture with additional tools, structured output parsing, FinTech‑focused research logic, and robust coding practices. The final design and implementation are my own work and reflect my understanding of agent systems and production‑ready Python development.

**Additional Support**

- LangChain documentation and community
- OpenAI for GPT-4 API
- Anthropic's Claude for development assistance

---

**Built with ❤️ and curiosity about AI in FinTech**
