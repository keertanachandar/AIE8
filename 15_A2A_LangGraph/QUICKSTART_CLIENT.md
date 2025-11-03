# 🚀 Quick Start Guide - A2A Client Agent

## 📋 Prerequisites

Before starting, make sure you have:

1. ✅ Python 3.12 or higher
2. ✅ `uv` package manager installed
3. ✅ OpenAI API key
4. ✅ Tavily API key (for web search)

## ⚡ 5-Minute Setup

### Step 1: Environment Setup

```bash
# Make sure you're in the project directory
cd /path/to/15_A2A_LangGraph

# Create .env file if you haven't already
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
TOOL_LLM_NAME=gpt-4o-mini
OPENAI_CHAT_MODEL=gpt-4o-mini
RAG_DATA_DIR=data
EOF
```

### Step 2: Install Dependencies

```bash
# Run the quickstart script (installs everything)
./quickstart.sh

# Or manually with uv
uv sync
```

### Step 3: Start the A2A Server

Open a **new terminal window** and run:

```bash
cd /path/to/15_A2A_LangGraph
uv run python -m app
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:10000
```

✅ **Server is running!** Keep this terminal open.

### Step 4: Run the Client Agent

Open **another terminal window** and run:

```bash
cd /path/to/15_A2A_LangGraph
uv run python app/run_client_agent.py -i
```

You should see:
```
================================================================================
🤖 A2A Client Agent - Interactive Session
================================================================================

Connecting to A2A server at: http://localhost:10000

This agent can delegate tasks to the A2A agent which has:
  • Web search capabilities (Tavily)
  • Academic paper search (ArXiv)
  • Document retrieval (RAG)

Type 'quit' or 'exit' to end the session
Type 'help' for examples
================================================================================
```

✅ **Client agent is ready!** You can now start chatting.

## 💬 Try These Examples

### Example 1: Web Search

```
👤 You: What are the latest developments in artificial intelligence?

🤖 Agent (thinking...)
   🔧 Using tool: query_a2a_agent

🤖 Agent: Based on the search results, here are recent AI developments...
```

### Example 2: Academic Papers

```
👤 You: Find recent papers on transformer architectures

🤖 Agent (thinking...)
   🔧 Using tool: query_a2a_agent

🤖 Agent: I found several papers on transformers:
1. "Attention Is All You Need 2.0" - [arXiv:2024.xxxxx]
...
```

### Example 3: Follow-up Question

```
👤 You: Find papers on large language models

🤖 Agent: [Returns papers]

👤 You: Can you summarize the key findings?

🤖 Agent (thinking...)
   🔧 Using tool: continue_a2a_conversation

🤖 Agent: The key findings from these papers are:
1. Scaling laws continue to apply...
...
```

### Example 4: Simple Question (No A2A Call)

```
👤 You: What is 2 + 2?

🤖 Agent: 2 + 2 equals 4.
```

Notice: No tool call needed for simple questions!

## 🧪 Running Tests

Verify everything works:

```bash
# Run automated tests
uv run python test_client_agent.py
```

Expected output:
```
🧪 Testing A2A Client Agent
✅ Test 1 PASSED: Client agent created successfully
✅ Test 2 PASSED: Agent responded successfully  
✅ Test 3 PASSED: A2A tool used successfully
✅ Test 4 PASSED: Graph visualization generated
🎉 Testing Complete!
```

## 🎯 Single Query Mode

For quick one-off queries:

```bash
uv run python app/run_client_agent.py -q "What are recent AI breakthroughs?"
```

This runs the query and exits (no interactive session).

## 🔍 Viewing the Graph

Visualize the client agent structure:

```bash
uv run python app/visualize_client.py
```

This creates:
- `client_agent_graph.mmd` - Mermaid diagram
- `client_agent_graph.png` - PNG image (if graphviz installed)

View the diagram at [mermaid.live](https://mermaid.live/)

## 📊 Understanding the Output

### When Agent Uses A2A Tool

```
👤 You: [Your query]

🤖 Agent (thinking...)        ← Agent deciding what to do
   🔧 Using tool: query_a2a_agent  ← Calling A2A server

🤖 Agent: [Response from A2A server]
```

### When Agent Responds Directly

```
👤 You: What is 2 + 2?

🤖 Agent: 2 + 2 equals 4.    ← Direct response, no tools
```

## 🐛 Troubleshooting

### Issue: "Connection refused"

**Problem**: A2A server is not running

**Solution**:
```bash
# Start the server in a separate terminal
uv run python -m app
```

### Issue: "Timeout error"

**Problem**: Query is taking too long

**Solution**: This is normal for complex queries. Wait up to 30 seconds.

### Issue: "Missing API key"

**Problem**: Environment variables not set

**Solution**:
```bash
# Check your .env file has:
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

### Issue: No tool calls happening

**Problem**: Agent deciding to respond directly

**Solution**: Try more specific queries:
- ❌ "Tell me about AI" (too vague)
- ✅ "Search for the latest AI news from this week" (specific)
- ✅ "Find papers on transformer architectures" (actionable)

## 📚 Next Steps

### 1. Read the Documentation

- **[CLIENT_AGENT.md](./CLIENT_AGENT.md)** - Detailed client agent guide
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete system architecture
- **[app/README.md](./app/README.md)** - Server agent documentation

### 2. Customize the Client

Edit `app/client_agent.py`:
```python
system_instruction = """
Your custom instructions here...
"""
```

### 3. Add Custom Tools

Create new tools in `app/a2a_tool.py`:
```python
@tool
async def my_custom_tool(query: str) -> str:
    """Your tool description"""
    # Implementation
    return result
```

### 4. Test Different Scenarios

Try these query types:
- Current events: "What's happening in tech today?"
- Academic research: "Find papers on quantum computing"
- Multi-turn: Ask follow-up questions
- Simple math: "Calculate 25 * 4"
- Mixed: "Compare recent AI research with current news"

## 🎓 Understanding the Flow

```
1. You type a query
   ↓
2. Client Agent receives it
   ↓
3. Agent decides: Use A2A tool or respond directly?
   ↓
4a. If A2A needed:
    → Calls server agent via HTTP
    → Server processes (may use tools: Tavily, ArXiv, RAG)
    → Server evaluates helpfulness
    → Returns result to client
    ↓
4b. If direct response:
    → Agent responds immediately
    ↓
5. You see the final answer
```

## 💡 Pro Tips

### Tip 1: Use Descriptive Queries

Better results with specific queries:
- ❌ "AI"
- ✅ "What are the latest breakthroughs in AI for 2025?"

### Tip 2: Multi-Turn Conversations

The agent maintains context:
```
You: Find papers on attention mechanisms
Agent: [Returns papers]

You: Summarize the first one  ← Remembers context!
Agent: [Summarizes first paper from previous response]
```

### Tip 3: See What's Happening

Watch both terminals:
- **Client terminal**: See user interaction
- **Server terminal**: See tool calls and processing

### Tip 4: Custom Server URL

Point to a different server:
```bash
uv run python app/run_client_agent.py --base-url http://your-server:8080 -i
```

## 🎨 Example Session

Here's a complete example session:

```bash
$ uv run python app/run_client_agent.py -i

================================================================================
🤖 A2A Client Agent - Interactive Session
================================================================================

👤 You: Find recent papers on transformer architectures

🤖 Agent (thinking...)
   🔧 Using tool: query_a2a_agent

🤖 Agent: I found several recent papers on transformer architectures:

1. "Attention Mechanisms in Modern Transformers" - [arXiv:2024.12345]
   Published: October 2024
   Abstract: This paper explores novel attention mechanisms...

2. "Efficient Transformers: A Survey" - [arXiv:2024.67890]
   Published: November 2024
   Abstract: We survey recent advances in efficient transformer designs...

[More papers...]

👤 You: Can you summarize the key innovations in the first paper?

🤖 Agent (thinking...)
   🔧 Using tool: continue_a2a_conversation

🤖 Agent: The key innovations in "Attention Mechanisms in Modern Transformers" are:

1. **Sparse Attention**: Reduces computational complexity from O(n²) to O(n log n)
2. **Multi-scale Attention**: Processes information at different scales
3. **Adaptive Attention**: Dynamically adjusts based on input

These innovations make transformers more efficient for long sequences.

👤 You: What is 5 * 8?

🤖 Agent: 5 * 8 equals 40.

👤 You: quit

👋 Goodbye!
```

## ✅ Success Checklist

Before moving forward, verify:

- [ ] Server starts without errors
- [ ] Client connects to server successfully
- [ ] Agent can make A2A tool calls
- [ ] Agent responds directly to simple queries
- [ ] Multi-turn conversations work
- [ ] Tests pass successfully

## 🚀 You're Ready!

Congratulations! You now have a working A2A client agent that can:

✅ Delegate complex tasks to specialized agents  
✅ Manage multi-turn conversations  
✅ Make intelligent decisions about when to use tools  
✅ Communicate via the A2A protocol  

### What You Built

You've completed **Activity #1** from the homework:

> Build a LangGraph Graph to "use" your application.
> 
> Do this by creating a Simple Agent that can make API calls to the 🤖Agent Node above through the A2A protocol.

**You built**:
1. ✅ LangGraph client agent (`app/client_agent.py`)
2. ✅ A2A communication tools (`app/a2a_tool.py`)
3. ✅ Interactive CLI (`app/run_client_agent.py`)
4. ✅ Tests and visualization tools
5. ✅ Complete documentation

### Record Your Demo

For your homework submission, record a Loom showing:
1. Starting the A2A server
2. Running the client agent
3. Example queries (web search, academic papers, follow-ups)
4. Multi-turn conversation
5. Explaining how it works

---

**Happy agent building! 🤖**

Need help? See the [full documentation](./CLIENT_AGENT.md) or check the [architecture guide](./ARCHITECTURE.md).

